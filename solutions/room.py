class Room:
    # Add ceiling feature definitions at class level
    CEILING_FEATURES = {
        'concrete': {
            'density': 2400,  # kg/m³
            'thickness': 0.15,  # meters
            'soundproof_rating': 55  # dB reduction
        },
        'timber': {
            'density': 500,  # kg/m³
            'thickness': 0.025,  # meters
            'soundproof_rating': 35  # dB reduction
        },
        'coving': {
            'area_reduction': 0.05,  # 5% reduction in ceiling area
            'soundproof_rating': 2  # dB reduction
        },
        'down_lights': {
            'area_per_light': 0.09,  # m² per light
            'soundproof_reduction': -3  # dB reduction (negative because it reduces soundproofing)
        }
    }

    # Add floor feature definitions
    FLOOR_FEATURES = {
        'parquet': {
            'thickness': 0.015,  # meters
            'soundproof_rating': 25  # dB reduction
        },
        'floor_boards': {
            'thickness': 0.020,  # meters
            'soundproof_rating': 30  # dB reduction
        },
        'lino': {
            'thickness': 0.002,  # meters
            'soundproof_rating': 15  # dB reduction
        },
        'real_wood': {
            'thickness': 0.025,  # meters
            'soundproof_rating': 35  # dB reduction
        }
    }

    def __init__(self, name, length, width, height):
        # Validate dimensions
        try:
            self.length = float(length)
            self.width = float(width)
            self.height = float(height)
            
            if any(d <= 0 for d in [self.length, self.width, self.height]):
                raise ValueError("All dimensions must be positive numbers")
                
            self.name = str(name)
            self.walls = []
            self.blockages = []
            self.floor = {
                'area': 0,
                'effective_area': 0,
                'features': [],
                'soundproof_rating': 0
            }
            self.ceiling = {
                'area': 0,
                'effective_area': 0,
                'features': [],
                'mass': 0,
                'soundproof_rating': 0
            }
            
            # Initialize room components
            self._initialize_walls()
            self._initialize_floor_ceiling()
            
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid room dimensions: {str(e)}")

    def _initialize_floor_ceiling(self):
        """Initialize floor and ceiling with base properties"""
        base_area = self.length * self.width
        
        # Initialize ceiling (existing code)
        self.ceiling.update({
            'area': base_area,
            'effective_area': base_area,
            'features': [],
            'mass': 0,
            'soundproof_rating': 0
        })
        
        # Initialize floor
        self.floor.update({
            'area': base_area,
            'effective_area': base_area,
            'features': [],
            'soundproof_rating': 0
        })

    def add_ceiling_feature(self, feature_type):
        """Add a ceiling feature and recalculate properties"""
        if feature_type not in self.CEILING_FEATURES:
            raise ValueError(f"Unknown ceiling feature: {feature_type}")
        
        if feature_type not in self.ceiling['features']:
            self.ceiling['features'].append(feature_type)
            self._recalculate_ceiling_properties()

    def _recalculate_ceiling_properties(self):
        """Recalculate ceiling properties based on features"""
        base_area = self.length * self.width
        effective_area = base_area
        mass = 0
        soundproof_rating = 0

        for feature in self.ceiling['features']:
            feature_data = self.CEILING_FEATURES[feature]
            
            # Calculate mass and area effects
            if feature in ['concrete', 'timber']:
                mass += base_area * feature_data['thickness'] * feature_data['density']
                soundproof_rating += feature_data['soundproof_rating']
            
            elif feature == 'coving':
                effective_area *= (1 - feature_data['area_reduction'])
                soundproof_rating += feature_data['soundproof_rating']
            
            elif feature == 'down_lights':
                num_lights = int(base_area / 4)  # One light per 4m²
                effective_area -= num_lights * feature_data['area_per_light']
                soundproof_rating += feature_data['soundproof_reduction']

        self.ceiling.update({
            'area': base_area,
            'effective_area': max(0, effective_area),
            'mass': mass,
            'soundproof_rating': max(0, soundproof_rating)
        })

    def add_floor_feature(self, feature_type):
        """Add a floor feature and recalculate properties"""
        if feature_type not in self.FLOOR_FEATURES:
            raise ValueError(f"Unknown floor feature: {feature_type}")
        
        if feature_type not in self.floor['features']:
            self.floor['features'].append(feature_type)
            self._recalculate_floor_properties()

    def _recalculate_floor_properties(self):
        """Recalculate floor properties based on features"""
        base_area = self.length * self.width
        effective_area = base_area
        soundproof_rating = 0

        for feature in self.floor['features']:
            feature_data = self.FLOOR_FEATURES[feature]
            
            # Calculate soundproof_rating effects
            soundproof_rating += feature_data['soundproof_rating']

        self.floor.update({
            'effective_area': max(0, effective_area),
            'soundproof_rating': max(0, soundproof_rating)
        })

    def get_ceiling_summary(self):
        """Get detailed ceiling information"""
        return {
            'area': self.ceiling['area'],
            'effective_area': self.ceiling['effective_area'],
            'features': self.ceiling['features'],
            'mass': self.ceiling['mass'],
            'soundproof_rating': self.ceiling['soundproof_rating']
        }

    def get_floor_summary(self):
        """Get detailed floor information"""
        return {
            'area': self.floor['area'],
            'effective_area': self.floor['effective_area'],
            'features': self.floor['features'],
            'soundproof_rating': self.floor['soundproof_rating']
        }

    def get_room_summary(self):
        """Get complete room summary including ceiling and floor details"""
        return {
            'dimensions': {
                'length': self.length,
                'width': self.width,
                'height': self.height
            },
            'areas': {
                'wall': self.calculate_wall_area(),
                'floor': self.length * self.width,
                'ceiling': self.get_ceiling_summary()
            },
            'blockages': {
                'windows': len([b for b in self.blockages if b['type'] == 'window']),
                'doors': len([b for b in self.blockages if b['type'] == 'door']),
                'vents': len([b for b in self.blockages if b['type'] == 'vent'])
            }
        }