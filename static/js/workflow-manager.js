if (!window.WorkflowManager) {
    class WorkflowManager {
        constructor() {
            this.initialized = false;
            this.currentStep = 0;
            this.steps = [
                { id: 'room-details-section', label: 'Room Details', requiresValidation: true },
                { id: 'surface-features-section', label: 'Surface Features', requiresValidation: false },
                { id: 'soundproofing-section', label: 'Soundproofing', requiresValidation: true },
                { id: 'review-section', label: 'Review', requiresValidation: true }
            ];
            this.stepValidations = {
                0: this.validateRoomDetails.bind(this),
                1: () => true,
                2: () => true,
                3: this.validateSoundproofing.bind(this),
                4: this.validateReview.bind(this)
            };
            this.dependencies = [
                'roomManager', 
                'surfaceManager', 
                'wallManager', 
                'soundproofingManager'
            ];
        }
        
        

        async waitForDOM() {
            return new Promise(resolve => {
                if (document.readyState === 'complete') {
                    resolve();
                } else {
                    window.addEventListener('load', resolve);
                }
            });
        }

        async waitForDependencies() {
            console.log('WorkflowManager: Waiting for dependencies...');
            for (const dep of this.dependencies) {
                if (!window[dep]?.initialized) {
                    console.log(`WorkflowManager: Waiting for ${dep}...`);
                    await new Promise(resolve => 
                        window.addEventListener(`${dep}Initialized`, resolve, { once: true })
                    );
                    console.log(`WorkflowManager: Detected ${dep}Initialized event.`);
                }
            }
            console.log('WorkflowManager: All dependencies are ready.');
        }

        async initialize() {
            console.log('WorkflowManager: Starting initialization...');
            if (this.initialized) return true;

            await this.waitForDOM();
            await this.waitForDependencies();
            console.log('WorkflowManager: Dependencies are ready');

            await this.bindEvents();
            this.showCurrentStep();

            this.initialized = true;
            console.log('WorkflowManager initialized successfully');
            window.dispatchEvent(new CustomEvent('workflowManagerInitialized'));
            return true;
        }

        createProgressBar() {
            const stepsContainer = document.querySelector('.steps-container');
            if (!stepsContainer) return;

            // Clear existing steps
            stepsContainer.innerHTML = '';

            // Create step elements
            this.steps.forEach((step, index) => {
                const stepElement = document.createElement('div');
                stepElement.className = `step ${index <= this.currentStep ? 'active' : ''}`;
                stepElement.dataset.step = index;
                stepElement.setAttribute('role', 'button');
                stepElement.setAttribute('tabindex', '0');
                
                stepElement.innerHTML = `
                    <div class="step-number">${index + 1}</div>
                    <span class="step-label">${step.label}</span>
                    <span class="step-status" aria-hidden="true"></span>
                `;
                
                stepsContainer.appendChild(stepElement);
            });

            // Update progress bar
            const progress = (this.currentStep / (this.steps.length - 1)) * 100;
            const fill = document.querySelector('.progress-fill');
            if (fill) {
                fill.style.width = `${progress}%`;
            }
        }

        async bindEvents() {
            // Step clicks
            document.querySelectorAll('.step').forEach((step, index) => {
                step.addEventListener('click', () => {
                    this.goToStep(index);
                });

                // Keyboard accessibility
                step.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        this.goToStep(index);
                    }
                });
            });

            // Navigation buttons
            const prevBtn = document.getElementById('prev-btn');
            const nextBtn = document.getElementById('next-btn');

            if (prevBtn) {
                prevBtn.addEventListener('click', () => this.prevStep());
            }
            if (nextBtn) {
                nextBtn.addEventListener('click', () => this.nextStep());
            }
        }

        showCurrentStep() {
            // Hide all sections first
            document.querySelectorAll('.workflow-section').forEach(section => {
                section.classList.remove('active');
                section.style.display = 'none';
            });

            // Show current section
            const currentSection = document.getElementById(this.steps[this.currentStep].id);
            if (currentSection) {
                currentSection.classList.add('active');
                currentSection.style.display = 'block';
            }

            // Update step indicators
            document.querySelectorAll('.step').forEach((step, index) => {
                step.classList.remove('active', 'completed');
                if (index === this.currentStep) {
                    step.classList.add('active');
                } else if (index < this.currentStep) {
                    step.classList.add('completed');
                }
            });
        }

        updateNavigationButtons() {
            const prevBtn = document.getElementById('prev-btn');
            const nextBtn = document.getElementById('next-btn');

            if (prevBtn) {
                prevBtn.disabled = this.currentStep === 0;
            }
            
            if (nextBtn) {
                const isLastStep = this.currentStep === this.steps.length - 1;
                nextBtn.disabled = isLastStep;
                nextBtn.innerHTML = isLastStep ? 
                    'Complete <span class="btn-icon">✓</span>' : 
                    'Next <span class="btn-icon">→</span>';
            }
        }

        async updateProgressBar() {
            const progressFill = document.querySelector('.progress-fill');
            const fill = document.querySelector('.progress-fill');
            if (fill) fill.style.width = `${progress}%`;
            
            const progress = ((this.currentStep + 1) / this.steps.length) * 100;
            progressFill.style.width = `${progress}%`;

            // Update step states
            document.querySelectorAll('.step').forEach((step, index) => {
                step.classList.remove('active', 'completed');
                if (index === this.currentStep) {
                    step.classList.add('active');
                } else if (index < this.currentStep) {
                    step.classList.add('completed');
                }
            });
        }

        // ... existing code ...

