from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB connection string
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/soundproofing')

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client.soundproofing

# Clear existing collections
db.solutions.drop()
db.materials.drop()

# Initialize wall solutions
wall_solutions = [
    {
        'name': 'Genie Clip wall (Standard)',
        'id': 'GenieClipWallStandard',
        'surface_type': 'wall',
        'sound_reduction': 50,
        'materials': [
            {'name': 'Genie Clip', 'cost': 3.4, 'coverage': 4, 'unit': 'm²'},
            {'name': 'Furring Channel', 'cost': 4.45, 'coverage': 2, 'unit': 'm²'},
            {'name': 'Rockwool RWA45 50mm', 'cost': 50.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': 'Resilient bars', 'cost': 4.2, 'coverage': 1, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 25, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 45
    },
    {
        'name': 'Genie Clip wall (SP15 Soundboard Upgrade)',
        'id': 'GenieClipWallSP15',
        'surface_type': 'wall',
        'sound_reduction': 55,
        'materials': [
            {'name': 'Genie Clip', 'cost': 3.4, 'coverage': 4, 'unit': 'm²'},
            {'name': 'Furring Channel', 'cost': 4.45, 'coverage': 2, 'unit': 'm²'},
            {'name': 'Rockwool RWA45 50mm', 'cost': 50.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': 'SP15 Soundboard', 'cost': 28.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Resilient bars', 'cost': 4.2, 'coverage': 1, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 25, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 50
    },
    {
        'name': 'M20 Solution (Standard)',
        'id': 'M20WallStandard',
        'surface_type': 'wall',
        'sound_reduction': 45,
        'materials': [
            {'name': 'Metal Frame Work', 'cost': 12.65, 'coverage': 1, 'unit': 'm²'},
            {'name': 'Rockwool RWA45 50mm', 'cost': 50.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Acoustic Sealant', 'cost': 12.35, 'coverage': 3, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 25, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 40
    },
    {
        'name': 'M20 Solution (SP15 Soundboard upgrade)',
        'id': 'M20WallSP15',
        'surface_type': 'wall',
        'sound_reduction': 50,
        'materials': [
            {'name': 'Metal Frame Work', 'cost': 12.65, 'coverage': 1, 'unit': 'm²'},
            {'name': 'Rockwool RWA45 50mm', 'cost': 50.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': 'SP15 Soundboard', 'cost': 28.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Acoustic Sealant', 'cost': 12.35, 'coverage': 3, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 25, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 45
    },
    {
        'name': 'Independent Wall (Standard)',
        'id': 'IndependentWallStandard',
        'surface_type': 'wall',
        'sound_reduction': 60,
        'materials': [
            {'name': 'Metal Frame Work', 'cost': 12.65, 'coverage': 1, 'unit': 'm²'},
            {'name': 'Rockwool RW3 100mm', 'cost': 65.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Acoustic Sealant', 'cost': 12.35, 'coverage': 3, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 30, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 50
    },
    {
        'name': 'Independent Wall (SP15 Soundboard Upgrade)',
        'id': 'IndependentWallSP15',
        'surface_type': 'wall',
        'sound_reduction': 65,
        'materials': [
            {'name': 'Metal Frame Work', 'cost': 12.65, 'coverage': 1, 'unit': 'm²'},
            {'name': 'Rockwool RW3 100mm', 'cost': 65.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': 'SP15 Soundboard', 'cost': 28.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Acoustic Sealant', 'cost': 12.35, 'coverage': 3, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 30, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 55
    },
    {
        'name': 'Resilient bar wall (Standard)',
        'id': 'ResilientBarWallStandard',
        'surface_type': 'wall',
        'sound_reduction': 48,
        'materials': [
            {'name': 'Resilient bars', 'cost': 4.2, 'coverage': 1, 'unit': 'm²'},
            {'name': 'Rockwool RWA45 50mm', 'cost': 50.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Acoustic Sealant', 'cost': 12.35, 'coverage': 3, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 25, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 40
    },
    {
        'name': 'Resilient bar wall (SP15 Soundboard Upgrade)',
        'id': 'ResilientBarWallSP15',
        'surface_type': 'wall',
        'sound_reduction': 53,
        'materials': [
            {'name': 'Resilient bars', 'cost': 4.2, 'coverage': 1, 'unit': 'm²'},
            {'name': 'Rockwool RWA45 50mm', 'cost': 50.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': 'SP15 Soundboard', 'cost': 28.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Acoustic Sealant', 'cost': 12.35, 'coverage': 3, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 25, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 45
    }
]

# Initialize ceiling solutions
ceiling_solutions = [
    {
        'name': 'Genie Clip ceiling',
        'id': 'GenieClipCeilingStandard',
        'surface_type': 'ceiling',
        'sound_reduction': 52,
        'materials': [
            {'name': 'Genie Clip', 'cost': 3.4, 'coverage': 4, 'unit': 'm²'},
            {'name': 'Furring Channel', 'cost': 4.45, 'coverage': 2, 'unit': 'm²'},
            {'name': 'Rockwool RWA45 50mm', 'cost': 50.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Acoustic Sealant', 'cost': 12.35, 'coverage': 3, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 30, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 50
    },
    {
        'name': 'Genie Clip ceiling (SP15 Soundboard Upgrade)',
        'id': 'GenieClipCeilingSP15',
        'surface_type': 'ceiling',
        'sound_reduction': 57,
        'materials': [
            {'name': 'Genie Clip', 'cost': 3.4, 'coverage': 4, 'unit': 'm²'},
            {'name': 'Furring Channel', 'cost': 4.45, 'coverage': 2, 'unit': 'm²'},
            {'name': 'Rockwool RWA45 50mm', 'cost': 50.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': 'SP15 Soundboard', 'cost': 28.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Acoustic Sealant', 'cost': 12.35, 'coverage': 3, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 30, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 55
    },
    {
        'name': 'Independent Ceiling',
        'id': 'IndependentCeilingStandard',
        'surface_type': 'ceiling',
        'sound_reduction': 62,
        'materials': [
            {'name': 'Metal Frame Work', 'cost': 12.65, 'coverage': 1, 'unit': 'm²'},
            {'name': 'Rockwool RW3 100mm', 'cost': 65.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Acoustic Sealant', 'cost': 12.35, 'coverage': 3, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 35, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 55
    },
    {
        'name': 'Independent Ceiling (SP15 Soundboard Upgrade)',
        'id': 'IndependentCeilingSP15',
        'surface_type': 'ceiling',
        'sound_reduction': 67,
        'materials': [
            {'name': 'Metal Frame Work', 'cost': 12.65, 'coverage': 1, 'unit': 'm²'},
            {'name': 'Rockwool RW3 100mm', 'cost': 65.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': 'SP15 Soundboard', 'cost': 28.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Acoustic Sealant', 'cost': 12.35, 'coverage': 3, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 35, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 60
    },
    {
        'name': 'Resilient bar Ceiling',
        'id': 'ResilientBarCeilingStandard',
        'surface_type': 'ceiling',
        'sound_reduction': 50,
        'materials': [
            {'name': 'Resilient bars', 'cost': 4.2, 'coverage': 1, 'unit': 'm²'},
            {'name': 'Rockwool RWA45 50mm', 'cost': 50.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Acoustic Sealant', 'cost': 12.35, 'coverage': 3, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 30, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 45
    },
    {
        'name': 'Resilient bar Ceiling (SP15 Soundboard Upgrade)',
        'id': 'ResilientBarCeilingSP15',
        'surface_type': 'ceiling',
        'sound_reduction': 55,
        'materials': [
            {'name': 'Resilient bars', 'cost': 4.2, 'coverage': 1, 'unit': 'm²'},
            {'name': 'Rockwool RWA45 50mm', 'cost': 50.2, 'coverage': 8.64, 'unit': 'm²'},
            {'name': 'SP15 Soundboard', 'cost': 28.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': '12.5mm Sound Plasterboard', 'cost': 18.45, 'coverage': 2.88, 'unit': 'm²'},
            {'name': 'Acoustic Sealant', 'cost': 12.35, 'coverage': 3, 'unit': 'm²'},
            {'name': 'Screws', 'cost': 16.21, 'coverage': 30, 'unit': 'box'},
            {'name': 'Floor protection', 'cost': 30, 'coverage': 30, 'unit': 'm²'}
        ],
        'labor_rate': 50
    }
]

# Insert solutions into database
db.solutions.insert_many(wall_solutions + ceiling_solutions)

print(f"Initialized database with {len(wall_solutions)} wall solutions and {len(ceiling_solutions)} ceiling solutions") 