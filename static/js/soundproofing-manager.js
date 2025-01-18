if (!window.SoundproofingManager) {
    class SoundproofingManager {
        constructor() {
            this.initialized = false;
            this.solutions = {
                wall: {
                    standard: ['Genie Clip wall (Standard)', 'Independent Wall (Standard)', 'Resilient bar wall (Standard)', 'M20 Solution (Standard)'],
                    premium: ['Genie Clip wall (SP15 Soundboard Upgrade)', 'Independent Wall (SP15 Soundboard Upgrade)', 'Resilient bar wall (SP15 Soundboard Upgrade)', 'M20 Solution (SP15 Soundboard upgrade)']
                },
                ceiling: {
                    standard: ['Genie Clip ceiling', 'LB3 Genie Clip', 'Independent Ceiling', 'Resilient bar Ceiling'],
                    premium: ['Genie Clip ceiling (SP15 Soundboard Upgrade)', 'LB3 Genie Clip (SP15 Soundboard Upgrade)', 'Independent Ceiling (SP15 Soundboard Upgrade)', 'Resilient bar Ceiling (SP15 Soundboard Upgrade)']
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
                'M20 Solution (Standard)': {
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
                    notes: ['Single layer system with excellent cost-effectiveness']
                },
                'Independent Wall (Standard)': {
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
                    notes: ['Two layers of 12.5mm Sound Plasterboard.']
                },
                'Resilient bar wall (Standard)': {
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
                    notes: ['Single layer system with resilient bars for decoupling']
                },
                'Genie Clip wall (Standard)': {
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
                    notes: ['2 layers of 12.5mm plasterboard for this system.', 'Add 1 box of screws no matter the m².']
                },
                'M20 Solution (SP15 Soundboard upgrade)': {
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
                    notes: ['We only use 1 layer of plasterboard on this system.']
                },
                'Independent Wall (SP15 Soundboard Upgrade)': {
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
                    notes: ['Only one layer of 12.5mm sound plasterboard.']
                },
                'Resilient bar wall (SP15 Soundboard Upgrade)': {
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
                    notes: ['1 layer of 12.5mm Sound Plasterboard']
                },
                'Genie Clip wall (SP15 Soundboard Upgrade)': {
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
                    notes: ['Only 1 layer of 12.5mm plasterboard on this system.']
                },
                'Genie Clip ceiling': {
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
                    notes: ['2 layers of 12.5mm sound plasterboard.']
                },
                'LB3 Genie Clip': {
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
                    notes: ['2 layers of 12.5mm Sound Plasterboard']
                },
                'Independent Ceiling': {
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
                    notes: ['Uses both 19mm plank and 12.5mm sound plasterboard']
                },
                'Resilient bar Ceiling': {
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
                    notes: ['Basic but effective ceiling solution']
                },
                'Genie Clip ceiling (SP15 Soundboard Upgrade)': {
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
                    notes: ['One layer of 12.5mm plasterboard with SP15 upgrade']
                },
                'LB3 Genie Clip (SP15 Soundboard Upgrade)': {
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
                    notes: ['1 layer of 12.5mm Sound Plasterboard with enhanced LB3 system']
                },
                'Independent Ceiling (SP15 Soundboard Upgrade)': {
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
                    notes: ['Enhanced independent system with SP15 upgrade']
                },
                'Resilient bar Ceiling (SP15 Soundboard Upgrade)': {
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
        }

        initialize() {
            if (this.initialized) return;
            this.bindEvents();
            this.initialized = true;
            window.dispatchEvent(new CustomEvent('soundproofingManagerInitialized'));
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
                    this.updateNoiseCharacteristics(e.target.value);
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
                console.log(`Updating recommendations due to ${type} change`);
                this.updateRecommendations(type);
            }, this.updateDebounceTime);
        }

        async updateRecommendations(triggerType) {
            try {
                // Get current form state
                const formState = window.FormState || {};
                const noiseData = formState.noiseData || {};
                const dimensions = formState.dimensions || {};

                // Validate required inputs
                if (!this.validateInputs(noiseData)) {
                    console.log('Insufficient data for recommendations');
                    return;
                }

                // Get noise source surfaces
                const noiseSurfaces = this.getNoiseSourceSurfaces();
                
                // Calculate priority based on multiple factors
                const priority = this.calculateOverallPriority(noiseData);

                // Get recommendations based on comprehensive analysis
                const recommendations = {
                    primary: await this.getPrimarySolutions(noiseData, noiseSurfaces, priority),
                    alternatives: this.getAlternativeSolutions(noiseData, noiseSurfaces, priority),
                    effectiveness: this.calculateOverallEffectiveness(noiseData)
                };

                // Display updated recommendations
                await this.displayRecommendations(recommendations, triggerType);

            } catch (error) {
                console.error('Error updating recommendations:', error);
            }
        }

        validateInputs(noiseData) {
            return noiseData.type && 
                   noiseData.direction && 
                   noiseData.direction.length > 0 && 
                   noiseData.intensity;
        }

        calculateOverallPriority(noiseData) {
            let priorityScore = 0;

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
            priorityScore += noiseTypePriorities[noiseData.type] || 3;

            // Time of day priority
            if (noiseData.time) {
                if (noiseData.time.includes('night')) priorityScore += 3;
                if (noiseData.time.includes('evening')) priorityScore += 2;
                if (noiseData.time.length > 1) priorityScore += 1; // Multiple time periods
            }

            // Intensity priority
            priorityScore += parseInt(noiseData.intensity) || 0;

            // Bass content
            if (this.noiseAssessment.sourceDetails.characteristics.bass_content) {
                priorityScore += 2;
            }

            // Vibration
            if (this.noiseAssessment.sourceDetails.characteristics.vibration) {
                priorityScore += 2;
            }

            // Impact levels
            const impactLevels = this.noiseAssessment.problemAssessment.impact_level;
            priorityScore += (impactLevels.conversation_privacy +
                            impactLevels.sleep_disturbance +
                            impactLevels.concentration_impact) / 3;

            // Room usage priority
            const roomUsagePriorities = {
                'bedroom': 5,
                'studio': 5,
                'office': 4,
                'living_room': 3
            };
            priorityScore += roomUsagePriorities[this.noiseAssessment.roomDetails.usage] || 3;

            // Convert score to priority level
            if (priorityScore >= 12) return 'high';
            if (priorityScore >= 8) return 'medium';
            return 'low';
        }

        async getPrimarySolutions(noiseData, noiseSurfaces, priority) {
            const solutions = {
                walls: [],
                ceiling: null,
                floor: null
            };

            // Get available solutions based on priority
            const wallSolutions = priority === 'high' ? 
                this.solutions.wall.premium : 
                this.solutions.wall.standard;

            const ceilingSolutions = priority === 'high' ? 
                this.solutions.ceiling.premium : 
                this.solutions.ceiling.standard;

            // Process wall solutions if needed
            if (noiseSurfaces.walls.length > 0) {
                for (const wall of noiseSurfaces.walls) {
                    const bestWallSolution = await this.findBestSolution(
                        wallSolutions,
                        noiseData,
                        'wall',
                        wall
                    );
                    if (bestWallSolution) {
                        solutions.walls.push(bestWallSolution);
                    }
                }
            }

            // Process ceiling solution if needed
            if (noiseSurfaces.ceiling) {
                solutions.ceiling = await this.findBestSolution(
                    ceilingSolutions,
                    noiseData,
                    'ceiling'
                );
            }

            // Process floor solution if needed
            if (noiseSurfaces.floor) {
                solutions.floor = {
                    message: this.solutions.floor.message,
                    contactInfo: this.solutions.floor.contactInfo
                };
            }

            return solutions;
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
            const solutionSpecs = this.solutionCharacteristics[solution];
            if (!solutionSpecs) return 0;

            let score = 0;
            const weights = this.calculateDetailedWeights(noiseData, type);

            // Sound reduction effectiveness
            score += (solutionSpecs.soundReduction / 60) * weights.soundReduction;

            // Frequency range match
            const freqMatchScore = this.calculateFrequencyMatch(
                solutionSpecs.frequencyRange,
                this.noiseCharacteristics[noiseData.type]?.frequencyRange || [125, 4000]
            );
            score += freqMatchScore * weights.frequencyMatch;

            // STC rating consideration
            score += (solutionSpecs.stc_rating / 60) * weights.stcRating;

            // Installation and maintenance
            score += (1 - solutionSpecs.installationTime / 3) * weights.installation;
            score += (solutionSpecs.maintenanceRequired === 'low' ? 1 : 0.5) * weights.maintenance;

            // Cost effectiveness (inverse relationship)
            const costScore = 1 - (solutionSpecs.total_cost / 300); // Normalize to max cost
            score += costScore * weights.cost;

            // Special considerations
            if (this.noiseAssessment.sourceDetails.characteristics.bass_content && 
                solutionSpecs.frequencyRange[0] < 100) {
                score += 0.1; // Bonus for good bass handling
            }

            if (this.noiseAssessment.sourceDetails.characteristics.impact_noise && 
                solutionSpecs.impactResistance > 0.8) {
                score += 0.1; // Bonus for impact resistance
            }

            return Math.min(score, 1);
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

        calculateEffectiveness(solution, state) {
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

                // Calculate scores for each wall solution
                solution.walls.forEach(wall => {
                    const specs = this.solutionCharacteristics[wall.solution];
                    const noiseSpecs = this.noiseCharacteristics[state.noiseData.type];

                    scores.acousticPerformance += specs.soundReduction / 70; // Normalize to max 70dB
                    scores.frequencyMatch += this.calculateFrequencyMatch(specs.frequencyRange, noiseSpecs.frequencyRange);
                    scores.costEfficiency += 1 - (specs.cost / 250); // Normalize to max cost
                    scores.installationFeasibility += this.calculateInstallationFeasibility(specs, state);
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
                console.error('Error calculating effectiveness:', error);
                return {
                    overall: 0,
                    breakdown: {
                        acousticPerformance: 0,
                        frequencyMatch: 0,
                        costEfficiency: 0,
                        installationFeasibility: 0
                    }
                };
            }
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

        getPrimarySolution(noiseData, noiseSurfaces, priority, state) {
            try {
                const solutions = {
                walls: [],
                ceiling: null,
                    floor: null
                };

                // Determine solution tier
                const tier = this.determineSolutionTier(noiseData, state?.roomType);

                // Process walls if needed
                if (noiseSurfaces.walls && noiseSurfaces.walls.length > 0) {
                    const availableWallSolutions = tier === 'premium' ? 
                        this.solutions.wall.premium : 
                        this.solutions.wall.standard;

                    for (const wall of noiseSurfaces.walls) {
                        const wallSolution = this.findBestSolution(availableWallSolutions, noiseData, 'wall', wall);
                        if (wallSolution) {
                            solutions.walls.push(wallSolution);
                        }
                    }
                }

                // Process ceiling if needed
            if (noiseSurfaces.ceiling) {
                    const availableCeilingSolutions = tier === 'premium' ? 
                        this.solutions.ceiling.premium : 
                        this.solutions.ceiling.standard;

                    const ceilingSolution = this.findBestSolution(availableCeilingSolutions, noiseData, 'ceiling');
                if (ceilingSolution) {
                        solutions.ceiling = ceilingSolution;
                    }
                }

                // Process floor if needed
            if (noiseSurfaces.floor) {
                    solutions.floor = {
                        message: this.solutions.floor.message,
                        contactInfo: this.solutions.floor.contactInfo
                    };
                }

                return solutions;

            } catch (error) {
                console.error('Error in getPrimarySolution:', error);
                return {
                    walls: [],
                    ceiling: null,
                    floor: null
                };
            }
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

        getWallSolutions(tier, noiseData, context) {
            const solutions = tier === 'premium' ? 
                this.solutions.wall.premium : 
                this.solutions.wall.standard;

            return solutions.map(solutionName => {
                const specs = this.solutionCharacteristics[solutionName];
                const score = this.calculateSolutionScore(solutionName, noiseData, context);
                const reasoning = this.generateSolutionReasoning(solutionName, specs, noiseData);
                
                return {
                    name: solutionName,
                    score,
                    specs,
                    reasoning
                };
            }).sort((a, b) => b.score - a.score);
        }

        getCeilingSolution(tier, noiseData, context) {
            const solutions = tier === 'premium' ? 
                this.solutions.ceiling.premium : 
                this.solutions.ceiling.standard;

            if (!solutions || solutions.length === 0) {
                return null;
            }

            return solutions.map(solutionName => {
                const specs = this.solutionCharacteristics[solutionName];
                const score = this.calculateSolutionScore(solutionName, noiseData, context);
                const reasoning = this.generateSolutionReasoning(solutionName, specs, noiseData);
                
                return {
                    name: solutionName,
                    score,
                    specs,
                    reasoning
                };
            }).sort((a, b) => b.score - a.score)[0]; // Return the highest scored solution
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

        async displayRecommendations(recommendations, triggerType) {
            let container;
            try {
                console.log('Displaying recommendations:', recommendations);
                container = document.getElementById('soundproofing-solutions');
                if (!container) {
                    container = this.createSolutionsContainer();
                }

                let html = '<div class="recommendations">';
                
                if (!recommendations.primary) {
                    html += '<div class="error-message">No recommendations available</div>';
                } else {
                    // Wall Solutions
                    if (recommendations.primary.walls?.length > 0) {
                        html += await this.generateWallSolutionsHtml(recommendations.primary.walls);
                    }

                    // Ceiling Solution
                    if (recommendations.primary.ceiling) {
                        html += await this.generateCeilingSolutionHtml(recommendations.primary.ceiling);
                    }

                    // Floor Solution
                    if (recommendations.primary.floor) {
                        html += this.generateFloorPlaceholderHtml(recommendations.primary.floor);
                    }

                    // Add effectiveness rating
                    if (recommendations.effectiveness) {
                        html += this.generateEffectivenessHtml(recommendations.effectiveness);
                    }
                }

                html += `<div class="update-indicator" data-trigger="${triggerType}">
                    Last updated: ${new Date().toLocaleTimeString()}
                </div>`;

                container.innerHTML = html;

            } catch (error) {
                console.error('Error displaying recommendations:', error);
                if (container) {
                    container.innerHTML = `
                        <div class="error-message">
                            Error displaying recommendations. Please try again.
                        </div>`;
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

        // Helper method to generate solution HTML with detailed breakdown
        generateSolutionHtml(wall, costs) {
            let html = `
                <div class="solution-item">
                    <div class="solution-header">
                        <span class="solution-location">${wall.wall} Wall</span>
                        <span class="solution-name">${wall.solution}</span>
                        <span class="solution-score">Effectiveness: ${(wall.score * 100).toFixed(1)}%</span>
                    </div>
                    <div class="solution-details">
                        ${wall.reasoning.map(reason => `<div class="solution-reason">• ${reason}</div>`).join('')}
                    </div>`;

            if (costs && !costs.error) {
                html += `
                    <div class="cost-breakdown">
                        <h5>Material Breakdown:</h5>
                        <ul>
                            ${costs.costs.map(item => `
                                <li>
                                    <span class="material-name">${item.name}</span>
                                    <span class="material-quantity">${item.quantity} units</span>
                                    <span class="material-cost">£${item.total_cost.toFixed(2)}</span>
                                </li>
                            `).join('')}
                        </ul>
                        <div class="total-cost">
                            <span>Total Cost</span>
                            <span>£${costs.total.toFixed(2)}</span>
                        </div>
                    </div>`;
            }

            html += '</div>';
            return html;
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

        // Update the wall solutions HTML generator
        async generateWallSolutionsHtml(walls) {
            let html = '<div class="primary-solution">';
            html += '<h4>Wall Treatments</h4>';
            
            const dimensions = window.FormState.dimensions;
            const dimensionsValidation = this.validateDimensions(dimensions);
            
            if (!dimensionsValidation.isValid) {
                dimensionsValidation.errors.push('Please enter valid room dimensions');
                return html + `
                    <div class="error-message">
                        Please enter valid room dimensions to see cost breakdown.
                        <ul>
                            ${dimensionsValidation.errors.map(error => `<li>${error}</li>`).join('')}
                        </ul>
                    </div>
                </div>`;
            }

            for (const wall of walls) {
                try {
                    const costs = this.calculateLocalCosts(wall.solution, dimensions, 'wall', wall.wall.toLowerCase());
                    if (costs.error) {
                        throw new Error(costs.message);
                    }
                    html += `
                        <div class="solution-item">
                            <div class="solution-header">
                                <span class="solution-location">${wall.wall} Wall (${costs.area} m²)</span>
                                <span class="solution-name">${wall.solution}</span>
                                <span class="solution-score">Effectiveness: ${(wall.score * 100).toFixed(1)}%</span>
                            </div>
                            <div class="solution-details">
                                ${wall.reasoning.map(reason => `<div class="solution-reason">• ${reason}</div>`).join('')}
                            </div>
                            <div class="material-breakdown">
                                <h5>Materials Required:</h5>
                                <ul>
                                    ${costs.materials.map(material => `
                                        <li>
                                            <span class="material-name">${material.name}</span>
                                            <span class="material-amount">${material.amount} ${material.unit}</span>
                                            <span class="material-cost">£${material.cost.toFixed(2)}</span>
                                        </li>
                                    `).join('')}
                                </ul>
                                <div class="total-cost">Total Cost: £${costs.total.toFixed(2)}</div>
                            </div>
                        </div>`;
                } catch (error) {
                    console.error('Error generating wall solution HTML:', error);
                    html += `
                        <div class="error-message">
                            Error calculating costs for ${wall.solution}. Please try again.
                        </div>`;
                }
            }

            html += '</div>';
            return html;
        }

        // Update the ceiling solution HTML generator
        async generateCeilingSolutionHtml(ceiling) {
            try {
                const dimensions = window.FormState.dimensions;
                const costs = this.calculateLocalCosts(ceiling.solution, dimensions);
                if (costs.error) {
                    throw new Error(costs.message);
                }
                return `
                    <div class="solution-item">
                        <div class="solution-header">
                            <span class="solution-name">${ceiling.solution}</span>
                            <span class="solution-score">Effectiveness: ${(ceiling.score * 100).toFixed(1)}%</span>
                        </div>
                        <div class="solution-details">
                            ${ceiling.reasoning.map(reason => `<div class="solution-reason">• ${reason}</div>`).join('')}
                        </div>
                        <div class="material-breakdown">
                            <h5>Materials Required:</h5>
                            <ul>
                                ${costs.materials.map(material => `
                                    <li>
                                        <span class="material-name">${material.name}</span>
                                        <span class="material-amount">${material.amount} ${material.unit}</span>
                                        <span class="material-cost">£${material.cost.toFixed(2)}</span>
                                    </li>
                                `).join('')}
                            </ul>
                            <div class="total-cost">Total Cost: £${costs.total.toFixed(2)}</div>
                        </div>
                    </div>`;
            } catch (error) {
                console.error('Error generating ceiling solution HTML:', error);
                return `
                    <div class="error-message">
                        Error calculating costs for ${ceiling.solution}. Please try again.
                    </div>`;
            }
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
        calculateLocalCosts(solution, dimensions, surfaceType = 'wall', wall = null) {
            const solutionData = this.solutionCharacteristics[solution];
            if (!solutionData || !solutionData.materials) {
                return {
                    error: true,
                    message: 'Solution data not found'
                };
            }

            // Calculate the correct area based on surface type and wall
            let area;
            if (surfaceType === 'wall') {
                if (wall === 'north' || wall === 'south') {
                    area = dimensions.width * dimensions.height;
                } else if (wall === 'east' || wall === 'west') {
                    area = dimensions.length * dimensions.height;
                }
            } else if (surfaceType === 'ceiling' || surfaceType === 'floor') {
                area = dimensions.length * dimensions.width;
            }

            if (!area) {
                return {
                    error: true,
                    message: 'Invalid surface type or dimensions'
                };
            }

            const materials = solutionData.materials.map(material => {
                let quantity;
                if (material.coverage === '1') {
                    // For items sold as single units (like clips, channels, etc.)
                    if (material.name.toLowerCase().includes('clip')) {
                        quantity = Math.ceil(area * 0.7); // Approximately 0.7 clips per m²
                    } else if (material.name.toLowerCase().includes('channel') || 
                             material.name.toLowerCase().includes('bar')) {
                        quantity = Math.ceil(area * 0.5); // Approximately 0.5 channels/bars per m²
                    } else if (material.name.toLowerCase().includes('screw') || 
                             material.name.toLowerCase().includes('fixing')) {
                        quantity = Math.ceil(area * 8); // Approximately 8 screws per m²
                    } else {
                        quantity = Math.ceil(area / 20); // Default for other unit items
                    }
                } else {
                    // For materials sold by area
                    quantity = Math.ceil(area / parseFloat(material.coverage));
                }

                const totalCost = material.cost * quantity;
                return {
                    name: material.name,
                    amount: quantity.toFixed(0), // Round to whole units
                    unit: material.coverage === '1' ? 'unit(s)' : 'm²',
                    cost: totalCost
                };
            });

            const total = materials.reduce((sum, material) => sum + material.cost, 0);

            return {
                materials,
                total,
                area: area.toFixed(2),
                error: false
            };
        }

        bindDynamicUpdates() {
            // Listen for form state updates
            window.addEventListener('formStateUpdated', (event) => {
                const { detail } = event;
                console.log('Form state updated:', detail);
                this.handleFormUpdate('formState');
            });

            // Listen for blockage updates
            window.addEventListener('blockagesUpdated', (event) => {
                const { detail } = event;
                console.log('Blockages updated:', detail);
                this.handleFormUpdate('blockages');
            });

            // Listen for dimensions updates
            window.addEventListener('dimensionsUpdated', (event) => {
                const { detail } = event;
                console.log('Dimensions updated:', detail);
                this.handleFormUpdate('dimensions');
            });

            // Listen for noise data updates
            window.addEventListener('noiseDataUpdated', (event) => {
                const { detail } = event;
                console.log('Noise data updated:', detail);
                this.handleFormUpdate('noise');
            });
        }

        // Add this method to the SoundproofingManager class
        generateFloorPlaceholderHtml(floor) {
            return `
                <div class="solution-item floor-placeholder">
                    <div class="solution-header">
                        <span class="solution-location">Floor Treatment</span>
                    </div>
                    <div class="solution-details">
                        <div class="solution-reason info-message">
                            ${floor.message}
                        </div>
                        <div class="solution-note">
                            • Contact our specialists for custom floor solutions
                            • We'll analyze your specific requirements
                            • Get a detailed quote for your floor treatment
                        </div>
                    </div>
                </div>`;
        }

        updateNoiseCharacteristics(noiseType) {
            const characteristics = this.noiseCharacteristics[noiseType];
            if (characteristics) {
                this.noiseAssessment.sourceDetails.characteristics.bass_content = characteristics.bassHeavy || false;
                this.noiseAssessment.sourceDetails.characteristics.vibration = characteristics.impactComponent || false;
                this.noiseAssessment.sourceDetails.characteristics.impact_noise = characteristics.impactComponent || false;
            }
        }

        calculateOverallEffectiveness(noiseData) {
            try {
                // Get noise characteristics
                const noiseSpecs = this.noiseCharacteristics[noiseData.type];
                if (!noiseSpecs) return { overall: 0, breakdown: {} };

                // Initialize effectiveness components
                const components = {
                    soundReduction: 0,
                    frequencyMatch: 0,
                    impactControl: 0,
                    bassHandling: 0,
                    roomCoverage: 0
                };

                // Calculate sound reduction effectiveness
                const intensity = parseInt(noiseData.intensity) || 3;
                const requiredReduction = noiseSpecs.typicalIntensity * (intensity / 5);
                
                // Get all active solutions
                const activeSolutions = this.getNoiseSourceSurfaces();
                let totalSolutions = 0;
                let totalScore = 0;

                // Process wall solutions
                if (activeSolutions.walls.length > 0) {
                    activeSolutions.walls.forEach(wall => {
                        const solution = this.findBestSolutionForWall(wall, noiseData);
                        if (solution) {
                            const specs = this.solutionCharacteristics[solution];
                            if (specs) {
                                components.soundReduction += specs.soundReduction / requiredReduction;
                                components.frequencyMatch += this.calculateFrequencyMatch(
                                    specs.frequencyRange,
                                    noiseSpecs.frequencyRange
                                );
                                if (specs.impactResistance > 0.7) components.impactControl += 1;
                                if (specs.frequencyRange[0] < 100) components.bassHandling += 1;
                                totalSolutions++;
                                totalScore += this.calculateSolutionScore(solution, noiseData, {});
                            }
                        }
                    });
                }

                // Process ceiling solution
                if (activeSolutions.ceiling) {
                    const ceilingSolution = this.findBestCeilingSolution(noiseData);
                    if (ceilingSolution) {
                        const specs = this.solutionCharacteristics[ceilingSolution];
                        if (specs) {
                            components.soundReduction += specs.soundReduction / requiredReduction;
                            components.frequencyMatch += this.calculateFrequencyMatch(
                                specs.frequencyRange,
                                noiseSpecs.frequencyRange
                            );
                            if (specs.impactResistance > 0.7) components.impactControl += 1;
                            if (specs.frequencyRange[0] < 100) components.bassHandling += 1;
                            totalSolutions++;
                            totalScore += this.calculateSolutionScore(ceilingSolution, noiseData, {});
                        }
                    }
                }

                // Normalize components
                if (totalSolutions > 0) {
                    Object.keys(components).forEach(key => {
                        components[key] = components[key] / totalSolutions;
                    });
                }

                // Calculate room coverage
                const surfaces = this.getNoiseSourceSurfaces();
                const totalSurfaces = surfaces.walls.length + (surfaces.ceiling ? 1 : 0) + (surfaces.floor ? 1 : 0);
                components.roomCoverage = totalSurfaces / (surfaces.walls.length + 2); // +2 for ceiling and floor

                // Calculate overall effectiveness
                const weights = {
                    soundReduction: 0.35,
                    frequencyMatch: 0.25,
                    impactControl: 0.15,
                    bassHandling: 0.15,
                    roomCoverage: 0.10
                };

                const overall = Object.entries(components).reduce((sum, [key, value]) => {
                    return sum + (value * weights[key]);
                }, 0);

                return {
                    overall: Math.min(overall, 1),
                    breakdown: components
                };

            } catch (error) {
                console.error('Error calculating overall effectiveness:', error);
                return {
                    overall: 0,
                    breakdown: {}
                };
            }
        }

        findBestSolutionForWall(wall, noiseData) {
            const priority = this.calculateOverallPriority(noiseData);
            const solutions = priority === 'high' ? 
                this.solutions.wall.premium : 
                this.solutions.wall.standard;
            
            let bestScore = 0;
            let bestSolution = null;

            solutions.forEach(solution => {
                const score = this.calculateSolutionScore(solution, noiseData, {});
                if (score > bestScore) {
                    bestScore = score;
                    bestSolution = solution;
                }
            });

            return bestSolution;
        }

        findBestCeilingSolution(noiseData) {
            const priority = this.calculateOverallPriority(noiseData);
            const solutions = priority === 'high' ? 
                this.solutions.ceiling.premium : 
                this.solutions.ceiling.standard;
            
            let bestScore = 0;
            let bestSolution = null;

            solutions.forEach(solution => {
                const score = this.calculateSolutionScore(solution, noiseData, {});
                if (score > bestScore) {
                    bestScore = score;
                    bestSolution = solution;
                }
            });

            return bestSolution;
        }

        calculateSpaceEfficiency(solution, roomContext) {
            // Base efficiency score based on solution thickness
            let score = 1 - (solution.thickness / 0.3); // Normalize to max reasonable thickness of 300mm

            // Adjust for room dimensions if available
            if (roomContext && roomContext.dimensions) {
                const { width, length, height } = roomContext.dimensions;
                
                // Penalize if room is small and solution is thick
                const roomVolume = width * length * height;
                if (roomVolume < 30 && solution.thickness > 0.15) { // 30 cubic meters as small room threshold
                    score *= 0.8;
                }
                
                // Penalize if ceiling height is low and solution is thick
                if (height < 2.4 && solution.thickness > 0.1) { // 2.4m as standard ceiling height
                    score *= 0.9;
                }
            }

            // Bonus for solutions with good space efficiency
            if (solution.thickness < 0.1) { // Less than 100mm
                score *= 1.2;
            }

            return Math.min(Math.max(score, 0), 1); // Ensure score is between 0 and 1
        }

        generateSummaryHtml() {
            const noiseData = window.FormState?.noiseData || {};
            const dimensions = window.FormState?.dimensions || {};
            const blockages = window.FormState?.blockages || {};
            
            let html = '<div class="calculator-section review-section">';
            
            // Project Summary
            html += '<div class="summary-group">';
            html += '<h3 class="section-header">Project Summary</h3>';
            html += '<div class="summary-content">';
            html += `
                <div class="info-grid">
                    <div class="info-item">
                        <label>Noise Type:</label>
                        <span class="value">${this.formatValue(noiseData.type)}</span>
                    </div>
                    <div class="info-item">
                        <label>Intensity:</label>
                        <span class="value">Level ${this.formatValue(noiseData.intensity)}</span>
                    </div>
                    <div class="info-item">
                        <label>Time:</label>
                        <span class="value">${this.formatArrayValue(noiseData.time)}</span>
                    </div>
                    <div class="info-item">
                        <label>Direction:</label>
                        <span class="value">${this.formatArrayValue(noiseData.direction)}</span>
                    </div>
                </div>
            `;
            html += '</div></div>';

            // Room Dimensions
            html += '<div class="summary-group">';
            html += '<h3 class="section-header">Room Dimensions</h3>';
            html += '<div class="summary-content">';
            html += `
                <div class="dimensions-grid">
                    <div class="dimension-item">
                        <label>Length:</label>
                        <span class="value">${this.formatDimension(dimensions.length)} m</span>
                    </div>
                    <div class="dimension-item">
                        <label>Width:</label>
                        <span class="value">${this.formatDimension(dimensions.width)} m</span>
                    </div>
                    <div class="dimension-item">
                        <label>Height:</label>
                        <span class="value">${this.formatDimension(dimensions.height)} m</span>
                    </div>
                </div>
            `;
            html += '</div></div>';

            // Surface Features
            html += '<div class="summary-group">';
            html += '<h3 class="section-header">Surface Features</h3>';
            html += '<div class="summary-content">';
            
            if (this.hasAnyBlockages(blockages)) {
                html += '<div class="features-grid">';
                
                // Wall features
                if (blockages.wall?.length > 0) {
                    html += '<div class="feature-category"><h4>Wall Features</h4>';
                    blockages.wall.forEach(blockage => {
                        if (blockage?.type && blockage?.wall) {
                            html += `
                                <div class="feature-item">
                                    <label>${blockage.wall} Wall:</label>
                                    <span class="value">${blockage.type} (${blockage.width}m × ${blockage.height}m)</span>
                                </div>`;
                        }
                    });
                    html += '</div>';
                }

                // Ceiling features
                if (blockages.ceiling?.length > 0) {
                    html += '<div class="feature-category"><h4>Ceiling Features</h4>';
                    blockages.ceiling.forEach(blockage => {
                        if (blockage?.type) {
                            html += `
                                <div class="feature-item">
                                    <label>Feature:</label>
                                    <span class="value">${blockage.type} (${blockage.width}m × ${blockage.length}m)</span>
                                </div>`;
                        }
                    });
                    html += '</div>';
                }

                // Floor features
                if (blockages.floor?.length > 0) {
                    html += '<div class="feature-category"><h4>Floor Features</h4>';
                    blockages.floor.forEach(blockage => {
                        if (blockage?.type) {
                            html += `
                                <div class="feature-item">
                                    <label>Feature:</label>
                                    <span class="value">${blockage.type} (${blockage.width}m × ${blockage.length}m)</span>
                                </div>`;
                        }
                    });
                    html += '</div>';
                }
                
                html += '</div>';
            } else {
                html += '<div class="no-features">No surface features reported</div>';
            }
            html += '</div></div>';

            // Cost Summary
            html += '<div class="summary-group">';
            html += '<h3 class="section-header">Cost Summary</h3>';
            html += '<div class="summary-content costs-container">';
            
            try {
                const noiseSurfaces = this.getNoiseSourceSurfaces();
                let totalCost = 0;
                let costBreakdown = [];

                // Calculate costs for each surface
                if (noiseSurfaces.walls?.length > 0) {
                    noiseSurfaces.walls.forEach(wall => {
                        const solution = this.findBestSolutionForWall(wall, noiseData);
                        if (solution) {
                            const costs = this.calculateLocalCosts(solution, dimensions, 'wall', wall.toLowerCase());
                            if (!costs.error) {
                                totalCost += costs.total;
                                costBreakdown.push({
                                    surface: wall,
                                    solution: solution,
                                    cost: costs.total,
                                    area: costs.area,
                                    materials: costs.materials
                                });
                            }
                        }
                    });
                }

                if (noiseSurfaces.ceiling) {
                    const solution = this.findBestCeilingSolution(noiseData);
                    if (solution) {
                        const costs = this.calculateLocalCosts(solution, dimensions, 'ceiling');
                        if (!costs.error) {
                            totalCost += costs.total;
                            costBreakdown.push({
                                surface: 'Ceiling',
                                solution: solution,
                                cost: costs.total,
                                area: costs.area,
                                materials: costs.materials
                            });
                        }
                    }
                }

                // Display cost breakdown
                costBreakdown.forEach(item => {
                    html += `
                        <div class="cost-section">
                            <div class="cost-header">
                                <span class="surface">${item.surface}</span>
                                <span class="area">${item.area.toFixed(2)} m²</span>
                                <span class="solution">${item.solution}</span>
                            </div>
                            <div class="materials-list">
                                ${item.materials.map(material => `
                                    <div class="material-item">
                                        <span class="name">${material.name}</span>
                                        <span class="amount">${material.amount} ${material.unit}</span>
                                        <span class="cost">£${material.cost.toFixed(2)}</span>
                                    </div>
                                `).join('')}
                            </div>
                            <div class="surface-total">
                                <label>Surface Total:</label>
                                <span class="cost">£${item.cost.toFixed(2)}</span>
                            </div>
                        </div>`;
                });

                // Blockage adjustment
                const blockageAdjustment = this.calculateBlockageAdjustment(blockages);
                if (blockageAdjustment > 0) {
                    const adjustmentAmount = totalCost * blockageAdjustment;
                    html += `
                        <div class="adjustment-section">
                            <div class="adjustment-item">
                                <label>Blockage Adjustment (+${(blockageAdjustment * 100).toFixed(0)}%):</label>
                                <span class="cost">£${adjustmentAmount.toFixed(2)}</span>
                            </div>
                        </div>`;
                    totalCost += adjustmentAmount;
                }

                // Total cost
                html += `
                    <div class="total-section">
                        <div class="total-cost">
                            <label>Total Estimated Cost:</label>
                            <span class="cost">£${totalCost.toFixed(2)}</span>
                        </div>
                    </div>`;

            } catch (error) {
                console.error('Error calculating costs:', error);
                html += '<div class="error-message">Error calculating costs. Please check your inputs.</div>';
            }

            html += '</div></div>';

            // Add quote button
            html += `
                <div class="quote-section">
                    <button type="button" class="quote-button" onclick="window.workflowManager.generateQuote()">
                        Download Detailed Quote
                    </button>
                </div>`;

            html += '</div>';
            return html;
        }

        // Helper methods for formatting
        formatValue(value) {
            return value || 'Not specified';
        }

        formatArrayValue(arr) {
            return Array.isArray(arr) && arr.length > 0 ? arr.join(', ') : 'Not specified';
        }

        formatDimension(value) {
            return value ? `${value.toFixed(2)} meters` : '0 meters';
        }

        hasAnyBlockages(blockages) {
            return ['wall', 'ceiling', 'floor'].some(type => 
                blockages[type] && Array.isArray(blockages[type]) && blockages[type].length > 0
            );
        }

        calculateBlockageAdjustment(blockages) {
            try {
                if (!blockages || typeof blockages !== 'object') {
                    return 0;
                }

                let totalAdjustment = 0;
                const processBlockageType = (type) => {
                    if (!type || typeof type !== 'string') {
                        return 0;
                    }
                    
                    const typeStr = type.toLowerCase();
                    // Adjustment percentages for different blockage types
                    if (typeStr.includes('window')) return 0.15;
                    if (typeStr.includes('door')) return 0.20;
                    if (typeStr.includes('pipe')) return 0.10;
                    if (typeStr.includes('vent')) return 0.25;
                    if (typeStr.includes('electrical')) return 0.05;
                    return 0;
                };

                // Process wall blockages
                if (Array.isArray(blockages.wall)) {
                    blockages.wall.forEach(blockage => {
                        if (blockage && typeof blockage === 'object' && blockage.type) {
                            totalAdjustment += processBlockageType(blockage.type);
                        }
                    });
                }

                // Process ceiling blockages
                if (Array.isArray(blockages.ceiling)) {
                    blockages.ceiling.forEach(blockage => {
                        if (blockage && typeof blockage === 'object' && blockage.type) {
                            totalAdjustment += processBlockageType(blockage.type);
                        }
                    });
                }

                // Process floor blockages
                if (Array.isArray(blockages.floor)) {
                    blockages.floor.forEach(blockage => {
                        if (blockage && typeof blockage === 'object' && blockage.type) {
                            totalAdjustment += processBlockageType(blockage.type);
                        }
                    });
                }

                // Cap the total adjustment at 50%
                return Math.min(totalAdjustment, 0.5);
            } catch (error) {
                console.error('Error calculating blockage adjustment:', error);
                return 0;
            }
        }
    }

    window.SoundproofingManager = SoundproofingManager;
}

// Initialize manager
if (!window.soundproofingManager) {
    window.soundproofingManager = new SoundproofingManager();
    window.soundproofingManager.initialize();
}

// Helper function for fetching costs
async function fetchSolutionCosts(solution, dimensions) {
    try {
        // Get CSRF token from meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
        if (!csrfToken) {
            throw new Error('CSRF token not found');
        }

        // Validate dimensions
        const validatedDimensions = validateDimensions(dimensions);
        if (!validatedDimensions.isValid) {
            console.warn('Invalid dimensions:', validatedDimensions.errors);
            return {
                error: 'Please enter valid room dimensions before calculating costs',
                costs: [],
                total: 0
            };
        }

        try {
            const response = await fetch('http://192.168.1.41:10000/api/calculate-costs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    solution: solution,
                    dimensions: validatedDimensions.dimensions
                })
            });
            
            if (!response.ok) {
                // Log the error response for debugging
                const errorText = await response.text();
                console.warn('Backend error:', response.status, errorText);
                return generatePlaceholderCosts(solution, validatedDimensions.dimensions);
            }

            const data = await response.json();
            return {
                costs: data.costs || [],
                total: data.total || 0
            };

        } catch (error) {
            console.warn('Backend error:', error);
            return generatePlaceholderCosts(solution, validatedDimensions.dimensions);
        }

    } catch (error) {
        console.error('Error in fetchSolutionCosts:', error);
        return {
            error: error.message,
            costs: [],
            total: 0
        };
    }
}

// Add helper function to generate placeholder costs
function generatePlaceholderCosts(solution, dimensions) {
    // Calculate area
    const area = dimensions.length * dimensions.width;
    
    // Basic placeholder data with proper coverage values
    const baseCosts = {
        'standard': {
            materials: [
                { name: 'Acoustic Panels', rate: 45, coverage: 2.88 },  // Each panel covers 2.88m²
                { name: 'Sound Barrier', rate: 35, coverage: 2.88 },    // Each barrier covers 2.88m²
                { name: 'Installation Materials', rate: 15, coverage: 8.64 }  // Each pack covers 8.64m²
            ],
            laborRate: 40
        },
        'premium': {
            materials: [
                { name: 'Premium Acoustic Panels', rate: 75, coverage: 2.88 },
                { name: 'High-Mass Barrier', rate: 55, coverage: 2.88 },
                { name: 'Professional Installation Kit', rate: 25, coverage: 8.64 }
            ],
            laborRate: 60
        }
    };

    const tier = solution.toLowerCase().includes('premium') ? 'premium' : 'standard';
    const costs = baseCosts[tier].materials.map(material => {
        const unitsNeeded = Math.ceil(area / material.coverage);
        return {
            name: material.name,
            quantity: unitsNeeded,
            rate: material.rate,
            total_cost: Math.ceil(unitsNeeded * material.rate)
        };
    });

    // Add labor cost (1 unit per 10m²)
    const laborUnits = Math.ceil(area / 10);
    costs.push({
        name: 'Installation Labor',
        quantity: laborUnits,
        rate: baseCosts[tier].laborRate,
        total_cost: Math.ceil(laborUnits * baseCosts[tier].laborRate)
    });

    const total = costs.reduce((sum, item) => sum + item.total_cost, 0);

    return {
        costs,
        total,
        isPlaceholder: true
    };
}

// Add dimension validation helper
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