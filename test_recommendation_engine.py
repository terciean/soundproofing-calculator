import unittest
from solutions.recommendation_engine import RecommendationEngine, NoiseProfile, RoomProfile

class TestRecommendationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RecommendationEngine()
        
    def test_basic_recommendations(self):
        """Test basic recommendations for different noise types"""
        noise_types = ["speech", "music", "tv", "traffic", "impact", "footsteps", "machinery"]
        room = RoomProfile(
            dimensions={"length": 4.0, "width": 3.0, "height": 2.4},
            surfaces=["walls", "ceiling", "floor"],
            room_type="bedroom"
        )
        
        for noise_type in noise_types:
            noise = NoiseProfile(
                type=noise_type,
                intensity=5,
                direction=["north"]
            )
            
            recommendations = self.engine.get_recommendations(noise, room)
            
            # Verify basic structure
            self.assertIn("primary", recommendations)
            self.assertIn("walls", recommendations["primary"])
            self.assertIn("ceiling", recommendations["primary"])
            self.assertIn("floor", recommendations["primary"])
            self.assertIn("reasoning", recommendations)
            
            # Verify wall solutions
            self.assertIsInstance(recommendations["primary"]["walls"], list)
            if recommendations["primary"]["walls"]:
                self.assertLessEqual(len(recommendations["primary"]["walls"]), 3)
                for solution in recommendations["primary"]["walls"]:
                    self.assertIn("solution", solution)
                    self.assertIn("materials", solution)
                    self.assertIn("score", solution)
                    self.assertIn("effectiveness", solution)
                    
    def test_intensity_variations(self):
        """Test recommendations for different noise intensities"""
        intensities = [1, 5, 10]
        noise = NoiseProfile(
            type="music",
            intensity=5,
            direction=["north"]
        )
        room = RoomProfile(
            dimensions={"length": 4.0, "width": 3.0, "height": 2.4},
            surfaces=["walls", "ceiling", "floor"],
            room_type="bedroom"
        )
        
        for intensity in intensities:
            noise.intensity = intensity
            recommendations = self.engine.get_recommendations(noise, room)
            
            # Verify recommendations reflect intensity
            if recommendations["primary"]["walls"]:
                for solution in recommendations["primary"]["walls"]:
                    self.assertGreater(solution["effectiveness"], 0)
                    
    def test_direction_combinations(self):
        """Test recommendations for different direction combinations"""
        directions = [
            ["north"],
            ["north", "south"],
            ["above"],
            ["below"],
            ["north", "above"],
            ["north", "south", "above", "below"]
        ]
        
        noise = NoiseProfile(
            type="music",
            intensity=5,
            direction=["north"]
        )
        room = RoomProfile(
            dimensions={"length": 4.0, "width": 3.0, "height": 2.4},
            surfaces=["walls", "ceiling", "floor"],
            room_type="bedroom"
        )
        
        for direction_set in directions:
            noise.direction = direction_set
            recommendations = self.engine.get_recommendations(noise, room)
            
            # Verify affected surfaces are handled
            affected_surfaces = self.engine._get_affected_surfaces(direction_set)
            
            if affected_surfaces["walls"]:
                self.assertGreater(len(recommendations["primary"]["walls"]), 0)
            if affected_surfaces["ceiling"]:
                self.assertIsNotNone(recommendations["primary"]["ceiling"])
            if affected_surfaces["floor"]:
                self.assertIsNotNone(recommendations["primary"]["floor"])
                
    def test_room_variations(self):
        """Test recommendations for different room types and dimensions"""
        room_configs = [
            {
                "dimensions": {"length": 3.0, "width": 2.5, "height": 2.2},
                "surfaces": ["walls", "ceiling"],
                "room_type": "bathroom"
            },
            {
                "dimensions": {"length": 5.0, "width": 4.0, "height": 2.4},
                "surfaces": ["walls", "floor"],
                "room_type": "living_room"
            },
            {
                "dimensions": {"length": 4.0, "width": 3.0, "height": 2.4},
                "surfaces": ["walls", "ceiling", "floor"],
                "room_type": "bedroom"
            }
        ]
        
        noise = NoiseProfile(
            type="music",
            intensity=5,
            direction=["north"]
        )
        
        for config in room_configs:
            room = RoomProfile(**config)
            recommendations = self.engine.get_recommendations(noise, room)
            
            # Verify only requested surfaces are included
            for surface in ["walls", "ceiling", "floor"]:
                if surface in config["surfaces"]:
                    if surface == "walls":
                        self.assertGreater(len(recommendations["primary"]["walls"]), 0)
                    else:
                        self.assertIsNotNone(recommendations["primary"][surface])
                        
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Test invalid noise type
        with self.assertRaises(ValueError):
            NoiseProfile(
                type="invalid_noise",
                intensity=5,
                direction=["north"]
            )
            
        # Test invalid intensity
        with self.assertRaises(ValueError):
            NoiseProfile(
                type="music",
                intensity=11,
                direction=["north"]
            )
            
        # Test invalid direction
        with self.assertRaises(ValueError):
            NoiseProfile(
                type="music",
                intensity=5,
                direction=["invalid_direction"]
            )
            
        # Test invalid room dimensions
        with self.assertRaises(ValueError):
            RoomProfile(
                dimensions={"length": -1, "width": 3.0, "height": 2.4},
                surfaces=["walls"]
            )
            
        # Test invalid surface
        with self.assertRaises(ValueError):
            RoomProfile(
                dimensions={"length": 4.0, "width": 3.0, "height": 2.4},
                surfaces=["invalid_surface"]
            )
            
    def test_recommendation_logic(self):
        """Test that recommendations are logically consistent"""
        noise = NoiseProfile(
            type="music",
            intensity=5,
            direction=["north"]
        )
        room = RoomProfile(
            dimensions={"length": 4.0, "width": 3.0, "height": 2.4},
            surfaces=["walls", "ceiling", "floor"],
            room_type="bedroom"
        )
        
        recommendations = self.engine.get_recommendations(noise, room)
        
        # Verify reasoning is provided
        self.assertGreater(len(recommendations["reasoning"]), 0)
        
        # Verify wall solutions are sorted by score
        if len(recommendations["primary"]["walls"]) > 1:
            scores = [s["score"] for s in recommendations["primary"]["walls"]]
            self.assertEqual(scores, sorted(scores, reverse=True))
            
        # Verify effectiveness is reasonable
        for surface in ["walls", "ceiling", "floor"]:
            if surface == "walls":
                for solution in recommendations["primary"]["walls"]:
                    self.assertGreaterEqual(solution["effectiveness"], 0)
                    self.assertLessEqual(solution["effectiveness"], 1)
            elif recommendations["primary"][surface]:
                self.assertGreaterEqual(recommendations["primary"][surface]["effectiveness"], 0)
                self.assertLessEqual(recommendations["primary"][surface]["effectiveness"], 1)

    def test_concurrent_recommendations(self):
        """Test concurrent recommendation requests for thread safety and cache consistency"""
        import threading
        results = []
        def worker(noise_type, intensity):
            noise = NoiseProfile(type=noise_type, intensity=intensity, direction=["north"])
            room = RoomProfile(dimensions={"length": 4.0, "width": 3.0, "height": 2.4}, surfaces=["walls", "ceiling", "floor"], room_type="bedroom")
            recs = self.engine.get_recommendations(noise, room)
            results.append(recs)
        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=("music", 5 + i % 3))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(len(results), 10)
        for rec in results:
            self.assertIn("primary", rec)
            self.assertIn("walls", rec["primary"])

    def test_cache_invalidation(self):
        """Test cache invalidation and refresh logic"""
        from solutions.cache_manager import get_cache_manager
        cache_manager = get_cache_manager()
        noise = NoiseProfile(type="music", intensity=5, direction=["north"])
        room = RoomProfile(dimensions={"length": 4.0, "width": 3.0, "height": 2.4}, surfaces=["walls", "ceiling", "floor"], room_type="bedroom")
        rec1 = self.engine.get_recommendations(noise, room)
        cache_manager.clear()
        rec2 = self.engine.get_recommendations(noise, room)
        self.assertEqual(rec1["primary"].keys(), rec2["primary"].keys())

    def test_edge_case_empty_room(self):
        """Test recommendations for a room with no surfaces"""
        noise = NoiseProfile(type="music", intensity=5, direction=["north"])
        room = RoomProfile(dimensions={"length": 4.0, "width": 3.0, "height": 2.4}, surfaces=[], room_type="bedroom")
        rec = self.engine.get_recommendations(noise, room)
        self.assertIn("primary", rec)
        self.assertEqual(rec["primary"].get("walls"), [])
        self.assertIsNone(rec["primary"].get("ceiling"))
        self.assertIsNone(rec["primary"].get("floor"))

if __name__ == '__main__':
    unittest.main()