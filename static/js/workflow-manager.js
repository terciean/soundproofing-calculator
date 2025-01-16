if (!window.WorkflowManager) {
    class WorkflowManager {
        constructor() {
            this.initialized = false;
            this.currentStep = 0;
            this.steps = [
                { id: 'room-details', label: 'Room Details' },
                { id: 'noise-details', label: 'Noise Details' },
                { id: 'surface-details', label: 'Surface Features' },
                { id: 'review', label: 'Review' }
            ];
            this.sectionStates = {};
        }

        initialize() {
            if (this.initialized) return;
            this.bindEvents();
            this.showCurrentStep();
            this.initialized = true;
            window.dispatchEvent(new CustomEvent('workflowManagerInitialized'));
        }

        bindEvents() {
            // Progress bar navigation allows direct clicking
            document.querySelectorAll('.progress-step').forEach(step => {
                step.addEventListener('click', (e) => {
                    const stepNum = parseInt(step.dataset.step);
                    if (!isNaN(stepNum)) {
                        this.goToStep(stepNum);
                    }
                });
            });

            // Navigation buttons work without validation
            document.addEventListener('click', (e) => {
                if (e.target.matches('.workflow-navigation button')) {
                    if (e.target.id === 'prev-btn') {
                        this.prevStep();
                    } else if (e.target.id === 'next-btn') {
                        if (this.currentStep === this.steps.length - 1) {
                            this.generateQuote();
                        } else {
                            this.nextStep();
                        }
                    }
                }
            });
        }

        showCurrentStep() {
            // Get current section
            const currentSection = document.getElementById(this.steps[this.currentStep].id);
            if (!currentSection) {
                console.error('Section not found:', this.steps[this.currentStep].id);
                return;
            }

            // Hide all sections
            document.querySelectorAll('.section').forEach(section => {
                section.classList.remove('active');
            });

            // Show current section
            currentSection.classList.add('active');

            // Update progress bar
            document.querySelectorAll('.progress-step').forEach((step, index) => {
                step.classList.remove('active');
                if (index === this.currentStep) {
                    step.classList.add('active');
                }
            });

            // Update navigation buttons
            this.updateNavigationButtons();

            // If we're on the review section, populate the summary
            if (this.steps[this.currentStep].id === 'review') {
                this.populateSummary();
            }

            // Scroll to top
            window.scrollTo(0, 0);
        }

        populateSummary() {
            console.log('Populating summary...');
            
            // Get current data
            const { dimensions, surfaces, noiseData } = window.FormState;
            console.log('Current FormState:', { dimensions, surfaces, noiseData });
            
            // Calculate areas
            const areas = this.calculateAreas(dimensions);
            
            // Room dimensions and type
            const dimensionsText = Object.values(dimensions).some(v => v) ? 
                `Length: ${dimensions.length || 0}m, Width: ${dimensions.width || 0}m, Height: ${dimensions.height || 0}m` : '-';
            this.safeSetText('summary-dimensions', dimensionsText);
            
            // Display areas
            this.safeSetText('summary-wall-area', `${areas.walls.toFixed(2)} m²`);
            this.safeSetText('summary-floor-area', `${areas.floor.toFixed(2)} m²`);
            this.safeSetText('summary-ceiling-area', `${areas.ceiling.toFixed(2)} m²`);
            
            const roomType = document.getElementById('room-type')?.value || '-';
            this.safeSetText('summary-room-type', roomType);
            
            console.log('Updated room details:', { dimensionsText, roomType, areas });

            // Noise Details
            if (noiseData) {
                this.safeSetText('summary-noise-type', noiseData.type || '-');
                this.safeSetText('summary-noise-intensity', noiseData.intensity ? `Level ${noiseData.intensity}` : '-');
                this.safeSetText('summary-noise-time', noiseData.time?.join(', ') || '-');
                this.safeSetText('summary-noise-sources', noiseData.direction?.join(', ') || '-');
                console.log('Updated noise details:', noiseData);
            }

            // Get recommendations from SoundproofingManager
            if (window.soundproofingManager) {
                const noiseSurfaces = window.soundproofingManager.getNoiseSourceSurfaces();
                const noisePriority = window.soundproofingManager.getNoisePriority();
                const recommendations = window.soundproofingManager.getPrimarySolution(noiseData, noiseSurfaces, noisePriority);
                console.log('Got recommendations:', recommendations);

                // Update recommendations section
                const recsContainer = document.getElementById('summary-recommendations');
                if (recsContainer) {
                    let recsHtml = '<div class="recommendations-summary">';
                    
                    if (recommendations.walls.length > 0) {
                        recsHtml += '<div class="recommendation-item"><h4>Wall Solutions:</h4>';
                        recommendations.walls.forEach(wall => {
                            recsHtml += `<p>${wall.wall} Wall: ${wall.solution}</p>`;
                        });
                        recsHtml += '</div>';
                    }

                    if (recommendations.ceiling) {
                        recsHtml += `<div class="recommendation-item">
                            <h4>Ceiling Solution:</h4>
                            <p>${recommendations.ceiling}</p>
                        </div>`;
                    }

                    if (recommendations.reasoning.length > 0) {
                        recsHtml += '<div class="recommendation-reasoning">';
                        recommendations.reasoning.forEach(reason => {
                            recsHtml += `<p>• ${reason}</p>`;
                        });
                        recsHtml += '</div>';
                    }

                    recsHtml += '</div>';
                    recsContainer.innerHTML = recsHtml;
                    console.log('Updated recommendations display');
                }

                // Calculate and display costs
                const costs = this.calculateCosts(recommendations);
                this.safeSetText('summary-wall-cost', costs.wall ? `$${costs.wall.toFixed(2)}` : '-');
                this.safeSetText('summary-floor-cost', costs.floor ? `$${costs.floor.toFixed(2)}` : '-');
                this.safeSetText('summary-ceiling-cost', costs.ceiling ? `$${costs.ceiling.toFixed(2)}` : '-');
                this.safeSetText('summary-total-cost', `$${costs.total.toFixed(2)}`);
                console.log('Updated costs:', costs);

                // Update implementation details
                this.safeSetText('summary-install-time', this.getInstallationTime(recommendations));
                this.safeSetText('summary-skill-level', this.getSkillLevel(recommendations));
                this.safeSetText('summary-special-reqs', this.getSpecialRequirements(recommendations).join(', ') || 'None');
                console.log('Updated implementation details');
            }
        }

        // Helper methods for implementation details
        getInstallationTime(recommendations) {
            const wallCount = recommendations.walls.length;
            const hasCeiling = Boolean(recommendations.ceiling);
            const baseTime = 2; // Base days
            const wallTime = wallCount * 1; // 1 day per wall
            const ceilingTime = hasCeiling ? 2 : 0; // 2 days for ceiling
            return `${baseTime + wallTime + ceilingTime} days`;
        }

        getSkillLevel(recommendations) {
            const solutions = [
                ...recommendations.walls.map(w => w.solution),
                recommendations.ceiling
            ].filter(Boolean);

            if (solutions.some(s => s.includes('GenieClip') || s.includes('Independent'))) {
                return 'Professional';
            } else if (solutions.some(s => s.includes('ResilientBar'))) {
                return 'Advanced';
            }
            return 'Intermediate';
        }

        getSpecialRequirements(recommendations) {
            const reqs = new Set();
            const solutions = [
                ...recommendations.walls.map(w => w.solution),
                recommendations.ceiling
            ].filter(Boolean);

            if (solutions.some(s => s.includes('SP15'))) {
                reqs.add('Special handling for SP15 boards');
            }
            if (solutions.some(s => s.includes('GenieClip'))) {
                reqs.add('Precision mounting required');
            }
            if (solutions.some(s => s.includes('Independent'))) {
                reqs.add('Additional floor space needed');
            }

            return Array.from(reqs);
        }

        safeSetText(elementId, text) {
            if (!elementId) return;
            const element = document.getElementById(elementId);
            if (element) {
                element.textContent = text;
            }
        }

        populateFeaturesList(surface) {
            const featuresList = document.getElementById(`${surface}-features-list`);
            if (!featuresList) return;

            featuresList.innerHTML = '';
            const features = document.querySelectorAll(`input[name="${surface}-features"]:checked`);
            
            features.forEach(feature => {
                if (feature && feature.parentElement) {
                    const li = document.createElement('li');
                    li.textContent = feature.parentElement.textContent.trim();
                    featuresList.appendChild(li);
                }
            });
        }

        populateBlockages() {
            const { blockages } = window.FormState;

            // Clear existing blockages
            ['north', 'east', 'south', 'west'].forEach(wall => {
                const list = document.getElementById(`summary-${wall}-blockages`);
                if (list) list.innerHTML = '';
            });

            // Wall blockages
            ['north', 'east', 'south', 'west'].forEach(wall => {
                const list = document.getElementById(`summary-${wall}-blockages`);
                if (!list) return;

                const wallBlockages = blockages.wall?.filter(b => b.wall === wall) || [];
                
                wallBlockages.forEach(blockage => {
                    const li = document.createElement('li');
                    li.textContent = `${this.formatBlockageType(blockage.type)} (${blockage.width}m × ${blockage.height}m)`;
                    if (blockage.notes) li.title = blockage.notes;
                    list.appendChild(li);
                });
                
                // Add "No blockages" message if empty
                if (wallBlockages.length === 0) {
                    const li = document.createElement('li');
                    li.textContent = 'No blockages';
                    li.classList.add('no-blockages');
                    list.appendChild(li);
                }
            });

            // Floor and ceiling blockages
            ['floor', 'ceiling'].forEach(surface => {
                const list = document.getElementById(`summary-${surface}-blockages`);
                if (!list) return;

                list.innerHTML = '';
                const surfaceBlockages = blockages[surface] || [];

                surfaceBlockages.forEach(blockage => {
                    const li = document.createElement('li');
                    li.textContent = `${this.formatBlockageType(blockage.type)} (${blockage.width}m × ${blockage.length}m)`;
                    if (blockage.notes) li.title = blockage.notes;
                    list.appendChild(li);
                });
                
                // Add "No blockages" message if empty
                if (surfaceBlockages.length === 0) {
                    const li = document.createElement('li');
                    li.textContent = 'No blockages';
                    li.classList.add('no-blockages');
                    list.appendChild(li);
                }
            });
        }

        generateQuote() {
            // TODO: Implement quote generation
            console.log('Generating quote with form state:', window.FormState);
        }

        saveCurrentSectionState() {
            const currentSection = document.getElementById(this.steps[this.currentStep]?.id);
            if (currentSection) {
                // Save form values
                const formInputs = currentSection.querySelectorAll('input, select, textarea');
                this.sectionStates = this.sectionStates || {};
                this.sectionStates[this.steps[this.currentStep].id] = Array.from(formInputs).reduce((state, input) => {
                    if (input && input.id) {  // Only save elements with valid IDs
                        state[input.id] = input.value;
                    }
                    return state;
                }, {});
            }
        }

        restoreSectionState(section) {
            if (this.sectionStates?.[section.id]) {
                const state = this.sectionStates[section.id];
                Object.entries(state).forEach(([id, value]) => {
                    if (id) {  // Only process valid IDs
                        const input = section.querySelector(`#${id}`);
                        if (input) {
                            input.value = value;
                        }
                    }
                });
            }
        }

        goToStep(stepIndex) {
            // This method correctly allows free navigation
            if (stepIndex >= 0 && stepIndex < this.steps.length) {
                this.currentStep = stepIndex;
                this.showCurrentStep();
            }
        }

        nextStep() {
            if (this.currentStep < this.steps.length - 1) {
                this.currentStep++;
                this.showCurrentStep();
            }
        }

        prevStep() {
            if (this.currentStep > 0) {
                this.currentStep--;
                this.showCurrentStep();
            }
        }

        updateNavigationButtons() {
            const prevBtn = document.querySelector('#prev-btn');
            const nextBtn = document.querySelector('#next-btn');
            
            if (prevBtn) {
                prevBtn.disabled = false; // Always enable prev button
            }
            if (nextBtn) {
                nextBtn.disabled = false; // Always enable next button
                nextBtn.textContent = this.currentStep === this.steps.length - 1 ? 'Generate Quote' : 'Next';
            }
        }

        // Helper method to format blockage types
        formatBlockageType(type) {
            return type
                .split('-')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
        }

        generateRecommendations(noiseData) {
            // Basic recommendation logic based on noise type and intensity
            const recommendations = {
                walls: [],
                ceiling: null,
                floor: null
            };
            
            if (noiseData.direction.includes('above')) {
                recommendations.ceiling = 'ResilientBarCeilingStandard';
            }
            
            if (noiseData.direction.some(d => ['north', 'east', 'south', 'west'].includes(d))) {
                recommendations.walls.push('M20WallStandard');
            }
            
            return recommendations;
        }

        displayRecommendations(recommendations) {
            // Update the recommendations section
            if (recommendations.walls.length > 0) {
                this.safeSetText('summary-wall-treatment', recommendations.walls.join(', '));
            }
            if (recommendations.ceiling) {
                this.safeSetText('summary-ceiling-treatment', recommendations.ceiling);
            }
            if (recommendations.floor) {
                this.safeSetText('summary-floor-treatment', recommendations.floor);
            }
            
            // Calculate and display estimated costs
            const costs = this.calculateCosts(recommendations);
            this.safeSetText('summary-total-cost', `$${costs.total.toFixed(2)}`);
        }

        calculateCosts(recommendations) {
            const costs = {
                wall: 0,
                floor: 0,
                ceiling: 0,
                total: 0
            };

            // Calculate wall costs
            if (recommendations.walls.length > 0) {
                costs.wall = recommendations.walls.length * 1000; // Base cost per wall
                if (recommendations.walls[0].solution.includes('SP15')) {
                    costs.wall *= 1.5; // 50% premium for SP15
                }
            }

            // Calculate ceiling costs
            if (recommendations.ceiling) {
                costs.ceiling = 2000; // Base ceiling cost
                if (recommendations.ceiling.includes('SP15')) {
                    costs.ceiling *= 1.5; // 50% premium for SP15
                }
            }

            costs.total = costs.wall + costs.floor + costs.ceiling;
            return costs;
        }

        calculateAreas(dimensions) {
            const { length = 0, width = 0, height = 0 } = dimensions;
            return {
                walls: 2 * (length * height + width * height),
                floor: length * width,
                ceiling: length * width
            };
        }
    }

    window.WorkflowManager = WorkflowManager;
}

// Initialize workflow manager
if (!window.workflowManager) {
    window.workflowManager = new WorkflowManager();
    document.addEventListener('DOMContentLoaded', () => {
        window.workflowManager.initialize();
    });
}