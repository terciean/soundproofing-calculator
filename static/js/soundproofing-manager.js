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
                    notes: ['We only use 1 layer of plasterboard on this system.']
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
                    notes: ['Only 1 layer of 12.5mm plasterboard on this system.']
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
                    notes: ['Two layers of 12.5mm Sound Plasterboard.']
                },
                'Independent Wall (SP15 Soundboard Upgrade)': {
                    soundReduction: 55,
                    frequencyRange: [63, 8000],
                    materials: [
                        {name: 'Metal Frame Work', cost: 12.65, coverage: '1'},
                        {name: 'Rockwool RWA45 50mm', cost: 50.2, coverage: '8.64'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Tecsound 50', cost: 59.5, coverage: '7.2'},
                        {name: '1 box screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'},
                        {name: 'SP15 Soundboard', cost: 22.95, coverage: '1'}
                    ],
                    total_cost: 264.15,
                    notes: ['Only one layer of 12.5mm sound plasterboard.']
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
                    total_cost: 124.16
                },
                'Resilient bar wall (SP15 Soundboard Upgrade)': {
                    soundReduction: 53,
                    frequencyRange: [80, 5000],
                    materials: [
                        {name: 'Rockwool RW3 100mm', cost: 42.95, coverage: '2.88'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'SP15 Soundboard', cost: 22.95, coverage: '1'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 184.75,
                    notes: ['Only one layer of 12.5mm sound plasterboard.']
                },
                'M20 Solution (Standard)': {
                    soundReduction: 45,
                    frequencyRange: [125, 4000],
                    materials: [
                        {name: 'M20 Rubber wall panel', cost: 23.95, coverage: '1'},
                        {name: 'M20 adhesive', cost: 5.95, coverage: '1'},
                        {name: 'Acoustic Mastic', cost: 12.35, coverage: '2'},
                        {name: '12.5mm Sound plasterboard', cost: 18.45, coverage: '2.88'}
                    ],
                    total_cost: 60.7
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
                    notes: ['2 layers of 12.5mm sound plasterboard.']
                },
                'Genie Clip ceiling (SP15 Soundboard Upgrade)': {
                    soundReduction: 56,
                    frequencyRange: [70, 5500],
                    materials: [
                        {name: 'Genie Clip', cost: 3.4, coverage: '0.25'},
                        {name: 'Furring Channel', cost: 4.45, coverage: '0.50'},
                        {name: 'Resilient bar', cost: 4.2, coverage: '1'},
                        {name: 'Rockwool RWA45 50mm', cost: 50.2, coverage: '8.64'},
                        {name: '12.5mm Sound Plasterboard', cost: 18.45, coverage: '2.88'},
                        {name: 'SP15 Soundboard', cost: 22.95, coverage: '1'},
                        {name: 'Acoustic Sealant', cost: 12.35, coverage: '3'},
                        {name: 'Screws', cost: 16.21, coverage: '30'},
                        {name: 'Floor protection', cost: 30, coverage: '30'}
                    ],
                    total_cost: 162.21,
                    notes: ['One layer of 12.5mm plasterboard']
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
                    notes: ['2 layers of 12.5mm Sound Plasterboard']
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
                    notes: ['1 layer of 12.5mm Sound Plasterboard']
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
                    total_cost: 174.66
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
                    total_cost: 182.11
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
                    total_cost: 124.16
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
                    total_cost: 147.11
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
            // Noise type changes
            const noiseTypeSelect = document.getElementById('noise-type');
            if (noiseTypeSelect) {
                noiseTypeSelect.addEventListener('change', () => this.handleFormUpdate('noise-type'));
            }

            // Noise intensity changes
            const intensitySlider = document.getElementById('noise-intensity');
            if (intensitySlider) {
                intensitySlider.addEventListener('input', () => this.handleFormUpdate('intensity'));
            }

            // Time checkboxes
            document.querySelectorAll('input[name="noise-time"]').forEach(checkbox => {
                checkbox.addEventListener('change', () => this.handleFormUpdate('time'));
            });

            // Direction checkboxes
            document.querySelectorAll('input[name="noise-direction"]').forEach(checkbox => {
                checkbox.addEventListener('change', () => this.handleFormUpdate('direction'));
            });
        }

        bindDimensionInputs() {
            ['length', 'width', 'height'].forEach(dim => {
                const input = document.getElementById(dim);
                if (input) {
                    input.addEventListener('input', () => this.handleFormUpdate('dimensions'));
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

        updateRecommendations(triggerType) {
            try {
                const noiseData = window.FormState.noiseData;
                const noiseSurfaces = this.getNoiseSourceSurfaces();
                const noisePriority = this.getNoisePriority();
                
                // Get current form state with all relevant data
                const currentState = {
                    dimensions: window.FormState.dimensions,
                    blockages: window.FormState.blockages,
                    noiseData: noiseData,
                    roomType: window.FormState.roomType,
                    surfaceFeatures: window.FormState.surfaces
                };

                console.log('Updating recommendations with state:', currentState);
                
                // Generate recommendations based on current state
                const recommendations = {
                    primary: this.getPrimarySolution(noiseData, noiseSurfaces, noisePriority, currentState),
                    alternatives: this.getAlternativeSolutions(noiseData, noiseSurfaces, noisePriority, currentState)
                };

                // Calculate effectiveness dynamically
                recommendations.effectiveness = this.calculateEffectiveness(recommendations.primary, currentState);

                // Update the display
                this.displayRecommendations(recommendations, triggerType);

                // Notify other components
                window.dispatchEvent(new CustomEvent('recommendationsUpdated', {
                    detail: {
                        recommendations,
                        triggerType,
                        state: currentState
                    }
                }));

            } catch (error) {
                console.error('Error updating recommendations:', error);
                window.errorUtils?.displayError('Failed to update recommendations');
            }
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

        getPrimarySolution(noiseData, noiseSurfaces, priority, state = {}) {
            const roomContext = {
                dimensions: state.dimensions || { width: 0, length: 0, height: 0 },
                blockages: state.blockages || {},
                areas: this.calculateAreas(state.dimensions || {}),
                roomType: state.roomType || 'default'
            };

            const solution = {
                walls: [],
                ceiling: null,
                floor: null,
                reasoning: []
            };

            if (!noiseData || !noiseSurfaces) {
                solution.reasoning.push('Please provide noise information to get recommendations');
                return solution;
            }

            // Get solution tier based on all factors
            const solutionTier = this.determineSolutionTier(noiseData, priority, state);

            // Handle walls
            if (noiseSurfaces.walls.length > 0) {
                const wallSolutions = this.getWallSolutions(solutionTier, noiseData, roomContext);
                noiseSurfaces.walls.forEach(wall => {
                    const bestSolution = wallSolutions[0]; // Get the highest scored solution
                    if (bestSolution) {
                        solution.walls.push({
                            wall,
                            solution: bestSolution.name,
                            score: bestSolution.score,
                            specs: bestSolution.specs,
                            reasoning: this.generateWallReasoning(bestSolution, wall, noiseData, state)
                        });
                    }
                });
            }

            // Handle ceiling
            if (noiseSurfaces.ceiling) {
                const ceilingSolution = this.getCeilingSolution(solutionTier, noiseData, roomContext);
                if (ceilingSolution) {
                    solution.ceiling = {
                        solution: ceilingSolution.name,
                        score: ceilingSolution.score,
                        specs: ceilingSolution.specs,
                        reasoning: this.generateCeilingReasoning(ceilingSolution, noiseData, state)
                    };
                }
            }

            // Handle floor - add placeholder message
            if (noiseSurfaces.floor) {
                solution.floor = {
                    isPlaceholder: true,
                    message: 'Floor solutions are currently under development. Please contact us for floor treatment recommendations.'
                };
            }

            return solution;
        }

        determineSolutionTier(noiseData, priority, state) {
            let score = 0;

            // Noise intensity factor (0-5)
            score += (noiseData.intensity / 5) * 2;

            // Time factor
            if (noiseData.time.includes('night')) score += 1;
            if (noiseData.time.length > 2) score += 0.5;

            // Room type factor
            const sensitiveRooms = ['studio', 'practice-room', 'media-room'];
            if (sensitiveRooms.includes(state.roomType)) score += 1;

            // Surface features factor
            if (state.surfaceFeatures?.size > 0) score += 0.5;

            // Blockages factor
            const hasBlockages = Object.values(state.blockages).some(b => b.length > 0);
            if (hasBlockages) score += 0.5;

            // Return tier based on score
            if (score >= 3) return 'premium';
            if (score >= 2) return 'standard-plus';
            return 'standard';
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
                'M20WallStandard': 'Standard double-layer solution with excellent cost-effectiveness',
                'GenieClipWallStandard': 'Premium isolation using specialized clip system',
                'ResilientBarWallStandard': 'Effective decoupling using resilient bars',
                'IndependentWallStandard': 'Maximum isolation with independent wall construction',
                'M20WallSP15': 'Enhanced performance with SP15 sound board',
                'GenieClipWallSP15': 'Maximum performance clip system with SP15',
                'ResilientBarWallSP15': 'Enhanced bar system with SP15 upgrade',
                'IndependentWallSP15': 'Premium independent wall with SP15 enhancement',
                'ResilientBarCeilingStandard': 'Standard ceiling isolation system',
                'ResilientBarCeilingSP15': 'Enhanced ceiling system with SP15'
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
            const noiseSpecs = this.noiseCharacteristics[criteria.noiseType] || this.noiseCharacteristics['speech']; // Default to speech
            
            if (!solutionSpecs) {
                console.warn(`No specifications found for solution: ${solution}`);
                return 0;
            }

            const scores = {
                acousticPerformance: this.calculateAcousticScore(solutionSpecs, noiseSpecs, criteria.intensity),
                frequencyMatch: this.calculateFrequencyMatch(solutionSpecs.frequencyRange, noiseSpecs.frequencyRange),
                spaceEfficiency: this.calculateSpaceEfficiency(solutionSpecs, roomContext),
                costEffectiveness: this.calculateCostEffectiveness(solutionSpecs, criteria.intensity),
                installationSuitability: this.calculateInstallationSuitability(solutionSpecs, roomContext),
                durabilityMatch: this.calculateDurabilityMatch(solutionSpecs, criteria)
            };

            const weights = {
                acousticPerformance: 0.35,
                frequencyMatch: 0.20,
                spaceEfficiency: 0.15,
                costEffectiveness: 0.10,
                installationSuitability: 0.10,
                durabilityMatch: 0.10
            };

            return Object.entries(scores).reduce((total, [criterion, score]) => {
                return total + (score * weights[criterion]);
            }, 0);
        }

        calculateAcousticScore(solution, noise, intensity) {
            const requiredReduction = this.calculateRequiredReduction(noise.typicalIntensity, intensity);
            const performanceRatio = solution.soundReduction / requiredReduction;
            return Math.min(Math.max(performanceRatio, 0), 1);
        }

        calculateRequiredReduction(baseNoise, intensity) {
            const intensityFactor = intensity / 3; // Normalize intensity (1-5 scale)
            return baseNoise * intensityFactor;
        }

        calculateFrequencyMatch(solutionRange, noiseRange) {
            const overlap = Math.min(solutionRange[1], noiseRange[1]) - 
                           Math.max(solutionRange[0], noiseRange[0]);
            const noiseSpan = noiseRange[1] - noiseRange[0];
            return Math.max(0, overlap / noiseSpan);
        }

        calculateSpaceEfficiency(solution, roomContext) {
            const availableSpace = roomContext.dimensions.width * 0.1; // Assume 10% of room width is available
            return Math.min(availableSpace / solution.thickness, 1);
        }

        calculateCostEffectiveness(solution, intensity) {
            const cost = solution.cost;
            const intensityFactor = intensity / 3; // Normalize intensity (1-5 scale)
            return Math.min(Math.max(1 - (intensityFactor / cost), 0), 1);
        }

        calculateInstallationSuitability(solution, roomContext) {
            const blockages = roomContext.blockages;
            let suitability = 1;

            // Check if blockages might interfere with installation
            if (blockages.wall && blockages.wall.length > 0) {
                suitability *= 0.8;
            }
            if (blockages.ceiling && blockages.ceiling.length > 0) {
                suitability *= 0.7;
            }

            // Check if room dimensions are suitable
            const dimensions = roomContext.dimensions;
            if (dimensions.height < 2.4) { // Standard ceiling height
                suitability *= 0.9;
            }

            return suitability;
        }

        calculateDurabilityMatch(solution, criteria) {
            const durability = solution.durability;
            const intensityFactor = criteria.intensity / 3; // Normalize intensity (1-5 scale)
            return Math.min(Math.max(1 - (intensityFactor / durability), 0), 1);
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
                                    <span class="material-cost">$${item.total_cost.toFixed(2)}</span>
                                </li>
                            `).join('')}
                        </ul>
                        <div class="total-cost">
                            <span>Total Cost</span>
                            <span>$${costs.total.toFixed(2)}</span>
                        </div>
                    </div>`;
            }

            html += '</div>';
            return html;
        }

        // Add this method to the SoundproofingManager class
        generateEffectivenessHtml(effectiveness) {
            return `
                <div class="effectiveness-rating">
                    <h4>Solution Effectiveness</h4>
                    <div class="effectiveness-score">
                        Overall: ${Math.round(effectiveness.overall * 100)}%
                    </div>
                    <div class="effectiveness-breakdown">
                        <div>Coverage: ${Math.round(effectiveness.breakdown.acousticPerformance * 100)}%</div>
                        <div>Frequency Match: ${Math.round(effectiveness.breakdown.frequencyMatch * 100)}%</div>
                        <div>Cost Efficiency: ${Math.round(effectiveness.breakdown.costEfficiency * 100)}%</div>
                        <div>Installation Feasibility: ${Math.round(effectiveness.breakdown.installationFeasibility * 100)}%</div>
                    </div>
                </div>
            `;
        }

        // Update the wall solutions HTML generator to be async
        async generateWallSolutionsHtml(walls) {
            let html = '<div class="primary-solution">';
            html += '<h4>Wall Treatments</h4>';
            
            const dimensions = window.FormState.dimensions;
            const dimensionsValidation = validateDimensions(dimensions);
            
            if (!dimensionsValidation.isValid) {
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
                    const costs = await fetchSolutionCosts(wall.solution, window.FormState.dimensions);
                    html += `
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
                                            <span class="material-cost">$${item.total_cost.toFixed(2)}</span>
                                        </li>
                                    `).join('')}
                                </ul>
                                <div class="total-cost">
                                    <span>Total Cost</span>
                                    <span>$${costs.total.toFixed(2)}</span>
                                </div>
                            </div>`;
                    }
                    html += '</div>';
                } catch (error) {
                    console.error(`Error generating wall solution HTML for ${wall.wall}:`, error);
                    html += `<div class="error-message">Error loading cost breakdown for ${wall.wall} wall</div>`;
                }
            }
            
            html += '</div>';
            return html;
        }

        // Update the ceiling solution HTML generator to be async
        async generateCeilingSolutionHtml(ceiling) {
            let html = `
                <div class="solution-item">
                    <div class="solution-header">
                        <span class="solution-location">Ceiling Treatment</span>
                        <span class="solution-name">${ceiling.solution}</span>
                        <span class="solution-score">Effectiveness: ${(ceiling.score * 100).toFixed(1)}%</span>
                    </div>
                    <div class="solution-details">
                        ${ceiling.reasoning.map(reason => `<div class="solution-reason">• ${reason}</div>`).join('')}
                    </div>`;

            try {
                const costs = await fetchSolutionCosts(ceiling.solution, window.FormState.dimensions);
                
                if (costs && !costs.error) {
                    html += `
                        <div class="cost-breakdown">
                            <h5>Material Breakdown:</h5>
                            <ul>
                                ${costs.costs.map(item => `
                                    <li>
                                        <span class="material-name">${item.name}</span>
                                        <span class="material-quantity">${item.quantity} units</span>
                                        <span class="material-cost">$${item.total_cost.toFixed(2)}</span>
                                    </li>
                                `).join('')}
                            </ul>
                            <div class="total-cost">
                                <span>Total Cost</span>
                                <span>$${costs.total.toFixed(2)}</span>
                            </div>
                        </div>`;
                }
            } catch (error) {
                console.error('Error fetching ceiling costs:', error);
                html += `<div class="error-message">Error loading cost breakdown</div>`;
            }

            html += '</div>';
            return html;
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