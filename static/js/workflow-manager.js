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
            try {
                const summaryContainer = document.getElementById(this.steps[this.steps.length - 1].id);
                if (!summaryContainer) {
                    console.warn(`Summary container '${this.steps[this.steps.length - 1].id}' not found`);
                    return;
                }

                // Get current form state with safe defaults
                const formState = window.FormState || {};
                const noiseData = formState.noiseData || {};
                const dimensions = formState.dimensions || {};
                const blockages = formState.blockages || {};

                // Safely get soundproofingManager instance
                const soundproofingManager = window.soundproofingManager;
                if (!soundproofingManager) {
                    throw new Error('SoundproofingManager not initialized');
                }

                // Get noise surfaces with safe defaults
                const noiseSurfaces = soundproofingManager.getNoiseSourceSurfaces() || {
                    walls: [],
                    ceiling: false,
                    floor: false
                };

                // Generate recommendations with safe error handling
                let recommendations;
                try {
                    recommendations = soundproofingManager.getPrimarySolution(
                        noiseData,
                        noiseSurfaces,
                        soundproofingManager.getNoisePriority(),
                        {
                            dimensions,
                            blockages,
                            roomType: formState.roomType
                        }
                    );
                } catch (recError) {
                    console.error('Error generating recommendations:', recError);
                    recommendations = null;
                }

                // Generate summary HTML with safe error handling
                let summaryHtml = '';
                try {
                    summaryHtml = soundproofingManager.generateSummaryHtml() || '';
                } catch (summaryError) {
                    console.error('Error generating summary HTML:', summaryError);
                    summaryHtml = '<div class="error-message">Error generating summary</div>';
                }

                // Update the summary container
                summaryContainer.innerHTML = summaryHtml;

                // Add recommendations section if available
                if (recommendations) {
                    const recommendationsHtml = this.generateRecommendationsHtml(recommendations);
                    if (recommendationsHtml) {
                        summaryContainer.innerHTML += recommendationsHtml;
                    }
                }

            } catch (error) {
                console.error('Error populating summary:', error);
                const summaryContainer = document.getElementById(this.steps[this.steps.length - 1].id);
                if (summaryContainer) {
                    summaryContainer.innerHTML = `
                        <div class="error-message">
                            <h3>Error Generating Summary</h3>
                            <p>There was an error generating your summary. Please try the following:</p>
                            <ul>
                                <li>Check that all required information is filled out</li>
                                <li>Ensure room dimensions are valid numbers</li>
                                <li>Verify noise source information is complete</li>
                            </ul>
                            <p>If the problem persists, please try refreshing the page.</p>
                        </div>`;
                }
            }
        }

        generateRecommendationsHtml(recommendations) {
            try {
                if (!recommendations) {
                    console.warn('No recommendations provided');
                    return '';
                }

                let html = '<div class="recommendations-summary">';
                html += '<h3>Recommended Solutions</h3>';

                // Wall solutions
                if (recommendations.walls && Array.isArray(recommendations.walls) && recommendations.walls.length > 0) {
                    html += '<div class="wall-solutions">';
                    html += '<h4>Wall Treatments</h4>';
                    recommendations.walls.forEach(wall => {
                        if (wall && wall.wall && wall.solution) {
                            html += `
                                <div class="solution">
                                    <p><strong>${wall.wall} Wall:</strong> ${wall.solution}</p>
                                    <p>Effectiveness: ${(wall.score || 0 * 100).toFixed(1)}%</p>
                                </div>`;
                        }
                    });
                    html += '</div>';
                }

                // Ceiling solution
                if (recommendations.ceiling && recommendations.ceiling.solution) {
                    html += '<div class="ceiling-solution">';
                    html += '<h4>Ceiling Treatment</h4>';
                    html += `
                        <div class="solution">
                            <p><strong>Solution:</strong> ${recommendations.ceiling.solution}</p>
                            <p>Effectiveness: ${((recommendations.ceiling.score || 0) * 100).toFixed(1)}%</p>
                        </div>`;
                    html += '</div>';
                }

                // Floor message
                if (recommendations.floor && recommendations.floor.message) {
                    html += '<div class="floor-solution">';
                    html += '<h4>Floor Treatment</h4>';
                    html += `
                        <div class="solution">
                            <p>${recommendations.floor.message}</p>
                            ${recommendations.floor.contactInfo ? 
                                `<p>Contact: ${recommendations.floor.contactInfo.phone || ''}</p>` : ''}
                        </div>`;
                    html += '</div>';
                }

                html += '</div>';
                return html;
            } catch (error) {
                console.error('Error generating recommendations HTML:', error);
                return '<div class="error-message">Error displaying recommendations</div>';
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
            try {
                const formState = window.FormState || {};
                const noiseData = formState.noiseData || {};
                const dimensions = formState.dimensions || {};
                const blockages = formState.blockages || {};

                // Create quote content
                let quoteContent = `Soundproofing Solution Quote\n`;
                quoteContent += `Generated: ${new Date().toLocaleString()}\n\n`;

                // Project Details
                quoteContent += `PROJECT DETAILS\n`;
                quoteContent += `-------------\n`;
                quoteContent += `Noise Type: ${noiseData.type || 'Not specified'}\n`;
                quoteContent += `Intensity: ${noiseData.intensity || 'Not specified'}\n`;
                quoteContent += `Time: ${Array.isArray(noiseData.time) ? noiseData.time.join(', ') : 'Not specified'}\n`;
                quoteContent += `Direction: ${Array.isArray(noiseData.direction) ? noiseData.direction.join(', ') : 'Not specified'}\n\n`;

                // Room Dimensions
                quoteContent += `ROOM DIMENSIONS\n`;
                quoteContent += `---------------\n`;
                quoteContent += `Length: ${dimensions.length ? dimensions.length.toFixed(2) + ' m' : '0 m'}\n`;
                quoteContent += `Width: ${dimensions.width ? dimensions.width.toFixed(2) + ' m' : '0 m'}\n`;
                quoteContent += `Height: ${dimensions.height ? dimensions.height.toFixed(2) + ' m' : '0 m'}\n\n`;

                // Surface Features
                quoteContent += `SURFACE FEATURES\n`;
                quoteContent += `----------------\n`;
                if (this.hasAnyBlockages(blockages)) {
                    if (blockages.wall?.length > 0) {
                        blockages.wall.forEach(blockage => {
                            if (blockage?.type && blockage?.wall) {
                                quoteContent += `${blockage.wall} Wall: ${blockage.type} (${blockage.width}m × ${blockage.height}m)\n`;
                            }
                        });
                    }
                    if (blockages.ceiling?.length > 0) {
                        blockages.ceiling.forEach(blockage => {
                            if (blockage?.type) {
                                quoteContent += `Ceiling: ${blockage.type} (${blockage.width}m × ${blockage.length}m)\n`;
                            }
                        });
                    }
                    if (blockages.floor?.length > 0) {
                        blockages.floor.forEach(blockage => {
                            if (blockage?.type) {
                                quoteContent += `Floor: ${blockage.type} (${blockage.width}m × ${blockage.length}m)\n`;
                            }
                        });
                    }
                } else {
                    quoteContent += `No surface features reported\n`;
                }
                quoteContent += '\n';

                // Cost Breakdown
                quoteContent += `COST BREAKDOWN\n`;
                quoteContent += `--------------\n`;
                
                const noiseSurfaces = window.soundproofingManager.getNoiseSourceSurfaces();
                let totalCost = 0;

                // Calculate costs for each surface
                if (noiseSurfaces.walls?.length > 0) {
                    noiseSurfaces.walls.forEach(wall => {
                        const solution = window.soundproofingManager.findBestSolutionForWall(wall, noiseData);
                        if (solution) {
                            const costs = window.soundproofingManager.calculateLocalCosts(solution, dimensions, 'wall', wall.toLowerCase());
                            if (!costs.error) {
                                totalCost += costs.total;
                                quoteContent += `${wall} Wall (${costs.area} m²): £${costs.total.toFixed(2)}\n`;
                                quoteContent += `Solution: ${solution}\n`;
                                quoteContent += `Materials:\n`;
                                costs.materials.forEach(material => {
                                    quoteContent += `  - ${material.name}: ${material.amount} ${material.unit} (£${material.cost.toFixed(2)})\n`;
                                });
                                quoteContent += '\n';
                            }
                        }
                    });
                }

                if (noiseSurfaces.ceiling) {
                    const solution = window.soundproofingManager.findBestCeilingSolution(noiseData);
                    if (solution) {
                        const costs = window.soundproofingManager.calculateLocalCosts(solution, dimensions, 'ceiling');
                        if (!costs.error) {
                            totalCost += costs.total;
                            quoteContent += `Ceiling (${costs.area} m²): £${costs.total.toFixed(2)}\n`;
                            quoteContent += `Solution: ${solution}\n`;
                            quoteContent += `Materials:\n`;
                            costs.materials.forEach(material => {
                                quoteContent += `  - ${material.name}: ${material.amount} ${material.unit} (£${material.cost.toFixed(2)})\n`;
                            });
                            quoteContent += '\n';
                        }
                    }
                }

                // Blockage adjustment
                const blockageAdjustment = window.soundproofingManager.calculateBlockageAdjustment(blockages);
                if (blockageAdjustment > 0) {
                    const adjustmentAmount = totalCost * blockageAdjustment;
                    quoteContent += `Blockage Adjustment (+${(blockageAdjustment * 100).toFixed(0)}%): £${adjustmentAmount.toFixed(2)}\n`;
                    totalCost += adjustmentAmount;
                }

                quoteContent += `\nTOTAL COST: £${totalCost.toFixed(2)}\n\n`;

                // Additional Notes
                quoteContent += `NOTES\n`;
                quoteContent += `-----\n`;
                quoteContent += `1. All prices include materials only\n`;
                quoteContent += `2. Installation costs may vary based on complexity\n`;
                quoteContent += `3. Quote valid for 30 days\n`;
                quoteContent += `4. Professional installation recommended\n`;
                quoteContent += `5. Contact us for detailed installation guidance\n\n`;

                // Contact Information
                quoteContent += `CONTACT INFORMATION\n`;
                quoteContent += `-------------------\n`;
                quoteContent += `Phone: +44 (0)1234 567890\n`;
                quoteContent += `Email: info@soundproofing.com\n`;

                // Create and download the file
                const blob = new Blob([quoteContent], { type: 'text/plain' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `soundproofing-quote-${new Date().toISOString().split('T')[0]}.txt`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);

            } catch (error) {
                console.error('Error generating quote:', error);
                alert('Error generating quote. Please try again.');
            }
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