validateRoomDetails() {
    const dimensions = window.FormState?.dimensions || {};
    const isValid = Object.values(dimensions).every(value => value > 0);
    if (!isValid) {
        window.errorUtils?.displayError('Please enter valid dimensions for the room.');
    }
    return isValid;
}

// ... existing code ...

        validateSoundproofing() {
            // Add your soundproofing validation logic
            return true;
        }

        validateReview() {
            // Add your review validation logic
            return true;
        }

        async goToStep(stepIndex) {
            if (stepIndex >= 0 && stepIndex < this.steps.length) {
                console.log(`WorkflowManager: Moving to step ${stepIndex}`);
                this.currentStep = stepIndex;
                this.showCurrentStep();
                await this.updateProgressBar();
                this.updateNavigationButtons();
                
                // Dispatch step change event
                window.dispatchEvent(new CustomEvent('workflowStepChanged', {
                    detail: { 
                        step: stepIndex, 
                        stepName: this.steps[stepIndex].label,
                        isValid: this.stepValidations[stepIndex]?.() ?? true
                    }
                }));
            } else {
                console.warn(`WorkflowManager: Invalid step index ${stepIndex}`);
            }
        }

        nextStep() {
            if (this.currentStep < this.steps.length - 1) {
                console.log('WorkflowManager: Moving to next step');
                this.goToStep(this.currentStep + 1);
            }
        }

        prevStep() {
            if (this.currentStep > 0) {
                console.log('WorkflowManager: Moving to previous step');
                this.goToStep(this.currentStep - 1);
            }
        }
    }

    window.WorkflowManager = WorkflowManager;
}

if (!window.workflowManager) {
    window.workflowManager = new WorkflowManager();
    window.addEventListener('load', () => {
        const dependencies = [
            'roomManager', 
            'surfaceManager', 
            'wallManager', 
            'soundproofingManager'
        ];
        
        const checkDependencies = () => {
            const allReady = dependencies.every(dep => window[dep]?.initialized);
            if (allReady) {
                window.workflowManager.initialize().then(() => {
                    window.dispatchEvent(new CustomEvent('workflowManagerInitialized'));
                });
            }
        };

        dependencies.forEach(dep => {
            window.addEventListener(`${dep}Initialized`, checkDependencies);
        });
        checkDependencies(); // Check immediately
    });
}