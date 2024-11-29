print("Starting import...")
from solutions.room import Room
print("Import completed")

def test_room():
    print("Creating test room...")
    room = Room("Test Room", 5.0, 4.0, 3.0)
    print(f"Room created: {room.name}")
    print(f"Room dimensions: {room.length}x{room.width}x{room.height}")
    return room

if __name__ == "__main__":
    print("Running test...")
    room = test_room()
    print("Test completed")