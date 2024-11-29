async function initializeFormHandlers() {
    console.log('Initializing form handlers');
    
    const requiredManagers = [
        'errorUtils', 'roomManager', 'roomCalculator', 
        'surfaceManager', 'wallManager', 'soundproofingManager', 
        'workflowManager'
    ];
    
    return new Promise((resolve, reject) => {
        const checkComplete = () => {
            const allInitialized = requiredManagers.every(
                name => window[name]?.initialized
            );
            if (allInitialized) {
                bindAllEvents()
                    .then(() => {
                        console.log('Form handlers initialized successfully');
                        resolve(true);
                    })
                    .catch(reject);
            }
        };
        
        requiredManagers.forEach(manager => {
            window.addEventListener(`${manager}Initialized`, checkComplete);
        });
        
        // Check immediately in case all are already initialized
        checkComplete();
    });
}

// Function to initialize a specific manager with a timeout
async function initializeManager(manager, timeout) {
    return new Promise((resolve, reject) => {
        const checkInitialized = () => {
            if (window[manager]?.initialized) {
                resolve(true);
            } else {
                setTimeout(checkInitialized, 1000); // Check again after 1 second
            }
        };
        setTimeout(() => {
            reject(new Error(`Timeout waiting for ${manager} to initialize`));
        }, timeout);
        checkInitialized();
    });
}

// Bind all events
async function bindAllEvents() {
    try {
        await Promise.all([
            bindNavigationEvents(),
            bindInputEvents(),
            bindSurfaceEvents(),
            bindSoundproofingEvents(),
            bindWorkflowEvents()
        ]);
        console.log('All events bound successfully');
    } catch (error) {
        console.error('Failed to bind events:', error);
        throw error;
    }
}

// Navigation events
function bindNavigationEvents() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    if (!prevBtn || !nextBtn) {
        console.error('Navigation buttons not found');
        return;
    }
    
    prevBtn.addEventListener('click', () => {
        if (window.workflowManager?.initialized) {
            window.workflowManager.prevStep();
        }
    });
    
    nextBtn.addEventListener('click', () => {
        if (window.workflowManager?.initialized) {
            window.workflowManager.nextStep();
        }
    });

    console.log('Navigation events bound');
}

// Input events
function bindInputEvents() {
    const dimensionInputs = document.querySelectorAll('input[type="number"]');
    if (!dimensionInputs.length) {
        console.warn('No dimension inputs found');
        return;
    }

    dimensionInputs.forEach(input => {
        const errorMsg = document.createElement('span'); // Create a span for error message
        errorMsg.className = 'error-message'; // Add a class for styling
        input.parentNode.insertBefore(errorMsg, input.nextSibling); // Insert error message after input

        input.addEventListener('input', debounce((e) => {
            const value = parseFloat(e.target.value);
            if (isNaN(value) || value <= 0 || value > 100) {
                e.target.classList.add('invalid');
                errorMsg.textContent = 'Enter a number between 1 and 100.'; // Display error message
            } else {
                e.target.classList.remove('invalid');
                errorMsg.textContent = ''; // Clear error message
            }
            window.roomManager.updateDimensions({ [e.target.id]: value });
        }, 300));
    });

    console.log('Input events bound');
}

// Surface events
function bindSurfaceEvents() {
    // Surface type selection
    const surfaceTypeButtons = document.querySelectorAll('.surface-type-btn');
    surfaceTypeButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (!window.surfaceManager?.initialized) {
                console.warn('SurfaceManager not initialized');
                return;
            }

            const surfaceType = button.dataset.surface;
            window.surfaceManager.selectSurfaceType(surfaceType);
        });
    });

    // Feature selection
    const featureCheckboxes = document.querySelectorAll('.feature-checkbox');
    featureCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            if (!window.surfaceManager?.initialized) {
                console.warn('SurfaceManager not initialized');
                return;
            }

            const feature = e.target.value;
            const surfaceType = e.target.dataset.surface;
            window.surfaceManager.updateFeature(surfaceType, feature, e.target.checked);
        });
    });

    console.log('Surface events bound');
}

// Soundproofing events
function bindSoundproofingEvents() {
    const solutionButtons = document.querySelectorAll('.solution-btn');
    solutionButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (!window.soundproofingManager?.initialized) {
                console.warn('SoundproofingManager not initialized');
                return;
            }

            const solution = button.dataset.solution;
            const category = button.dataset.category;
            window.soundproofingManager.selectSolution(category, solution);
        });
    });

    console.log('Soundproofing events bound');
}

// Workflow events
function bindWorkflowEvents() {
    const stepButtons = document.querySelectorAll('.workflow-steps .step');
    stepButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (!window.workflowManager?.initialized) {
                console.warn('WorkflowManager not initialized');
                return;
            }

            const stepIndex = parseInt(button.dataset.step);
            if (!isNaN(stepIndex)) {
                window.workflowManager.goToStep(stepIndex);
            }
        });
    });

    console.log('Workflow events bound');
}

// Helper functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    }
}

// Error handling wrapper
function handleError(context, error) {
    console.error(`${context}:`, error);
    if (window.errorUtils?.initialized) {
        window.errorUtils.displayError(`${context}: ${error.message}`);
    }
    throw error;
}

// Export if using modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeFormHandlers,
        bindAllEvents,
        bindNavigationEvents,
        bindInputEvents,
        bindSurfaceEvents,
        bindSoundproofingEvents,
        bindWorkflowEvents
    };
}

// Make form handlers available globally
window.initializeFormHandlers = initializeFormHandlers;