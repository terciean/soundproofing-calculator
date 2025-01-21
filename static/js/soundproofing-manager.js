if (!window.SoundproofingManager) {
    class SoundproofingManager {
        constructor() {
            this.initialized = false;
            this.solutions = {
                wall: {
                    standard: ['StandardWallSP10', 'StandardWallSP20', 'StandardWallSP30'],
                    premium: ['PremiumWallSP10', 'PremiumWallSP15', 'PremiumWallSP20', 'PremiumWallSP25', 'PremiumWallSP30']
                },
                ceiling: {
                    standard: ['StandardCeilingSP10', 'StandardCeilingSP20', 'StandardCeilingSP30', 'StandardCeilingSP40'],
                    premium: ['PremiumCeilingSP10', 'PremiumCeilingSP20', 'PremiumCeilingSP30', 'PremiumCeilingSP40']
                },
                floor: {
                    standard: [],
                    premium: [],
                    message: 'Floor solutions require custom assessment. Please contact our specialists for a detailed quote.',
                    contactInfo: {
                        phone: '+44 (0)1234 567890',
                        email: 'info@soundproofing.com'
                    }
                }
            };
            
            // Add live update tracking
            this.lastUpdate = null;
            this.updateDebounceTime = 300; // ms

            // Add specifications for all solutions
            this.solutionCharacteristics = {
                'StandardWallSP10': {  // Was 'M20 Solution (Standard)'
                    soundReduction: 45,
                    frequencyRange: [125, 4000],
                    materials: [
                        {name: 'M20 Rubber wall panel', cost: 23.95, coverage: '1'},
                        {name: 'M20 adhesive', cost: 5.95, coverage: '1'},
                        {name: 'Acoustic Mastic', cost: 12.35, coverage: '2'},
                        {name: '12.5mm Sound plasterboard', cost: 18.45, coverage: '2.88'}
                    ],
                    total_cost: 60.7,
                    thickness: 0.10,
                    installationTime: 1,
                    maintenanceRequired: 'low',
                    durability: 0.9,
                    impactResistance: 0.7,
                    stc_rating: 45,
                    displayName: 'Standard Wall SP10',
                    notes: ['Single layer system with excellent cost-effectiveness']
                },
                'StandardWallSP20': {  // Was 'Independent Wall (Standard)'
                    soundReduction: 50,
                    frequencyRange: [90, 4500],
                    materials: [
                        {name: 'Metal Frame Work', cost: 12.65, coverage: '1'},
                        {name: 'Rockwool RWA45 50mm', cost: 50.2, coverage: '8.64'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Tecsound 50', cost: 59.5, coverage: '7.2'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 241.2,
                    thickness: 0.15,
                    installationTime: 2,
                    maintenanceRequired: 'medium',
                    durability: 0.95,
                    impactResistance: 0.85,
                    stc_rating: 50,
                    displayName: 'Standard Wall SP20',
                    notes: ['Two layers of 12.5mm Sound Plasterboard.']
                },
                'StandardWallSP30': {  // Was 'Resilient bar wall (Standard)'
                    soundReduction: 48,
                    frequencyRange: [100, 4000],
                    materials: [
                        {name: 'Rockwool RW3 100mm', cost: 42.95, coverage: '2.88'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: '12.5mm Sound plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Floor protection', cost: 30, coverage: '30'},
                        {name: 'Screws', cost: 16.21, coverage: '30'}
                    ],
                    total_cost: 124.16,
                    thickness: 0.12,
                    installationTime: 1.5,
                    maintenanceRequired: 'low',
                    durability: 0.88,
                    impactResistance: 0.75,
                    stc_rating: 48,
                    displayName: 'Standard Wall SP30',
                    notes: ['Single layer system with resilient bars for decoupling']
                },
                'PremiumWallSP10': {  // Was 'Genie Clip wall (Standard)'
                    soundReduction: 52,
                    frequencyRange: [80, 5000],
                    materials: [
                        {name: 'Genie Clip', cost: 3.4, coverage: '4'},
                        {name: 'Furring Channel', cost: 4.45, coverage: '2'},
                        {name: 'Rockwool RWA45 50mm', cost: 50.2, coverage: '8.64'},
                        {name: 'Resilient bars', cost: 4.2, coverage: '1'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 25, coverage: '30'}
                    ],
                    total_cost: 159.55,
                    thickness: 0.13,
                    installationTime: 2,
                    maintenanceRequired: 'medium',
                    durability: 0.92,
                    impactResistance: 0.8,
                    stc_rating: 52,
                    displayName: 'Premium Wall SP10',
                    notes: ['2 layers of 12.5mm plasterboard for this system.', 'Add 1 box of screws no matter the m².']
                },
                'PremiumWallSP15': {  // Was 'M20 Solution (SP15 Soundboard upgrade)'
                    soundReduction: 56,
                    frequencyRange: [70, 5500],
                    materials: [
                        {name: 'M20 Rubber wall panel', cost: 23.95, coverage: '1'},
                        {name: 'M20 adhesive', cost: 5.95, coverage: '1'},
                        {name: 'Acoustic Mastic', cost: 12.35, coverage: '2'},
                        {name: 'SP15 Soundboard', cost: 26.95, coverage: '0.96'},
                        {name: '12.5mm Sound plasterboard', cost: 18.45, coverage: '2.88'}
                    ],
                    total_cost: 93.65,
                    thickness: 0.125,
                    installationTime: 1.5,
                    maintenanceRequired: 'low',
                    durability: 0.92,
                    impactResistance: 0.75,
                    stc_rating: 56,
                    displayName: 'Premium Wall SP15',
                    notes: ['We only use 1 layer of plasterboard on this system.']
                },
                'PremiumWallSP20': {  // Was 'Independent Wall (SP15 Soundboard Upgrade)'
                    soundReduction: 55,
                    frequencyRange: [63, 8000],
                    materials: [
                        {name: 'Metal Frame Work', cost: 12.65, coverage: '1'},
                        {name: 'Rockwool RWA45 50mm', cost: 50.2, coverage: '8.64'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'SP15 Soundboard', cost: 22.95, coverage: '1'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Tecsound 50', cost: 59.5, coverage: '7.2'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 264.15,
                    thickness: 0.175,
                    installationTime: 2.5,
                    maintenanceRequired: 'medium',
                    durability: 0.96,
                    impactResistance: 0.9,
                    stc_rating: 55,
                    displayName: 'Premium Wall SP20',
                    notes: ['Only one layer of 12.5mm sound plasterboard.']
                },
                'PremiumWallSP25': {  // Was 'Resilient bar wall (SP15 Soundboard Upgrade)'
                    soundReduction: 53,
                    frequencyRange: [85, 4500],
                    materials: [
                        {name: 'Rockwool RW3 100mm', cost: 42.95, coverage: '2.88'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: 'SP15 Soundboard', cost: 22.95, coverage: '1'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 147.11,
                    thickness: 0.145,
                    installationTime: 2,
                    maintenanceRequired: 'medium',
                    durability: 0.9,
                    impactResistance: 0.8,
                    stc_rating: 53,
                    displayName: 'Premium Wall SP25',
                    notes: ['1 layer of 12.5mm Sound Plasterboard']
                },
                'PremiumWallSP30': {  // Was 'Genie Clip wall (SP15 Soundboard Upgrade)'
                    soundReduction: 58,
                    frequencyRange: [63, 6000],
                    materials: [
                        {name: 'Genie Clip', cost: 3.4, coverage: '0.25'},
                        {name: 'Furring Channel', cost: 4.45, coverage: '0.5'},
                        {name: 'Rockwool RWA45 50mm', cost: 50.2, coverage: '8.64'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'SP15 Soundboard', cost: 22.95, coverage: '1'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 199.85,
                    thickness: 0.155,
                    installationTime: 2.5,
                    maintenanceRequired: 'medium',
                    durability: 0.94,
                    impactResistance: 0.85,
                    stc_rating: 58,
                    displayName: 'Premium Wall SP30',
                    notes: ['Only 1 layer of 12.5mm plasterboard on this system.']
                },
                'StandardCeilingSP10': {  // Was 'Genie Clip ceiling'
                    soundReduction: 52,
                    frequencyRange: [80, 5000],
                    materials: [
                        {name: 'Genie Clip', cost: 3.4, coverage: '0.25'},
                        {name: 'Furring Channel', cost: 4.45, coverage: '0.50'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: 'Rockwool RWA45 50mm', cost: 50.2, coverage: '8.64'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 139.26,
                    thickness: 0.14,
                    installationTime: 2,
                    maintenanceRequired: 'medium',
                    durability: 0.9,
                    impactResistance: 0.85,
                    stc_rating: 52,
                    displayName: 'Standard Ceiling SP10',
                    notes: ['2 layers of 12.5mm sound plasterboard.']
                },
                'StandardCeilingSP20': {  // Was 'LB3 Genie Clip'
                    soundReduction: 54,
                    frequencyRange: [75, 5200],
                    materials: [
                        {name: 'LB3 Genie Clip', cost: 6.2, coverage: '0.25'},
                        {name: 'Furring Channel', cost: 4.45, coverage: '0.50'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: 'Rockwool RW3 100mm', cost: 42.95, coverage: '2.88'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 134.81,
                    thickness: 0.15,
                    installationTime: 2,
                    maintenanceRequired: 'medium',
                    durability: 0.92,
                    impactResistance: 0.88,
                    stc_rating: 54,
                    displayName: 'Standard Ceiling SP20',
                    notes: ['2 layers of 12.5mm Sound Plasterboard']
                },
                'PremiumCeilingSP10': {  // Was 'Independent Ceiling'
                    soundReduction: 50,
                    frequencyRange: [90, 4500],
                    materials: [
                        {name: 'Timber and fixings', cost: 35, coverage: '1'},
                        {name: 'Rockwool RW3 100mm', cost: 42.95, coverage: '2.88'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: '19mm Plank Plasterboard', cost: 15.5, coverage: '1.44'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 174.66,
                    thickness: 0.16,
                    installationTime: 2.5,
                    maintenanceRequired: 'medium',
                    durability: 0.95,
                    impactResistance: 0.9,
                    stc_rating: 50,
                    displayName: 'Premium Ceiling SP10',
                    notes: ['Uses both 19mm plank and 12.5mm sound plasterboard']
                },
                'PremiumCeilingSP20': {  // Was 'Resilient bar Ceiling'
                    soundReduction: 48,
                    frequencyRange: [100, 4000],
                    materials: [
                        {name: 'Rockwool RW3 100mm', cost: 42.95, coverage: '2.88'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 124.16,
                    thickness: 0.13,
                    installationTime: 1.5,
                    maintenanceRequired: 'low',
                    durability: 0.88,
                    impactResistance: 0.8,
                    stc_rating: 48,
                    displayName: 'Premium Ceiling SP20',
                    notes: ['Basic but effective ceiling solution']
                },
                'StandardCeilingSP30': {  // Was 'Genie Clip ceiling (SP15 Soundboard Upgrade)'
                    soundReduction: 56,
                    frequencyRange: [70, 5500],
                    materials: [
                        {name: 'Genie Clip', cost: 3.4, coverage: '0.25'},
                        {name: 'Furring Channel', cost: 4.45, coverage: '0.50'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: 'Rockwool RWA45 50mm', cost: 50.2, coverage: '8.64'},
                        {name: 'SP15 Soundboard', cost: 22.95, coverage: '1'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 162.21,
                    thickness: 0.165,
                    installationTime: 2.5,
                    maintenanceRequired: 'medium',
                    durability: 0.92,
                    impactResistance: 0.87,
                    stc_rating: 56,
                    displayName: 'Standard Ceiling SP30',
                    notes: ['One layer of 12.5mm plasterboard with SP15 upgrade']
                },
                'StandardCeilingSP40': {  // Was 'LB3 Genie Clip (SP15 Soundboard Upgrade)'
                    soundReduction: 58,
                    frequencyRange: [65, 5800],
                    materials: [
                        {name: 'LB3 Genie Clip', cost: 6.2, coverage: '0.25'},
                        {name: 'Furring Channel', cost: 4.45, coverage: '0.50'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: 'Rockwool RW3 100mm', cost: 42.95, coverage: '2.88'},
                        {name: 'SP15 Soundboard', cost: 22.95, coverage: '1'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 157.76,
                    thickness: 0.175,
                    installationTime: 2.5,
                    maintenanceRequired: 'medium',
                    durability: 0.94,
                    impactResistance: 0.9,
                    stc_rating: 58,
                    displayName: 'Standard Ceiling SP40',
                    notes: ['1 layer of 12.5mm Sound Plasterboard with enhanced LB3 system']
                },
                'PremiumCeilingSP30': {  // Was 'Independent Ceiling (SP15 Soundboard Upgrade)'
                    soundReduction: 55,
                    frequencyRange: [80, 5000],
                    materials: [
                        {name: 'Timber and fixings', cost: 35, coverage: '1'},
                        {name: 'Rockwool RW3 100mm', cost: 42.95, coverage: '2.88'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: 'SP15 Soundboard', cost: 22.95, coverage: '1'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 182.11,
                    thickness: 0.185,
                    installationTime: 3,
                    maintenanceRequired: 'medium',
                    durability: 0.96,
                    impactResistance: 0.92,
                    stc_rating: 55,
                    displayName: 'Premium Ceiling SP30',
                    notes: ['Enhanced independent system with SP15 upgrade']
                },
                'PremiumCeilingSP40': {  // Was 'Resilient bar Ceiling (SP15 Soundboard Upgrade)'
                    soundReduction: 53,
                    frequencyRange: [85, 4500],
                    materials: [
                        {name: 'Rockwool RW3 100mm', cost: 42.95, coverage: '2.88'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: 'SP15 Soundboard', cost: 22.95, coverage: '1'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 147.11,
                    thickness: 0.155,
                    installationTime: 2,
                    maintenanceRequired: 'medium',
                    durability: 0.9,
                    impactResistance: 0.85,
                    stc_rating: 53,
                    displayName: 'Premium Ceiling SP40',
                    notes: ['Enhanced resilient bar system with SP15 upgrade']
                }
            };

            // Add noise assessment parameters
            this.noiseAssessment = {
                sourceDetails: {
                    noiseType: null,  // e.g., 'speech', 'music', 'tv', etc.
                    occurrence: {
                        timeOfDay: [],  // ['morning', 'afternoon', 'evening', 'night']
                        frequency: null, // 'constant', 'intermittent', 'occasional'
                        duration: null   // 'brief', 'moderate', 'extended'
                    },
                    location: {
                        direction: [], // ['north', 'south', 'east', 'west', 'ceiling', 'floor']
                        proximity: null // 'adjacent', 'above', 'below', 'distant'
                    },
                    characteristics: {
                        perceived_intensity: null, // 'barely_noticeable', 'noticeable', 'very_noticeable', 'intrusive'
                        bass_content: false,
                        vibration: false,
                        impact_noise: false
                    }
                },
                roomDetails: {
                    usage: null,  // 'bedroom', 'living_room', 'office', 'studio', etc.
                    dimensions: {
                        length: 0,
                        width: 0,
                        height: 0
                    },
                    existing_construction: {
                        wall_type: null,    // 'standard_drywall', 'brick', 'concrete', etc.
                        ceiling_type: null,  // 'standard_ceiling', 'concrete', etc.
                        floor_type: null     // 'wooden', 'concrete', etc.
                    },
                    existing_treatment: {
                        walls: false,
                        ceiling: false,
                        floor: false,
                        description: ''
                    }
                },
                problemAssessment: {
                    primary_concern: null,  // 'privacy', 'concentration', 'sleep', 'recording'
                    impact_level: {
                        conversation_privacy: 0,  // 0-5 scale
                        sleep_disturbance: 0,    // 0-5 scale
                        vibration_felt: 0,       // 0-5 scale
                        concentration_impact: 0   // 0-5 scale
                    },
                    specific_triggers: [],  // Array of specific activities/times when noise is worst
                    noise_description: ''   // Client's description of the noise problem
                }
            };

            // Add noise type characteristics for all types
            this.noiseCharacteristics = {
                'speech': {
                    frequencyRange: [125, 8000],
                    typicalIntensity: 60,
                    impactComponent: false,
                    airborneComponent: true,
                    variability: 'medium'
                },
                'music': {
                    frequencyRange: [20, 20000],
                    typicalIntensity: 85,
                    impactComponent: true,
                    airborneComponent: true,
                    variability: 'high',
                    bassHeavy: true
                },
                'tv': {
                    frequencyRange: [80, 12000],
                    typicalIntensity: 70,
                    impactComponent: false,
                    airborneComponent: true,
                    variability: 'medium'
                },
                'traffic': {
                    frequencyRange: [30, 5000],
                    typicalIntensity: 75,
                    impactComponent: false,
                    airborneComponent: true,
                    variability: 'high'
                },
                'aircraft': {
                    frequencyRange: [20, 8000],
                    typicalIntensity: 90,
                    impactComponent: false,
                    airborneComponent: true,
                    variability: 'very-high'
                },
                'footsteps': {
                    frequencyRange: [40, 2000],
                    typicalIntensity: 65,
                    impactComponent: true,
                    airborneComponent: false,
                    variability: 'medium'
                },
                'machinery': {
                    frequencyRange: [20, 15000],
                    typicalIntensity: 80,
                    impactComponent: true,
                    airborneComponent: true,
                    variability: 'high'
                }
            };

            // Add event listeners for dynamic updates
            this.bindDynamicUpdates();

            // Add cache for recommendations
            this.recommendationsCache = new Map();
            this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
            
            // Add debounce settings
            this.updateDebounceTime = 300; // ms
            this.updateTimeout = null;
            this.lastUpdate = null;

            // Add memoization cache
            this.evaluationCache = new Map();
            this.frequencyMatchCache = new Map();
            
            // Refined weights for different noise types
            this.noiseTypeWeights = {
                'music': {
                    lowFrequency: 0.4,
                    midFrequency: 0.3,
                    highFrequency: 0.3,
                    impact: 0.6,
                    airborne: 0.4
                },
                'speech': {
                    lowFrequency: 0.2,
                    midFrequency: 0.5,
                    highFrequency: 0.3,
                    impact: 0.3,
                    airborne: 0.7
                },
                'traffic': {
                    lowFrequency: 0.5,
                    midFrequency: 0.3,
                    highFrequency: 0.2,
                    impact: 0.2,
                    airborne: 0.8
                },
                'footsteps': {
                    lowFrequency: 0.3,
                    midFrequency: 0.4,
                    highFrequency: 0.3,
                    impact: 0.8,
                    airborne: 0.2
                },
                'machinery': {
                    lowFrequency: 0.4,
                    midFrequency: 0.4,
                    highFrequency: 0.2,
                    impact: 0.5,
                    airborne: 0.5
                }
            };
        }

        async initialize() {
            try {
                // Load solution characteristics
                try {
                    const response = await fetch('/api/solutions');
                    if (!response.ok) {
                        throw new Error('Failed to load solution characteristics');
                    }
                    this.solutionCharacteristics = await response.json();
                } catch (error) {
                    console.warn('Failed to load from API, using fallback data:', error);
                    // Fallback solution characteristics
                    this.solutionCharacteristics = {
                        'SP10': {
                            displayName: 'Standard Wall SP10',
                            soundReduction: 45,
                            frequencyRange: [125, 4000],
                            installationTime: 2,
                            maintenanceRequired: 'Low',
                            durability: 0.8,
                            materials: [
                                {
                                    name: 'Acoustic Panel',
                                    coverage: 1,
                                    cost: 45,
                                    unit: 'm²'
                                },
                                {
                                    name: 'Mounting Hardware',
                                    coverage: 1,
                                    cost: 10,
                                    unit: 'm²'
                                },
                                {
                                    name: 'Acoustic Sealant',
                                    coverage: 3,
                                    cost: 12,
                                    unit: 'm²'
                                }
                            ],
                            total_cost: 67,
                            stc_rating: 45,
                            notes: [
                                'Single layer system with excellent cost-effectiveness',
                                'Easy installation process',
                                'Minimal space requirements'
                            ]
                        },
                        'SP20': {
                            displayName: 'Premium Wall SP20',
                            soundReduction: 55,
                            frequencyRange: [63, 8000],
                            installationTime: 3,
                            maintenanceRequired: 'Medium',
                            durability: 0.9,
                            materials: [
                                {
                                    name: 'Premium Acoustic Panel',
                                    coverage: 1,
                                    cost: 75,
                                    unit: 'm²'
                                },
                                {
                                    name: 'Isolation Mounts',
                                    coverage: 1,
                                    cost: 25,
                                    unit: 'm²'
                                },
                                {
                                    name: 'Dampening Material',
                                    coverage: 1,
                                    cost: 20,
                                    unit: 'm²'
                                },
                                {
                                    name: 'Acoustic Sealant',
                                    coverage: 3,
                                    cost: 15,
                                    unit: 'm²'
                                }
                            ],
                            total_cost: 135,
                            stc_rating: 55,
                            notes: [
                                'Double layer system for maximum sound isolation',
                                'Professional grade materials',
                                'Enhanced low frequency performance'
                            ]
                        }
                    };
                }

                // Initialize solution categories
                this.solutions = {
                    wall: {
                        standard: ['SP10'],
                        premium: ['SP20']
                    },
                    ceiling: {
                        standard: ['SP10'],
                        premium: ['SP20']
                    },
                    floor: {
                        standard: ['SP10'],
                        premium: ['SP20']
                    }
                };

                console.log('Loaded solution characteristics:', this.solutionCharacteristics);
                this.bindDynamicUpdates();
                
            } catch (error) {
                console.error('Error initializing SoundproofingManager:', error);
            }
        }

        bindEvents() {
            // Listen for all relevant form changes
            this.bindNoiseInputs();
            this.bindDimensionInputs();
            this.bindBlockageUpdates();
        }

        bindNoiseInputs() {
            // Enhanced noise type changes
            const noiseTypeSelect = document.getElementById('noise-type');
            if (noiseTypeSelect) {
                noiseTypeSelect.addEventListener('change', (e) => {
                    this.noiseAssessment.sourceDetails.noiseType = e.target.value;
                    this.handleFormUpdate('noise-type');
                });
            }

            // Bind occurrence inputs
            document.querySelectorAll('input[name="noise-time"]').forEach(checkbox => {
                checkbox.addEventListener('change', (e) => {
                    const timeOfDay = e.target.value;
                    if (e.target.checked) {
                        this.noiseAssessment.sourceDetails.occurrence.timeOfDay.push(timeOfDay);
                    } else {
                        const index = this.noiseAssessment.sourceDetails.occurrence.timeOfDay.indexOf(timeOfDay);
                        if (index > -1) {
                            this.noiseAssessment.sourceDetails.occurrence.timeOfDay.splice(index, 1);
                        }
                    }
                    this.handleFormUpdate('time');
                });
            });

            // Bind direction inputs
            document.querySelectorAll('input[name="noise-direction"]').forEach(checkbox => {
                checkbox.addEventListener('change', (e) => {
                    const direction = e.target.value;
                    if (e.target.checked) {
                        this.noiseAssessment.sourceDetails.location.direction.push(direction);
                    } else {
                        const index = this.noiseAssessment.sourceDetails.location.direction.indexOf(direction);
                        if (index > -1) {
                            this.noiseAssessment.sourceDetails.location.direction.splice(index, 1);
                        }
                    }
                    this.handleFormUpdate('direction');
                });
            });

            // Bind characteristics inputs
            const intensitySelect = document.getElementById('perceived-intensity');
            if (intensitySelect) {
                intensitySelect.addEventListener('change', (e) => {
                    this.noiseAssessment.sourceDetails.characteristics.perceived_intensity = e.target.value;
                    this.handleFormUpdate('intensity');
                });
            }

            // Bind problem assessment inputs
            const impactInputs = document.querySelectorAll('.impact-level-input');
            impactInputs.forEach(input => {
                input.addEventListener('change', (e) => {
                    this.noiseAssessment.problemAssessment.impact_level[e.target.name] = parseInt(e.target.value);
                    this.handleFormUpdate('impact');
                });
            });
        }

        bindDimensionInputs() {
            ['length', 'width', 'height'].forEach(dim => {
                const input = document.getElementById(dim);
                if (input) {
                    input.addEventListener('input', () => {
                        const dimensions = {
                            length: parseFloat(document.getElementById('length')?.value || 0),
                            width: parseFloat(document.getElementById('width')?.value || 0),
                            height: parseFloat(document.getElementById('height')?.value || 0)
                        };
                        this.updateAreaDisplays(dimensions);
                        this.handleFormUpdate('dimensions');
                    });
                }
            });
        }

        bindBlockageUpdates() {
            window.addEventListener('blockagesUpdated', () => this.handleFormUpdate('blockages'));
        }

        handleFormUpdate(type) {
            const now = Date.now();
            if (this.lastUpdate && (now - this.lastUpdate) < this.updateDebounceTime) {
                clearTimeout(this.updateTimeout);
            }

            this.lastUpdate = now;
            this.updateTimeout = setTimeout(() => {
                // Only update recommendations if we have noise data
                if (type === 'dimensions') {
                    // Just update area displays for dimension changes
                    const dimensions = {
                        length: parseFloat(document.getElementById('length')?.value || 0),
                        width: parseFloat(document.getElementById('width')?.value || 0),
                        height: parseFloat(document.getElementById('height')?.value || 0)
                    };
                    this.updateAreaDisplays(dimensions);
                    
                    // Only proceed with recommendation update if we have noise data
                    if (window.FormState?.noiseData?.type && 
                        window.FormState.noiseData.direction?.length > 0) {
                this.updateRecommendations(type);
                    }
                } else {
                    this.updateRecommendations(type);
                }
            }, this.updateDebounceTime);
        }

        async updateRecommendations(triggerType) {
            try {
                console.log('Generating new recommendations');
                console.log('Current Form State:', window.FormState);
                
                // Get noise surfaces
                const noiseSurfaces = this.getNoiseSourceSurfaces();
                if (!noiseSurfaces || !noiseSurfaces.walls) {
                    console.warn('No noise surfaces found');
                    return;
                }

                // Get current form state
                const currentState = {
                    noiseData: window.FormState?.noiseData || {},
                    dimensions: window.FormState?.dimensions || {},
                    blockages: window.FormState?.blockages || {},
                    roomType: window.FormState?.roomType || 'standard',
                    surfaceFeatures: window.FormState?.surfaces || {}
                };

                console.log('Processing state:', currentState);

                // Generate primary solutions
                const primarySolutions = await this.getPrimarySolutions(
                    currentState.noiseData,
                    noiseSurfaces,
                    this.calculateOverallPriority(currentState.noiseData)
                );

                if (!primarySolutions) {
                    throw new Error('Failed to generate primary solutions');
                }

                // Calculate effectiveness
                const effectiveness = this.calculateEffectiveness([primarySolutions]);

                // Generate recommendations object
                const recommendations = {
                    primary: primarySolutions,
                    alternatives: [],  // You can add alternative solutions here if needed
                    effectiveness: effectiveness
                };

                console.log('Generated recommendations:', recommendations);

                // Display the recommendations
                await this.displayRecommendations(recommendations);

            } catch (error) {
                console.error('Error updating recommendations:', error);
                this.handleRecommendationError(error, triggerType);
            }
        }

        calculateEffectiveness(solutions) {
            if (!Array.isArray(solutions) || solutions.length === 0) {
                console.warn('No solutions provided or solutions is not an array');
                return [];
            }

            return solutions.map(solution => {
                try {
                    const weights = {
                        acousticPerformance: 0.35,
                        frequencyMatch: 0.25,
                        costEfficiency: 0.20,
                        installationFeasibility: 0.20
                    };

                    let scores = {
                        acousticPerformance: 0,
                        frequencyMatch: 0,
                        costEfficiency: 0,
                        installationFeasibility: 0
                    };

                    // Ensure solution.walls exists and is an array
                    if (!solution.walls || !Array.isArray(solution.walls)) {
                        console.warn('Invalid solution structure:', solution);
                        return {
                            overall: 0,
                            breakdown: scores
                        };
                    }

                    // Calculate scores for each wall solution
                    solution.walls.forEach(wall => {
                        if (!wall.solution) return;
                        
                        const specs = this.solutionCharacteristics[wall.solution];
                        if (!specs) return;

                        scores.acousticPerformance += specs.soundReduction / 70;
                        scores.costEfficiency += 1 - (specs.total_cost / 250);
                        scores.installationFeasibility += specs.durability;
                    });

                    // Average the scores
                    Object.keys(scores).forEach(key => {
                        scores[key] = scores[key] / solution.walls.length;
                    });

                    // Calculate weighted total
                    const effectiveness = Object.entries(weights).reduce((total, [key, weight]) => {
                        return total + (scores[key] * weight);
                    }, 0);

                    return {
                        overall: effectiveness,
                        breakdown: scores
                    };
                } catch (error) {
                    console.error('Error calculating individual solution effectiveness:', error);
                    return {
                        overall: 0,
                        breakdown: scores
                    };
                }
            });
        }

        validateInputs(noiseData) {
            const errors = [];
            
            if (!noiseData) {
                errors.push('Noise data is required');
            } else {
                if (!noiseData.type) errors.push('Noise type is required');
                if (!noiseData.intensity) errors.push('Noise intensity is required');
                if (!Array.isArray(noiseData.direction) || noiseData.direction.length === 0) {
                    errors.push('At least one noise direction is required');
                }
            }
            
            if (errors.length > 0) {
                throw new Error('Validation failed: ' + errors.join(', '));
            }
        }

        getErrorMessage(error) {
            // Convert technical errors to user-friendly messages
            const errorMessages = {
                'Validation failed': 'Please fill in all required noise information.',
                'Failed to generate primary solutions': 'Unable to generate recommendations. Please try again.',
                'Network error': 'Connection problem. Please check your internet connection.'
            };

            for (const [technical, friendly] of Object.entries(errorMessages)) {
                if (error.message.includes(technical)) return friendly;
            }

            return 'An unexpected error occurred. Please try again.';
        }

        async retryUpdate(triggerType) {
            // Clear cache for this update
            const currentState = {
                noiseData: window.FormState.noiseData,
                dimensions: window.FormState.dimensions,
                blockages: window.FormState.blockages,
                roomType: window.FormState.roomType,
                surfaceFeatures: window.FormState.surfaces
            };
            const cacheKey = JSON.stringify(currentState);
            this.recommendationsCache.delete(cacheKey);

            // Retry update
            await this.updateRecommendations(triggerType);
        }

        calculateOverallPriority(noiseData) {
            let priorityScore = 0;

            // Ensure noiseSurfaces is defined
            const noiseSurfaces = this.getNoiseSourceSurfaces(); // Add this line to initialize noiseSurfaces

            // Noise type priority
            const noiseTypePriorities = {
                'music': 5,
                'machinery': 5,
                'traffic': 4,
                'aircraft': 5,
                'speech': 3,
                'tv': 3,
                'footsteps': 4
            };

            // Calculate priority based on noise data
            if (noiseData.type && noiseTypePriorities[noiseData.type]) {
                priorityScore += noiseTypePriorities[noiseData.type];
            }

            // Additional calculations based on noiseSurfaces can be added here

            return priorityScore; // Return the calculated priority score
        }

        async findBestSolution(availableSolutions, noiseData, type, wall = null) {
            let bestScore = 0;
            let bestSolution = null;
            let bestReasoning = [];

            for (const solution of availableSolutions) {
                const score = await this.evaluateSolution(solution, noiseData, type);
                if (score > bestScore) {
                    bestScore = score;
                    bestSolution = solution;
                    bestReasoning = this.generateSolutionReasoning(solution, noiseData, type);
                }
            }

            if (bestSolution) {
                return {
                    wall: wall,
                    solution: bestSolution,
                    score: bestScore,
                    reasoning: bestReasoning
                };
            }

            return null;
        }

        async evaluateSolution(solution, noiseData, type) {
            try {
                // Create cache key
                const cacheKey = JSON.stringify({ solution, noiseData, type });
                
                // Check cache
                const cachedResult = this.evaluationCache.get(cacheKey);
                if (cachedResult) {
                    return cachedResult;
                }

                // Get solution specifications
                const specs = this.solutionCharacteristics[solution];
                const noiseSpecs = this.noiseCharacteristics[noiseData.type];
                
                if (!specs || !noiseSpecs) {
                    throw new Error('Invalid solution or noise type');
                }

                // Get weights for this noise type
                const weights = this.noiseTypeWeights[noiseData.type] || this.noiseTypeWeights['speech'];

                // Calculate detailed scores
                const scores = {
                    frequencyMatch: this.calculateFrequencyMatch(specs.frequencyRange, noiseSpecs.frequencyRange, weights),
                    soundReduction: this.calculateSoundReduction(specs.soundReduction, noiseSpecs.typicalIntensity, noiseData.intensity),
                    impactResistance: noiseSpecs.impactComponent ? specs.impactResistance * weights.impact : 1,
                    airborneReduction: noiseSpecs.airborneComponent ? (specs.soundReduction / 70) * weights.airborne : 1
                };

                // Calculate overall score with weighted average
                const overallScore = (
                    scores.frequencyMatch * 0.35 +
                    scores.soundReduction * 0.35 +
                    scores.impactResistance * 0.15 +
                    scores.airborneReduction * 0.15
                );

                const result = {
                    score: overallScore,
                    details: scores,
                    reasoning: this.generateSolutionReasoning(solution, specs, noiseData)
                };

                // Cache the result
                this.evaluationCache.set(cacheKey, result);

                return result;

            } catch (error) {
                console.error('Error evaluating solution:', error);
                return {
                    score: 0,
                    details: {},
                    reasoning: ['Error evaluating solution']
                };
            }
        }

        calculateFrequencyMatch(solutionRange, noiseRange, weights) {
            try {
                // Create cache key
                const cacheKey = JSON.stringify({ solutionRange, noiseRange });
                
                // Check cache
                const cachedResult = this.frequencyMatchCache.get(cacheKey);
                if (cachedResult) {
                    return cachedResult;
                }

                // Define frequency bands
                const bands = {
                    low: { min: 20, max: 250 },
                    mid: { min: 250, max: 2000 },
                    high: { min: 2000, max: 20000 }
                };

                // Calculate coverage for each band
                const coverage = {
                    low: this.calculateBandCoverage(solutionRange, noiseRange, bands.low),
                    mid: this.calculateBandCoverage(solutionRange, noiseRange, bands.mid),
                    high: this.calculateBandCoverage(solutionRange, noiseRange, bands.high)
                };

                // Calculate weighted score
                const score = 
                    coverage.low * weights.lowFrequency +
                    coverage.mid * weights.midFrequency +
                    coverage.high * weights.highFrequency;

                // Cache the result
                this.frequencyMatchCache.set(cacheKey, score);

                return score;

            } catch (error) {
                console.error('Error calculating frequency match:', error);
                return 0;
            }
        }

        calculateBandCoverage(solutionRange, noiseRange, band) {
            const bandWidth = band.max - band.min;
            
            // Calculate overlap within this band
            const overlapStart = Math.max(
                band.min,
                Math.max(solutionRange[0], noiseRange[0])
            );
            const overlapEnd = Math.min(
                band.max,
                Math.min(solutionRange[1], noiseRange[1])
            );
            
            if (overlapEnd <= overlapStart) return 0;
            
            const overlap = overlapEnd - overlapStart;
            return Math.min(overlap / bandWidth, 1);
        }

        calculateSoundReduction(solutionReduction, typicalIntensity, reportedIntensity) {
            const requiredReduction = (typicalIntensity * (reportedIntensity / 3)) - 35; // Target 35dB ambient
            return Math.min(solutionReduction / requiredReduction, 1);
        }

        calculateDetailedWeights(noiseData, type) {
            const weights = {
                soundReduction: 0.25,
                frequencyMatch: 0.20,
                stcRating: 0.15,
                installation: 0.10,
                maintenance: 0.10,
                cost: 0.20
            };

            // Adjust based on noise type
            if (noiseData.type === 'music' || noiseData.type === 'machinery') {
                weights.frequencyMatch += 0.1;
                weights.soundReduction += 0.05;
                weights.cost -= 0.15;
            }

            // Adjust based on intensity
            if (parseInt(noiseData.intensity) >= 4) {
                weights.soundReduction += 0.1;
                weights.stcRating += 0.05;
                weights.cost -= 0.15;
            }

            // Adjust based on time of day
            if (noiseData.time?.includes('night')) {
                weights.soundReduction += 0.15;
                weights.cost -= 0.15;
            }

            // Adjust based on room usage
            if (this.noiseAssessment.roomDetails.usage === 'studio') {
                weights.frequencyMatch += 0.15;
                weights.soundReduction += 0.1;
                weights.cost -= 0.25;
            }

            // Normalize weights
            const total = Object.values(weights).reduce((sum, w) => sum + w, 0);
            Object.keys(weights).forEach(key => {
                weights[key] = weights[key] / total;
            });

            return weights;
        }

        generateSolutionReasoning(solution, noiseData, type) {
            const specs = this.solutionCharacteristics[solution];
            const reasons = [];

            // Base effectiveness
            reasons.push(`${specs.soundReduction}dB sound reduction with STC rating of ${specs.stc_rating}`);

            // Frequency handling
            if (specs.frequencyRange[0] < 100) {
                reasons.push('Effective low frequency handling');
            }
            if (specs.frequencyRange[1] > 4000) {
                reasons.push('Extended high frequency coverage');
            }

            // Special characteristics
            if (specs.impactResistance > 0.8) {
                reasons.push('High impact resistance');
            }
            if (specs.durability > 0.9) {
                reasons.push('Excellent durability');
            }

            // Installation and maintenance
            reasons.push(`${specs.installationTime} day installation with ${specs.maintenanceRequired} maintenance requirements`);

            // Cost consideration
            reasons.push(`Cost-effective solution at £${specs.total_cost.toFixed(2)} per m²`);

            return reasons;
        }

        calculateCoverageScore(solution, state) {
            try {
                const noiseSurfaces = this.getNoiseSourceSurfaces();
                const coveredSurfaces = solution.walls.length + (solution.ceiling ? 1 : 0);
                const requiredSurfaces = noiseSurfaces.walls.length + (noiseSurfaces.ceiling ? 1 : 0);
                return requiredSurfaces > 0 ? coveredSurfaces / requiredSurfaces : 1;
            } catch (error) {
                console.error('Error calculating coverage score:', error);
                return 0;
            }
        }

        calculateSolutionQualityScore(solution, state) {
            try {
                const scores = [];
                solution.walls.forEach(wall => {
                    scores.push(this.scoreNoiseTypeMatch(wall.solution, state.noiseData.type));
                });
                return scores.length > 0 ? scores.reduce((a, b) => a + b) / scores.length : 0;
            } catch (error) {
                console.error('Error calculating solution quality score:', error);
                return 0;
            }
        }

        calculateInstallationFeasibility(solution, state) {
            try {
                let feasibility = 1.0;
                
                // Check blockages
                if (state.blockages && state.blockages.wall && state.blockages.wall.length > 0) {
                    feasibility *= 0.8;
                }
                
                // Check dimensions
                if (state.dimensions) {
                    if (state.dimensions.height < 2.4) {
                        feasibility *= 0.9;
                    }
                }
                
                return feasibility;
            } catch (error) {
                console.error('Error calculating installation feasibility:', error);
                return 0;
            }
        }

        determineSolutionTier(noiseData, roomContext) {
            if (!noiseData) return 'standard';

            let score = 0;
            
            // Noise type scoring
            const noiseTypeScores = {
                'music': 3,
                'machinery': 3,
                'aircraft': 3,
                'traffic': 2,
                'speech': 1,
                'tv': 1,
                'footsteps': 2
            };
            score += noiseTypeScores[noiseData.type] || 1;

            // Intensity scoring
            const intensity = parseInt(noiseData.intensity) || 0;
            score += intensity;

            // Time of day scoring
            if (noiseData.time && Array.isArray(noiseData.time)) {
                if (noiseData.time.includes('night')) score += 2;
                if (noiseData.time.includes('evening')) score += 1;
            }

            // Room usage scoring (if available)
            if (roomContext && roomContext.usage) {
                const usageScores = {
                    'studio': 3,
                    'bedroom': 2,
                    'office': 2,
                    'living_room': 1
                };
                score += usageScores[roomContext.usage] || 0;
            }

            // Determine tier based on total score
            if (score >= 7) return 'premium';
            if (score >= 4) return 'standard';
            return 'basic';
        }

        generateWallReasoning(solution, wall, noiseData, state) {
            const reasons = [];
            const specs = solution.specs;

            // Basic performance reasoning
            reasons.push(`Provides ${specs.soundReduction}dB sound reduction`);

            // Noise type specific reasoning
            switch (noiseData.type) {
                case 'music':
                    reasons.push(`Enhanced bass control down to ${specs.frequencyRange[0]}Hz`);
                    reasons.push('Specialized for music transmission');
                    break;
                case 'speech':
                    reasons.push('Optimized for voice frequency ranges');
                    reasons.push('Enhanced privacy for conversations');
                    break;
                case 'traffic':
                    reasons.push('Designed for external noise reduction');
                    reasons.push('Enhanced low-frequency performance');
                    break;
                // Add cases for other noise types
            }

            // Room type considerations
            if (state.roomType === 'studio') {
                reasons.push('Studio-grade acoustic isolation');
            } else if (state.roomType === 'bedroom') {
                reasons.push('Optimized for sleep environment');
            }

            // Installation considerations
            reasons.push(`${specs.thickness * 1000}mm total build-up`);
            if (specs.installationTime) {
                reasons.push(`Typical installation: ${specs.installationTime} days`);
            }

            return reasons;
        }

        generateCeilingReasoning(solution, noiseData, state) {
            const reasons = [];
            const specs = solution.specs;

            reasons.push(`${specs.soundReduction}dB ceiling sound reduction`);
            
            if (noiseData.type === 'footsteps') {
                reasons.push('Specialized for impact noise from above');
                reasons.push('Enhanced structural decoupling');
            }

            if (state.roomType === 'studio') {
                reasons.push('Full frequency range isolation');
            }

            return reasons;
        }

        generateFloorReasoning(solution, noiseData, state) {
            const reasons = [];
            const specs = solution.specs;

            reasons.push(`${specs.soundReduction}dB floor sound reduction`);
            
            if (noiseData.type === 'footsteps') {
                reasons.push('Impact noise reduction for spaces below');
            }

            if (specs.impactResistance > 0.8) {
                reasons.push('High impact resistance rating');
            }

            return reasons;
        }

        generateSolutionReasoning(solution, specs, noiseData) {
            const reasons = [];
            
            // Add sound reduction reasoning
            reasons.push(`Provides ${specs.soundReduction}dB sound reduction`);
            
            // Add frequency-specific reasoning
            if (noiseData.type === 'music' && specs.frequencyRange[0] < 100) {
                reasons.push('Enhanced low frequency performance for music/bass');
            }
            
            // Add impact noise reasoning
            if (specs.impactResistance > 0.8) {
                reasons.push('High impact noise resistance');
            }
            
            // Add installation context
            reasons.push(`${specs.thickness * 1000}mm total build-up`);
            
            return reasons;
        }

        getAlternativeSolutions(noiseData, noiseSurfaces, priority, state) {
            const alternatives = [];
            
            // Add alternative wall solutions
            if (noiseSurfaces.walls.length > 0) {
                const solutionSet = priority === 'high' ? 
                    this.solutions.wall.premium : 
                    this.solutions.wall.standard;
                
                // Skip the first one as it's used in primary solution
                solutionSet.slice(1).forEach(solution => {
                    alternatives.push({
                        type: 'wall',
                        solution: solution,
                        description: this.getSolutionDescription(solution)
                    });
                });
            }

            return alternatives;
        }

        getNoiseTypeReasoning(noiseType) {
            const reasonings = {
                'speech': 'Optimized for voice and conversation noise',
                'music': 'Enhanced bass and low frequency control',
                'tv': 'Balanced for mixed media sound',
                'traffic': 'Designed for external traffic noise',
                'aircraft': 'Specialized for high-intensity external noise',
                'footsteps': 'Impact noise reduction focus',
                'furniture': 'Impact and structural noise control',
                'machinery': 'Heavy vibration and mechanical noise control'
            };
            return reasonings[noiseType] || 'General noise reduction';
        }

        getSolutionDescription(solution) {
            const descriptions = {
                'Genie Clip wall (Standard)': 'Premium isolation using specialized clip system',
                'Independent Wall (Standard)': 'Maximum isolation with independent wall construction',
                'Resilient bar wall (Standard)': 'Effective decoupling using resilient bars',
                'M20 Solution (Standard)': 'Standard double-layer solution with excellent cost-effectiveness',
                'Genie Clip wall (SP15 Soundboard Upgrade)': 'Maximum performance clip system with SP15',
                'Independent Wall (SP15 Soundboard Upgrade)': 'Premium independent wall with SP15 enhancement',
                'Resilient bar wall (SP15 Soundboard Upgrade)': 'Enhanced bar system with SP15 upgrade',
                'M20 Solution (SP15 Soundboard upgrade)': 'Enhanced performance with SP15 sound board',
                'Genie Clip ceiling': 'Premium ceiling isolation using clip system',
                'LB3 Genie Clip': 'Enhanced ceiling isolation with LB3 clips',
                'Independent Ceiling': 'Maximum ceiling isolation with independent construction',
                'Resilient bar Ceiling': 'Standard ceiling isolation system',
                'Genie Clip ceiling (SP15 Soundboard Upgrade)': 'Premium ceiling system with SP15 and clips',
                'LB3 Genie Clip (SP15 Soundboard Upgrade)': 'Enhanced LB3 ceiling system with SP15',
                'Independent Ceiling (SP15 Soundboard Upgrade)': 'Premium independent ceiling with SP15',
                'Resilient bar Ceiling (SP15 Soundboard Upgrade)': 'Enhanced ceiling system with SP15'
            };
            return descriptions[solution] || 'Custom solution';
        }

        async displayRecommendations(recommendations) {
            try {
                console.log('Displaying recommendations:', recommendations);
                
                // Get the container for solutions
                const solutionsContainer = document.getElementById('soundproofing-solutions');
                if (!solutionsContainer) {
                    console.error('Solutions container not found');
                    return;
                }

                // Generate HTML for primary solutions
                let html = '<div class="recommendations-container">';

                // Add wall solutions
                if (recommendations.primary && recommendations.primary.walls) {
                    const wallHtml = await this.generateWallSolutionsHtml(recommendations.primary);
                    html += wallHtml;
                }

                // Add ceiling solution if present
                if (recommendations.primary && recommendations.primary.ceiling) {
                    const ceilingHtml = await this.generateCeilingSolutionHtml(recommendations.primary.ceiling);
                    html += ceilingHtml;
                }

                // Add floor solution message if present
                if (recommendations.primary && recommendations.primary.floor) {
                    html += `
                        <div class="floor-solution">
                            <h4>Floor Treatment</h4>
                            <p>${recommendations.primary.floor.message}</p>
                            <div class="contact-info">
                                <p>Contact us:</p>
                                <p>Phone: ${recommendations.primary.floor.contactInfo.phone}</p>
                                <p>Email: ${recommendations.primary.floor.contactInfo.email}</p>
                            </div>
                        </div>
                    `;
                }

                html += '</div>';
                
                // Update the container
                solutionsContainer.innerHTML = html;

            } catch (error) {
                console.error('Error displaying recommendations:', error);
                const solutionsContainer = document.getElementById('soundproofing-solutions');
                if (solutionsContainer) {
                    solutionsContainer.innerHTML = '<div class="error-message">Error displaying recommendations</div>';
                }
            }
        }

        // Helper method to create solutions container
        createSolutionsContainer() {
            const container = document.createElement('div');
            container.id = 'soundproofing-solutions';
            
            const parent = document.querySelector('.recommendations-container') || 
                          document.getElementById('noise-details');
            
            if (!parent) {
                console.error('Could not find parent container for recommendations');
                throw new Error('Parent container not found');
            }
            
            parent.appendChild(container);
            return container;
        }

        calculateSolutionScore(solution, criteria, roomContext) {
            const solutionSpecs = this.solutionCharacteristics[solution];
            const noiseSpecs = this.noiseCharacteristics[criteria.noiseType] || this.noiseCharacteristics['speech'];
            const assessment = this.noiseAssessment;
            
            if (!solutionSpecs) {
                console.warn(`No specifications found for solution: ${solution}`);
                return 0;
            }

            // Base scores for different aspects
            const scores = {
                acousticPerformance: this.calculateAcousticScore(solutionSpecs, noiseSpecs, assessment),
                frequencyMatch: this.calculateFrequencyMatch(solutionSpecs.frequencyRange, noiseSpecs.frequencyRange),
                spaceEfficiency: this.calculateSpaceEfficiency(solutionSpecs, roomContext),
                costEffectiveness: this.calculateCostEffectiveness(solutionSpecs, assessment),
                installationSuitability: this.calculateInstallationSuitability(solutionSpecs, roomContext),
                durabilityMatch: this.calculateDurabilityMatch(solutionSpecs, assessment)
            };

            // Get dynamic weights based on user inputs
            const weights = this.calculateWeights(assessment);

            // Apply specific adjustments based on noise type and characteristics
            let finalScore = 0;
            
            // Adjust for noise type specifics
            if (noiseSpecs.bassHeavy && solutionSpecs.soundReduction > 50) {
                finalScore += 0.15; // Bonus for high reduction solutions with bass-heavy noise
            }

            if (noiseSpecs.impactComponent && solutionSpecs.impactResistance > 0.8) {
                finalScore += 0.1; // Bonus for impact-resistant solutions with impact noise
            }

            // Adjust for room usage
            if (assessment.roomDetails.usage === 'studio' && solutionSpecs.soundReduction > 52) {
                finalScore += 0.2; // Bonus for high reduction in studio settings
            }

            if (assessment.roomDetails.usage === 'bedroom' && solutionSpecs.thickness < 0.15) {
                finalScore += 0.1; // Bonus for thinner solutions in bedrooms
            }

            // Adjust for noise timing
            if (assessment.sourceDetails.occurrence.timeOfDay.includes('night') && solutionSpecs.soundReduction > 48) {
                finalScore += 0.15; // Bonus for high reduction solutions for night noise
            }

            // Adjust for perceived intensity
            if (assessment.sourceDetails.characteristics.perceived_intensity === 'intrusive' && solutionSpecs.soundReduction > 55) {
                finalScore += 0.2; // Bonus for very high reduction solutions with intrusive noise
            }

            // Calculate weighted base score
            const baseScore = Object.entries(scores).reduce((total, [criterion, score]) => {
                return total + (score * weights[criterion]);
            }, 0);

            // Combine base score with adjustments
            return Math.min(baseScore + finalScore, 1);
        }

        calculateWeights(assessment) {
            let weights = {
                acousticPerformance: 0.3,
                frequencyMatch: 0.2,
                spaceEfficiency: 0.15,
                costEffectiveness: 0.15,
                installationSuitability: 0.1,
                durabilityMatch: 0.1
            };

            // Adjust weights based on primary concern
            switch (assessment.problemAssessment.primary_concern) {
                case 'privacy':
                    weights.acousticPerformance += 0.1;
                    weights.frequencyMatch += 0.05;
                    weights.costEffectiveness -= 0.1;
                    weights.spaceEfficiency -= 0.05;
                    break;
                case 'recording':
                    weights.frequencyMatch += 0.15;
                    weights.acousticPerformance += 0.1;
                    weights.costEffectiveness -= 0.15;
                    weights.spaceEfficiency -= 0.1;
                    break;
                case 'sleep':
                    weights.acousticPerformance += 0.15;
                    weights.durabilityMatch += 0.05;
                    weights.costEffectiveness -= 0.1;
                    weights.installationSuitability -= 0.1;
                    break;
                case 'concentration':
                    weights.acousticPerformance += 0.1;
                    weights.frequencyMatch += 0.1;
                    weights.costEffectiveness -= 0.1;
                    weights.spaceEfficiency -= 0.1;
                    break;
            }

            // Adjust for noise characteristics
            if (assessment.sourceDetails.characteristics.bass_content) {
                weights.frequencyMatch += 0.1;
                weights.acousticPerformance += 0.05;
                weights.spaceEfficiency -= 0.15;
            }

            if (assessment.sourceDetails.characteristics.vibration) {
                weights.durabilityMatch += 0.1;
                weights.installationSuitability += 0.05;
                weights.costEffectiveness -= 0.15;
            }

            // Normalize weights to ensure they sum to 1
            const totalWeight = Object.values(weights).reduce((sum, weight) => sum + weight, 0);
            Object.keys(weights).forEach(key => {
                weights[key] = weights[key] / totalWeight;
            });

            return weights;
        }

        calculateAcousticScore(solution, noise, assessment) {
            let score = solution.soundReduction / 60; // Base score normalized to max 60 dB reduction

            // Adjust for perceived intensity
            const intensityFactors = {
                'barely_noticeable': 0.6,
                'noticeable': 0.8,
                'very_noticeable': 1.0,
                'intrusive': 1.2
            };
            const intensityFactor = intensityFactors[assessment.sourceDetails.characteristics.perceived_intensity] || 1.0;
            score *= intensityFactor;

            // Adjust for impact levels
            const impactScore = (
                assessment.problemAssessment.impact_level.conversation_privacy +
                assessment.problemAssessment.impact_level.sleep_disturbance +
                assessment.problemAssessment.impact_level.concentration_impact
            ) / 15; // Normalize to 0-1 range
            score *= (1 + impactScore);

            return Math.min(score, 1); // Ensure score doesn't exceed 1
        }

        calculateFrequencyMatch(solutionRange, noiseRange) {
            // Calculate frequency range overlap
            const overlap = Math.min(solutionRange[1], noiseRange[1]) - 
                           Math.max(solutionRange[0], noiseRange[0]);
            const noiseSpan = noiseRange[1] - noiseRange[0];
            
            // Calculate base score from overlap
            let score = Math.max(0, overlap / noiseSpan);

            // Bonus for solutions that cover the entire noise range
            if (solutionRange[0] <= noiseRange[0] && solutionRange[1] >= noiseRange[1]) {
                score *= 1.2;
            }

            // Penalty for solutions that miss critical frequencies
            if (solutionRange[0] > noiseRange[0] * 1.2) { // Missing low frequencies
                score *= 0.8;
            }
            if (solutionRange[1] < noiseRange[1] * 0.8) { // Missing high frequencies
                score *= 0.8;
            }

            return Math.min(score, 1);
        }

        calculateCostEffectiveness(solution, assessment) {
            const baseCost = solution.total_cost;
            const maxReasonableCost = 300; // Adjust based on your price range
            let score = 1 - (baseCost / maxReasonableCost);

            // Adjust based on perceived intensity
            const intensityFactors = {
                'barely_noticeable': 1.2, // Cost more important for minor issues
                'noticeable': 1.0,
                'very_noticeable': 0.8,
                'intrusive': 0.6  // Cost less important for severe issues
            };
            score *= intensityFactors[assessment.sourceDetails.characteristics.perceived_intensity] || 1.0;

            // Adjust for frequency of occurrence
            if (assessment.sourceDetails.occurrence.frequency === 'constant') {
                score *= 0.8; // Cost less important for constant noise
            }

            return Math.max(Math.min(score, 1), 0);
        }

        calculateInstallationSuitability(solution, roomContext) {
            let score = 1;

            // Base score from solution characteristics
            score *= solution.installationTime <= 1 ? 1 : 
                    solution.installationTime <= 2 ? 0.9 : 
                    solution.installationTime <= 3 ? 0.8 : 0.7;

            // Adjust for room context if available
            if (roomContext) {
                // Check for blockages
                if (roomContext.blockages) {
                    const blockageCount = Object.values(roomContext.blockages)
                        .filter(Boolean).length;
                    score *= (1 - (blockageCount * 0.1));
                }

                // Check room dimensions
                if (roomContext.dimensions) {
                    if (roomContext.dimensions.height < 2.4) {
                        score *= 0.9; // Penalty for low ceilings
                    }
                }
            }

            // Adjust for solution complexity
            if (solution.notes && solution.notes.length > 0) {
                const complexityPenalty = solution.notes
                    .filter(note => note.toLowerCase().includes('complex') || 
                                  note.toLowerCase().includes('difficult'))
                    .length * 0.1;
                score *= (1 - complexityPenalty);
            }

            return Math.min(Math.max(score, 0), 1);
        }

        calculateDurabilityMatch(solution, assessment) {
            let score = solution.durability; // Base score from solution durability

            // Adjust for usage intensity
            const intensityFactors = {
                'barely_noticeable': 1.2,
                'noticeable': 1.0,
                'very_noticeable': 0.9,
                'intrusive': 0.8
            };
            score *= intensityFactors[assessment.sourceDetails.characteristics.perceived_intensity] || 1.0;

            // Adjust for frequency of use
            if (assessment.sourceDetails.occurrence.frequency === 'constant') {
                score *= 0.9;
            }

            // Adjust for impact noise
            if (assessment.sourceDetails.characteristics.impact_noise) {
                score *= solution.impactResistance;
            }

            // Adjust for vibration
            if (assessment.sourceDetails.characteristics.vibration) {
                score *= solution.impactResistance * 0.9;
            }

            return Math.min(Math.max(score, 0), 1);
        }

        getNoiseSourceSurfaces() {
            const directions = window.FormState.noiseData?.direction || [];
            return {
                walls: directions.filter(d => ['north', 'south', 'east', 'west'].includes(d)),
                ceiling: directions.includes('ceiling'),
                floor: directions.includes('floor')
            };
        }

        getNoisePriority() {
            const { type, intensity, time } = window.FormState.noiseData || {};
            let priority = 'medium';

            // High priority cases
            if (
                (intensity >= 4) || // High/Very High intensity
                (time?.includes('night')) || // Night-time noise
                (['music', 'machinery'].includes(type)) // Specific noise types
            ) {
                priority = 'high';
            }
            // Low priority cases
            else if (
                (intensity <= 2) && // Low/Very Low intensity
                (!time?.includes('night')) // Not night-time
            ) {
                priority = 'low';
            }

            return priority;
        }

        calculateAreas(dimensions) {
            const { length = 0, width = 0, height = 0 } = dimensions;
            return {
                walls: 2 * (length * height + width * height),
                floor: length * width,
                ceiling: length * width
            };
        }

        // Add method to format area display
        formatArea(value) {
            return value ? `${value.toFixed(2)} m²` : '0 m²';
        }

        // Update area displays
        updateAreaDisplays(dimensions) {
            const areas = this.calculateAreas(dimensions);
            
            const wallAreaElement = document.getElementById('wall-area');
            const floorAreaElement = document.getElementById('floor-area');
            const ceilingAreaElement = document.getElementById('ceiling-area');

            if (wallAreaElement) {
                wallAreaElement.textContent = this.formatArea(areas.walls);
            }
            if (floorAreaElement) {
                floorAreaElement.textContent = this.formatArea(areas.floor);
            }
            if (ceilingAreaElement) {
                ceilingAreaElement.textContent = this.formatArea(areas.ceiling);
            }
        }

        // Add the missing scoreNoiseTypeMatch function
        scoreNoiseTypeMatch(solution, noiseType) {
            const solutionSpecs = this.solutionCharacteristics[solution];
            const noiseSpecs = this.noiseCharacteristics[noiseType] || this.noiseCharacteristics['speech'];
            
            if (!solutionSpecs || !noiseSpecs) return 0.5; // Default score if specs missing

            let score = 0;

            // Score based on frequency range match
            score += this.calculateFrequencyMatch(solutionSpecs.frequencyRange, noiseSpecs.frequencyRange) * 0.4;

            // Score based on sound reduction vs typical intensity
            const reductionScore = solutionSpecs.soundReduction / noiseSpecs.typicalIntensity;
            score += Math.min(reductionScore, 1) * 0.3;

            // Score based on impact vs airborne handling
            if (noiseSpecs.impactComponent && solutionSpecs.impactResistance > 0.7) {
                score += 0.15;
            }
            if (noiseSpecs.airborneComponent && solutionSpecs.soundReduction > 45) {
                score += 0.15;
            }

            return score;
        }

        // Add this method to the SoundproofingManager class
        generateEffectivenessHtml(effectiveness) {
            const effectivenessPercent = effectiveness.overall ? 
                Math.round(effectiveness.overall * 100) : 0;
            
            return `
                <div class="effectiveness-rating">
                    <span class="rating-label">Solution Effectiveness:</span>
                    <span class="rating-value">${effectivenessPercent}%</span>
                </div>`;
        }

        // Add solution mapping function
        getSolutionDisplayName(solutionId) {
            const solutionData = this.solutionCharacteristics[solutionId];
            return solutionData?.displayName || solutionId;
        }

        // Update the wall solutions HTML generator
        async generateWallSolutionsHtml(recommendations) {
            try {
                if (!recommendations || !recommendations.walls || !Array.isArray(recommendations.walls)) {
                    console.warn('No wall recommendations available:', recommendations);
                    return '<p>No wall solutions available.</p>';
                }

                let html = '<div class="wall-solutions">';
                
                // Get current dimensions
                const dimensions = {
                    length: parseFloat(document.getElementById('length')?.value || 0),
                    width: parseFloat(document.getElementById('width')?.value || 0),
                    height: parseFloat(document.getElementById('height')?.value || 0)
                };

                console.log('Current dimensions:', dimensions);

                for (const wall of recommendations.walls) {
                    if (!wall || !wall.solution) {
                        console.warn('Invalid wall data:', wall);
                        continue;
                    }
                    
                    const solutionData = this.solutionCharacteristics[wall.solution];
                    if (!solutionData) {
                        console.warn('No solution data found for:', wall.solution);
                        continue;
                    }

                    // Calculate costs
                    console.log('Calculating costs for wall:', wall.wall);
                    const costs = await this.calculateLocalCosts(
                        wall.solution,
                        dimensions,
                        'wall',
                        wall.wall.toLowerCase()
                    );

                    console.log('Cost calculation result:', costs);

                    // Generate cost breakdown HTML
                    let costBreakdownHtml = '';
                    if (costs && !costs.error) {
                        costBreakdownHtml = `
                            <div class="cost-breakdown">
                                <h6>Cost Breakdown</h6>
                                <div class="cost-items">
                                    ${costs.materials.map(material => `
                                        <div class="cost-item">
                                            <span class="material-name">${material.name}</span>
                                            <span class="material-amount">${material.amount} ${material.unit}</span>
                                            <span class="material-cost">£${material.cost.toFixed(2)}</span>
                                        </div>
                                    `).join('')}
                                </div>
                                <div class="total-cost">
                                    <strong>Total Cost:</strong> £${costs.total.toFixed(2)}
                                </div>
                                <div class="area-info">
                                    <strong>Wall Area:</strong> ${costs.area}m²
                                </div>
                            </div>
                        `;
                    } else {
                        console.error('Cost calculation failed:', costs);
                        costBreakdownHtml = `
                            <div class="error-message">
                                Unable to calculate costs. Please check dimensions.
                            </div>
                        `;
                    }

                    // Add the solution card HTML
                    html += `
                        <div class="solution-card ${wall.score > 0.7 ? 'premium' : 'standard'}">
                            <div class="solution-header">
                                <div class="header-main">
                                    <h4>${wall.wall} Wall</h4>
                                    <div class="solution-badge ${wall.score > 0.7 ? 'premium' : 'standard'}">
                                        ${wall.score > 0.7 ? 'Premium' : 'Standard'}
                                    </div>
                                </div>
                                <div class="effectiveness-meter">
                                    <div class="meter-fill" style="width: ${(wall.score * 100)}%"></div>
                                    <span class="meter-label">${(wall.score * 100).toFixed(0)}% Effective</span>
                                </div>
                            </div>
                            
                            <div class="solution-content">
                                <div class="solution-main-details">
                                    <h5 class="solution-name">${solutionData.displayName || wall.solution}</h5>
                                    <div class="specs-grid">
                                        <div class="spec-item">
                                            <i class="fas fa-volume-down"></i>
                                            <span class="label">Reduction</span>
                                            <span class="value">${solutionData.soundReduction}dB</span>
                                        </div>
                                        <div class="spec-item">
                                            <i class="fas fa-wave-square"></i>
                                            <span class="label">Frequency</span>
                                            <span class="value">${solutionData.frequencyRange[0]}-${solutionData.frequencyRange[1]}Hz</span>
                                        </div>
                                        <div class="spec-item">
                                            <i class="fas fa-clock"></i>
                                            <span class="label">Install Time</span>
                                            <span class="value">${solutionData.installationTime} days</span>
                                        </div>
                                        <div class="spec-item">
                                            <i class="fas fa-tools"></i>
                                            <span class="label">Maintenance</span>
                                            <span class="value">${solutionData.maintenanceRequired}</span>
                                        </div>
                                    </div>
                                </div>

                                <div class="solution-features">
                                    <h6>Key Features</h6>
                                    <ul class="features-list">
                                        ${wall.reasoning.map(reason => `<li>${reason}</li>`).join('')}
                                    </ul>
                                </div>

                                ${costBreakdownHtml}
                            </div>
                        </div>
                    `;
                }

                html += '</div>';
                return html;

            } catch (error) {
                console.error('Error generating wall solutions HTML:', error);
                return '<p>Error displaying wall solutions.</p>';
            }
        }

        // Update the ceiling solution HTML generator to use the new solution names
        async generateCeilingSolutionHtml(ceiling) {
            let html = `
                    <div class="solution-item">
                        <div class="solution-header">
                        <span class="solution-location">Ceiling Treatment</span>
                        <span class="solution-name">${this.getSolutionDisplayName(ceiling.solution)}</span>
                            <span class="solution-score">Effectiveness: ${(ceiling.score * 100).toFixed(1)}%</span>
                    </div>`;

            const solutionData = this.solutionCharacteristics[ceiling.solution];
            if (solutionData) {
                html += `
                        <div class="solution-details">
                        <div class="solution-specs">
                            <p><strong>Sound Reduction:</strong> ${solutionData.soundReduction} dB</p>
                            <p><strong>Frequency Range:</strong> ${solutionData.frequencyRange[0]}-${solutionData.frequencyRange[1]} Hz</p>
                            <p><strong>STC Rating:</strong> ${solutionData.stc_rating}</p>
                        </div>
                        ${ceiling.reasoning.map(reason => `<div class="solution-reason">• ${reason}</div>`).join('')}
                    </div>`;
            }

            try {
                const costs = await this.calculateLocalCosts(ceiling.solution, window.FormState.dimensions, 'ceiling');
                if (costs && !costs.error) {
                    html += this.generateCostBreakdownHtml(costs);
                }
            } catch (error) {
                console.error('Error fetching ceiling costs:', error);
                html += `<div class="error-message">Error loading cost breakdown</div>`;
            }

            html += '</div>';
            return html;
        }

        validateDimensions(dimensions) {
            const errors = [];
            if (!dimensions.length || dimensions.length <= 0) {
                errors.push('Length must be greater than 0');
            }
            if (!dimensions.width || dimensions.width <= 0) {
                errors.push('Width must be greater than 0');
            }
            if (!dimensions.height || dimensions.height <= 0) {
                errors.push('Height must be greater than 0');
            }
            return {
                isValid: errors.length === 0,
                errors
            };
        }

        // Add local cost calculation function
        async calculateLocalCosts(solution, dimensions, surfaceType = 'wall', wall = null) {
            // Input validation
            if (!dimensions || !dimensions.length || !dimensions.width || !dimensions.height) {
                console.error('Invalid dimensions:', dimensions);
                return {
                    error: true,
                    message: 'Please provide valid room dimensions'
                };
            }

            // Find solution data
            const solutionData = this.solutionCharacteristics.find(s => s.name === solution);
            if (!solutionData) {
                console.error('Solution not found:', solution);
                return {
                    error: true,
                    message: 'Solution not found'
                };
            }

            // Calculate area and perimeter
            let area = 0;
            let perimeter = 0;
            if (surfaceType === 'wall') {
                if (wall === 'north' || wall === 'south') {
                    area = dimensions.width * dimensions.height;
                    perimeter = 2 * (dimensions.width + dimensions.height);
                } else if (wall === 'east' || wall === 'west') {
                    area = dimensions.length * dimensions.height;
                    perimeter = 2 * (dimensions.length + dimensions.height);
                }
            } else if (surfaceType === 'ceiling' || surfaceType === 'floor') {
                area = dimensions.length * dimensions.width;
                perimeter = 2 * (dimensions.length + dimensions.width);
            }

            if (!area || area <= 0) {
                console.error('Invalid area calculation');
                return {
                    error: true,
                    message: 'Invalid area calculation'
                };
            }

            // Calculate costs for each material
            let totalCost = 0;
            const materialsCosts = [];

            for (const material of solutionData.materials) {
                const coverage = parseFloat(material.coverage) || 1;
                const needsWastage = [
                    'Premium Acoustic Panel',
                    'Dampening Material',
                    '12.5mm Sound Plasterboard',
                    'SP15 Soundboard',
                    'Rockwool RWA45 50mm',
                    'Rockwool RW3 100mm'
                ].includes(material.name);

                const isPerimeterBased = [
                    'Acoustic Sealant',
                    'Acoustic Mastic'
                ].includes(material.name);

                let amount;
                if (isPerimeterBased) {
                    amount = Math.ceil(perimeter / coverage);
                } else {
                    const calcArea = needsWastage ? area * 1.1 : area;
                    amount = Math.ceil(calcArea / coverage);
                }

                const cost = amount * material.cost;
                totalCost += cost;

                materialsCosts.push({
                    name: material.name,
                    amount: amount,
                    unit: material.unit,
                    cost: cost
                });
            }

            // Add labor cost
            const laborUnits = Math.ceil(area / 10); // 1 unit per 10m²
            const laborCost = laborUnits * solutionData.labor_rate;
            totalCost += laborCost;

            materialsCosts.push({
                name: 'Installation Labor',
                amount: laborUnits,
                unit: 'hours',
                cost: laborCost
            });

            return {
                costs: materialsCosts,
                total: totalCost,
                area: area,
                perimeter: perimeter
            };
        }

        bindDynamicUpdates() {
            // Listen for form state updates
            window.addEventListener('formStateUpdated', (event) => {
                console.log('Form state updated:', event.detail);
                this.handleFormUpdate('formState');
            });

            // Listen for blockage updates
            window.addEventListener('blockagesUpdated', (event) => {
                console.log('Blockages updated:', event.detail);
                this.handleFormUpdate('blockages');
            });

            // Listen for dimensions updates
            window.addEventListener('dimensionsUpdated', (event) => {
                console.log('Dimensions updated:', event.detail);
                this.handleFormUpdate('dimensions');
            });

            // Listen for noise data updates
            window.addEventListener('noiseDataUpdated', (event) => {
                console.log('Noise data updated:', event.detail);
                this.handleFormUpdate('noise');
            });

            // Add click event listeners for surfaces using event delegation
            document.addEventListener('click', async (event) => {
                const surfaceElement = event.target.closest('.surface-clickable');
                if (!surfaceElement) return;

                try {
                    // Remove active class from all surfaces
                    document.querySelectorAll('.surface-clickable').forEach(el => {
                        if (el !== surfaceElement) el.classList.remove('active');
                    });

                    // Toggle active class on clicked surface
                    surfaceElement.classList.toggle('active');

                    const surfaceType = surfaceElement.dataset.surface;
                    const wall = surfaceElement.dataset.wall;
                    
                    // Get current dimensions
                    const dimensions = {
                        length: parseFloat(document.getElementById('length')?.value || 0),
                        width: parseFloat(document.getElementById('width')?.value || 0),
                        height: parseFloat(document.getElementById('height')?.value || 0)
                    };

                    console.log('Surface clicked:', { surfaceType, wall, dimensions });

                    // Validate dimensions
                    if (this.validateDimensions(dimensions).isValid) {
                        const solutionName = surfaceElement.querySelector('.solution-name')?.textContent;
                        console.log('Calculating costs for solution:', solutionName);

                        if (!solutionName) {
                            console.error('No solution name found in element');
                            return;
                        }

                        const costs = await this.calculateLocalCosts(
                            solutionName,
                            dimensions,
                            surfaceType,
                            wall
                        );
                        
                        console.log('Calculated costs:', costs);
                        
                        // Update the cost breakdown display
                        const costBreakdownElement = surfaceElement.querySelector('.cost-breakdown');
                        if (costBreakdownElement) {
                            if (costs.error) {
                                costBreakdownElement.innerHTML = `<div class="error-message">${costs.message}</div>`;
                            } else {
                                const costHtml = this.generateCostBreakdownHtml(costs);
                                console.log('Generated cost HTML:', costHtml);
                                costBreakdownElement.innerHTML = costHtml;
                            }
                            costBreakdownElement.style.display = 'block';
                        } else {
                            console.error('Cost breakdown element not found');
                        }
                    } else {
                        console.error('Invalid dimensions:', dimensions);
                    }
                } catch (error) {
                    console.error('Error in surface click handler:', error);
                }
            });
        }

        generateCostBreakdownHtml(costs) {
            if (!costs || !costs.materials) {
                return '<div class="cost-breakdown"><p class="no-data">No cost information available.</p></div>';
            }

            return `
                <div class="cost-breakdown">
                    <div class="cost-breakdown-header">
                        <h5>Cost Breakdown</h5>
                        <div class="area-info">Surface Area: ${costs.area} m²</div>
                    </div>
                    <div class="cost-items">
                        <div class="cost-item header">
                            <span>Material</span>
                            <span>Quantity</span>
                            <span>Cost</span>
                        </div>
                        ${costs.materials.map(material => `
                            <div class="cost-item">
                                <span class="material-name">${material.name}</span>
                                <span class="material-amount">${material.amount} ${material.unit}</span>
                                <span class="material-cost">£${material.cost.toFixed(2)}</span>
                            </div>
                        `).join('')}
                    </div>
                    <div class="total-cost">
                        <span>Total Cost</span>
                        <span class="total-amount">£${costs.total.toFixed(2)}</span>
                    </div>
                    <div class="cost-notes">
                        <p>* Prices include standard installation</p>
                        <p>* Additional costs may apply for complex installations</p>
                    </div>
                </div>
            `;
        }

        // ... existing code ...

        // Keep only the new generateSolutionHtml method
        generateSolutionHtml(wall, costs) {
            if (!wall || !wall.solution) {
                return '<p>No solution available for this surface.</p>';
            }

            const solutionData = this.solutionCharacteristics[wall.solution];
            if (!solutionData) {
                return '<p>Solution data not found.</p>';
            }

            return `
                <div class="solution-details">
                    <h4 class="solution-name">${solutionData.displayName || wall.solution}</h4>
                    <div class="solution-specs">
                        <p><strong>Sound Reduction:</strong> ${solutionData.soundReduction} dB</p>
                        <p><strong>Frequency Range:</strong> ${solutionData.frequencyRange[0]}-${solutionData.frequencyRange[1]} Hz</p>
                        <p><strong>Installation Time:</strong> ${solutionData.installationTime} days</p>
                        <p><strong>STC Rating:</strong> ${solutionData.stc_rating}</p>
                                            </div>
                    <div class="solution-notes">
                        ${solutionData.notes.map(note => `<p class="note">${note}</p>`).join('')}
                                            </div>
                    ${costs ? this.generateCostBreakdownHtml(costs) : ''}
                                            </div>
            `;
        }

        getPrimarySolutions(noiseData, noiseSurfaces, priority) {
            try {
                const solutions = {
                    walls: [],
                    ceiling: null,
                    floor: null
                };

                // Process wall solutions based on multiple factors
                if (noiseSurfaces.walls && noiseSurfaces.walls.length > 0) {
                    noiseSurfaces.walls.forEach(wall => {
                        // Adjust solution selection based on wall position and noise direction
                        const wallScore = this.calculateWallSpecificScore(wall, noiseData);
                        const solutionScore = this.calculateSolutionScore(noiseData, wallScore);
                        
                        // Get different solutions based on wall position and noise characteristics
                        let solution;
                        if (noiseData.direction.includes(wall.toLowerCase())) {
                            // Direct noise path gets premium solutions
                            solution = this.selectBestSolution(
                                { standard: 0.3, premium: 0.7 }, // Bias towards premium for direct noise
                                noiseData,
                                wall
                            );
                        } else {
                            // Indirect noise paths get balanced solution selection
                            solution = this.selectBestSolution(
                                solutionScore,
                                noiseData,
                                wall
                            );
                        }

                        solutions.walls.push({
                            wall: wall,
                            solution: solution.name,
                            score: solution.score,
                            reasoning: solution.reasoning
                        });
                    });
                }

                // Process ceiling solution based on noise characteristics
                if (noiseSurfaces.ceiling) {
                    const ceilingScore = this.calculateCeilingSolutionScore(noiseData);
                    const ceilingSolution = this.selectBestCeilingSolution(ceilingScore, noiseData);
                    solutions.ceiling = {
                        solution: ceilingSolution.name,
                        score: ceilingSolution.score,
                        reasoning: ceilingSolution.reasoning
                    };
                }

                // Process floor solution if needed
                if (noiseSurfaces.floor) {
                    const floorScore = this.calculateFloorSolutionScore(noiseData);
                    solutions.floor = this.selectBestFloorSolution(floorScore, noiseData);
                }

                return solutions;
            } catch (error) {
                console.error('Error in getPrimarySolutions:', error);
                return { walls: [], ceiling: null, floor: null };
            }
        }

        calculateWallSpecificScore(wall, noiseData) {
            // Base score
            let wallScore = 1.0;

            // Adjust score based on noise direction
            if (noiseData.direction.includes(wall.toLowerCase())) {
                wallScore *= 1.5; // Increase importance for walls directly facing noise
            }

            // Adjust for noise type
            const noiseTypeMultipliers = {
                'music': 1.4,
                'machinery': 1.3,
                'speech': 1.1,
                'tv': 1.2,
                'traffic': 1.3,
                'aircraft': 1.4,
                'footsteps': 1.1
            };
            wallScore *= noiseTypeMultipliers[noiseData.type] || 1.0;

            // Adjust for intensity
            wallScore *= (noiseData.intensity / 5); // Normalize intensity effect

            return wallScore;
        }

        selectBestSolution(scores, noiseData, wall) {
            const solutions = {
                standard: this.solutions.wall.standard,
                premium: this.solutions.wall.premium
            };

            // Select category based on scores and wall-specific factors
            const category = scores.premium > scores.standard ? 'premium' : 'standard';
            const solutionList = solutions[category];

            // Select specific solution based on multiple factors
            const intensityIndex = Math.min(
                Math.floor(noiseData.intensity / 3.34),
                solutionList.length - 1
            );

            // Add variation based on wall position
            const wallPositionOffset = wall.toLowerCase() === noiseData.direction[0] ? 1 : 0;
            const finalIndex = Math.min(
                intensityIndex + wallPositionOffset,
                solutionList.length - 1
            );

            return {
                name: solutionList[finalIndex],
                score: scores[category],
                reasoning: this.generateSolutionReasoning(solutionList[finalIndex], noiseData, wall)
            };
        }

        calculateCeilingSolutionScore(noiseData) {
            const scores = {
                standard: 0,
                premium: 0
            };

            // Factor 1: Noise Type Weight
            const noiseTypeWeights = {
                'music': { standard: 0.3, premium: 0.7 },
                'machinery': { standard: 0.2, premium: 0.8 },
                'speech': { standard: 0.7, premium: 0.3 },
                'tv': { standard: 0.6, premium: 0.4 },
                'traffic': { standard: 0.4, premium: 0.6 },
                'aircraft': { standard: 0.3, premium: 0.7 },
                'footsteps': { standard: 0.5, premium: 0.5 }
            };

            // Factor 2: Noise Intensity Weight
            const intensityWeight = noiseData.intensity / 10; // Assuming intensity is 1-10

            // Factor 3: Budget Consideration
            const budgetWeight = window.FormState?.requirements?.budget === 'high' ? 0.7 : 0.3;

            // Calculate final scores
            const typeWeights = noiseTypeWeights[noiseData.type] || { standard: 0.5, premium: 0.5 };
            scores.standard = (typeWeights.standard * 0.4) + ((1 - intensityWeight) * 0.4) + ((1 - budgetWeight) * 0.2);
            scores.premium = (typeWeights.premium * 0.4) + (intensityWeight * 0.4) + (budgetWeight * 0.2);

            return scores;
        }

        selectBestCeilingSolution(scores, noiseData) {
            const solutions = {
                standard: this.solutions.ceiling.standard,
                premium: this.solutions.ceiling.premium
            };

            // Select the appropriate category based on scores
            const category = scores.premium > scores.standard ? 'premium' : 'standard';
            const solutionList = solutions[category];

            // Select specific solution based on noise characteristics
            const solutionIndex = Math.min(
                Math.floor(noiseData.intensity / 3.34), // 0-2 index based on intensity
                solutionList.length - 1
            );

            return {
                name: solutionList[solutionIndex],
                score: scores[category],
                reasoning: this.generateSolutionReasoning(solutionList[solutionIndex], noiseData)
            };
        }

        calculateFloorSolutionScore(noiseData) {
            const scores = {
                standard: 0,
                premium: 0
            };

            // Factor 1: Noise Type Weight
            const noiseTypeWeights = {
                'music': { standard: 0.3, premium: 0.7 },
                'machinery': { standard: 0.2, premium: 0.8 },
                'speech': { standard: 0.7, premium: 0.3 },
                'tv': { standard: 0.6, premium: 0.4 },
                'traffic': { standard: 0.4, premium: 0.6 },
                'aircraft': { standard: 0.3, premium: 0.7 },
                'footsteps': { standard: 0.5, premium: 0.5 }
            };

            // Factor 2: Noise Intensity Weight
            const intensityWeight = noiseData.intensity / 10; // Assuming intensity is 1-10

            // Factor 3: Budget Consideration
            const budgetWeight = window.FormState?.requirements?.budget === 'high' ? 0.7 : 0.3;

            // Calculate final scores
            const typeWeights = noiseTypeWeights[noiseData.type] || { standard: 0.5, premium: 0.5 };
            scores.standard = (typeWeights.standard * 0.4) + ((1 - intensityWeight) * 0.4) + ((1 - budgetWeight) * 0.2);
            scores.premium = (typeWeights.premium * 0.4) + (intensityWeight * 0.4) + (budgetWeight * 0.2);

            return scores;
        }

        selectBestFloorSolution(scores, noiseData) {
            const solutions = {
                standard: this.solutions.floor.standard,
                premium: this.solutions.floor.premium
            };

            // Select the appropriate category based on scores
            const category = scores.premium > scores.standard ? 'premium' : 'standard';
            const solutionList = solutions[category];

            // Select specific solution based on noise characteristics
            const solutionIndex = Math.min(
                Math.floor(noiseData.intensity / 3.34), // 0-2 index based on intensity
                solutionList.length - 1
            );

            return {
                name: solutionList[solutionIndex],
                score: scores[category],
                reasoning: this.generateSolutionReasoning(solutionList[solutionIndex], noiseData)
            };
        }

        generateSolutionReasoning(solutionName, noiseData) {
            if (!noiseData || !noiseData.type) {
                console.warn('Missing noise data for generating solution reasoning');
                return ['Recommended based on general soundproofing requirements'];
            }

            const solutionData = this.solutionCharacteristics[solutionName];
            if (!solutionData) {
                console.warn('No solution data found for:', solutionName);
                return ['Solution details not available'];
            }

            const reasons = [];

            // Add noise type specific reasoning
            switch (noiseData.type) {
                case 'music':
                    reasons.push(`Optimized for musical frequencies (${solutionData.frequencyRange[0]}-${solutionData.frequencyRange[1]}Hz)`);
                    reasons.push(`Provides ${solutionData.soundReduction}dB reduction, ideal for music isolation`);
                    break;
                case 'speech':
                    reasons.push(`Effective against speech frequencies (${solutionData.frequencyRange[0]}-${solutionData.frequencyRange[1]}Hz)`);
                    reasons.push(`${solutionData.soundReduction}dB reduction suitable for conversation privacy`);
                    break;
                case 'machinery':
                    reasons.push(`Designed to combat mechanical noise and vibrations`);
                    reasons.push(`Heavy-duty sound reduction of ${solutionData.soundReduction}dB`);
                    break;
                case 'tv':
                    reasons.push(`Balanced frequency response for TV and entertainment sound`);
                    reasons.push(`${solutionData.soundReduction}dB reduction for media noise control`);
                    break;
                case 'traffic':
                    reasons.push(`Effective against low-frequency traffic noise`);
                    reasons.push(`${solutionData.soundReduction}dB reduction with focus on bass frequencies`);
                    break;
                case 'aircraft':
                    reasons.push(`Specialized for high-intensity aircraft noise`);
                    reasons.push(`Maximum sound reduction of ${solutionData.soundReduction}dB`);
                    break;
                case 'footsteps':
                    reasons.push(`Impact noise reduction technology`);
                    reasons.push(`${solutionData.soundReduction}dB reduction with vibration dampening`);
                    break;
                default:
                    reasons.push(`General purpose soundproofing solution`);
                    reasons.push(`Standard ${solutionData.soundReduction}dB noise reduction`);
            }

            // Add intensity-based reasoning
            if (noiseData.intensity >= 8) {
                reasons.push('Premium solution for high-intensity noise');
            } else if (noiseData.intensity >= 5) {
                reasons.push('Enhanced protection for moderate noise levels');
            } else {
                reasons.push('Standard protection for typical noise levels');
            }

            // Add solution-specific features
            if (solutionData.notes && Array.isArray(solutionData.notes)) {
                reasons.push(...solutionData.notes);
            }

            // Add installation and maintenance info
            reasons.push(`Installation time: ${solutionData.installationTime} days`);
            if (solutionData.maintenanceRequired) {
                reasons.push(`Maintenance: ${solutionData.maintenanceRequired}`);
            }

            return reasons;
        }
    }

    window.SoundproofingManager = SoundproofingManager;
}

// Initialize manager
if (!window.soundproofingManager) {
    window.soundproofingManager = new SoundproofingManager();
    window.soundproofingManager.initialize();
}

// Keep the validateDimensions helper
function validateDimensions(dimensions) {
    const errors = [];
    const validated = {
        length: parseFloat(dimensions.length),
        width: parseFloat(dimensions.width),
        height: parseFloat(dimensions.height)
    };

    // Check each dimension
    if (!validated.length || validated.length <= 0) {
        errors.push('Invalid room length');
    }
    if (!validated.width || validated.width <= 0) {
        errors.push('Invalid room width');
    }
    if (!validated.height || validated.height <= 0) {
        errors.push('Invalid room height');
    }

    // Add reasonable limits
    const MAX_DIMENSION = 30; // 30 meters
    const MIN_DIMENSION = 0.5; // 0.5 meters

    if (validated.length > MAX_DIMENSION || validated.length < MIN_DIMENSION) {
        errors.push(`Room length must be between ${MIN_DIMENSION}m and ${MAX_DIMENSION}m`);
    }
    if (validated.width > MAX_DIMENSION || validated.width < MIN_DIMENSION) {
        errors.push(`Room width must be between ${MIN_DIMENSION}m and ${MAX_DIMENSION}m`);
    }
    if (validated.height > MAX_DIMENSION || validated.height < MIN_DIMENSION) {
        errors.push(`Room height must be between ${MIN_DIMENSION}m and ${MAX_DIMENSION}m`);
    }

    return {
        isValid: errors.length === 0,
        dimensions: validated,
        errors: errors
    };
}