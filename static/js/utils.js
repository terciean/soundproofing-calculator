// At the top of the file, before any other code
window.InitializationState = {
    initialized: new Set(),
    dependencies: {
        errorUtils: [],
        roomManager: ['errorUtils'],
        roomCalculator: ['roomManager'],
        surfaceManager: ['roomManager', 'roomCalculator'],
        wallManager: ['roomManager', 'surfaceManager'],
        soundproofingManager: ['roomManager'],
        workflowManager: ['roomManager', 'surfaceManager', 'wallManager', 'soundproofingManager']
    }
};

// Initialize FormState first
window.FormState = {
    dimensions: {},
    surfaces: new Map(),
    soundproofing: new Map()
};

function showLoadingIndicator() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (!loadingIndicator) {
        const indicator = document.createElement('div');
        indicator.id = 'loading-indicator';
        indicator.className = 'loading-indicator';
        indicator.innerHTML = `
            <div class="loading-spinner"></div>
            <div class="loading-text">Loading...</div>
        `;
        document.body.appendChild(indicator);
    } else {
        loadingIndicator.style.display = 'flex';
    }
}

function hideLoadingIndicator() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'none';
    }
}

async function initializeApplication() {
    try {
        // Wait for DOM to be ready first
        if (document.readyState === 'loading') {
            await new Promise(resolve => document.addEventListener('DOMContentLoaded', resolve));
        }

        showLoadingIndicator();
        console.log('Starting application initialization...');

        // Initialize errorUtils first
        await waitForDependency('errorUtils'); // Wait for errorUtils to be ready

        // Initialize other managers with proper dependency chain
        const managers = [
            { name: 'roomManager' },
            { name: 'roomCalculator' },
            { name: 'surfaceManager' },
            { name: 'wallManager' },
            { name: 'soundproofingManager' },
            { name: 'workflowManager' }
        ];

        for (const manager of managers) {
            console.log(`Initializing ${manager.name}...`);
            await initializeManagerWithDependencies({
                name: manager.name,
                dependencies: window.InitializationState.dependencies[manager.name]
            });
        }

        console.log('Application initialization complete');
        return true;
    } catch (error) {
        console.error('Application initialization failed:', error);
        window.errorUtils?.displayError(`Initialization failed: ${error.message}`);
        throw error;
    } finally {
        hideLoadingIndicator();
    }
}

async function initializeManagerWithDependencies({ name, dependencies }) {
    // Wait for dependencies first
    if (dependencies.length > 0) {
        console.log(`Waiting for ${name} dependencies:`, dependencies);
        for (const dep of dependencies) {
            await waitForDependency(dep.toLowerCase());
        }
    }

    // Initialize the manager
    return new Promise((resolve, reject) => {
        const checkInitialized = () => {
            const instance = window[name.toLowerCase()];
            if (instance?.initialized) {
                console.log(`${name} initialization confirmed`);
                resolve();
                return true;
            }
            return false;
        };

        if (!checkInitialized()) {
            window.addEventListener(`${name.toLowerCase()}Initialized`, () => {
                checkInitialized();
            }, { once: true });
        }
    });
}

// Make sure initializeApplication is available globally
window.initializeApplication = initializeApplication;

// Update initialization timing
document.addEventListener('DOMContentLoaded', async () => {
    console.log('DOM Content Loaded - Starting initialization');
    try {
        // Wait for errorUtils to be ready first
        if (!window.errorUtils?.initialized) {
            await new Promise((resolve, reject) => {
                const timeout = setTimeout(() => {
                    reject(new Error('ErrorUtils initialization timeout'));
                }, 10000);
                
                const checkErrorUtils = () => {
                    if (window.errorUtils?.initialized) {
                        clearTimeout(timeout);
                        resolve();
                        return true;
                    }
                    return false;
                };

                // Check immediately
                if (!checkErrorUtils()) {
                    window.addEventListener('errorUtilsInitialized', () => {
                        checkErrorUtils();
                    }, { once: true });
                }
            });
        }
        
        await initializeApplication();
    } catch (error) {
        console.error('Failed to initialize application:', error);
        if (window.errorUtils?.initialized) {
            window.errorUtils.displayError('Failed to initialize application: ' + error.message);
        }
    }
});

// Global Dependency Tracker
async function waitForDependency(depName) {
    console.log(`Waiting for dependency: ${depName}`);

    return new Promise((resolve) => {
        // Check if the dependency is already initialized
        if (window[depName]?.initialized) {
            console.log(`${depName} already initialized`);
            resolve(true);
            return;
        }

        // Listen for the initialization event
        window.addEventListener(`${depName}Initialized`, () => {
            console.log(`${depName} initialized.`);
            resolve(true);
        }, { once: true });
    });
}
window.waitForDependency = waitForDependency;

// Initialize Manager Function
async function initializeManager(managerName) {
    console.log(`Initializing ${managerName}...`);
    return new Promise((resolve, reject) => {
        const checkInitialized = () => {
            const instance = window[managerName.toLowerCase()];
            if (instance?.initialized) {
                console.log(`${managerName} initialization confirmed`);
                resolve();
                return true;
            }
            return false;
        };

        window.addEventListener(`${managerName.toLowerCase()}Initialized`, () => {
            checkInitialized();
        }, { once: true });

        // Check immediately
        checkInitialized();
    });
}

async function ensureDependenciesReady(managerName, dependencies) {
    if (!Array.isArray(dependencies)) {
        const error = new Error(`${managerName}: Dependencies must be an array. Received: ${typeof dependencies}`);
        console.error(error);
        window.errorUtils?.displayError(error.message);
        throw error;
    }

    console.log(`${managerName}: Waiting for dependencies...`, dependencies);

    try {
        // Wait for all dependencies concurrently
        await Promise.all(dependencies.map(async dep => {
            const depName = dep.toLowerCase();
            console.log(`${managerName}: Checking dependency ${depName}...`);
            
            // Add retry logic for critical dependencies
            const maxRetries = depName === 'errorutils' ? 3 : 1;
            let lastError;
            
            for (let attempt = 1; attempt <= maxRetries; attempt++) {
                try {
                    await waitForDependency(depName);
                    console.log(`${managerName}: Dependency ${depName} is ready (attempt ${attempt})`);
                    return;
                } catch (error) {
                    lastError = error;
                    if (attempt < maxRetries) {
                        console.log(`${managerName}: Retrying dependency ${depName} (attempt ${attempt + 1})`);
                        await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1s between retries
                    }
                }
            }
            
            throw lastError;
        }));

        console.log(`${managerName}: All dependencies ready`);
    } catch (error) {
        const errorMessage = `${managerName}: Dependency initialization failed: ${error.message}`;
        console.error(errorMessage);
        window.errorUtils?.displayError(errorMessage);
        throw new Error(errorMessage);
    }
}

window.initializeManager = initializeManager;

// Element Availability Observer
function onElementAvailable(selector, callback) {
    const observer = new MutationObserver(() => {
        const element = document.querySelector(selector);
        if (element) {
            observer.disconnect();
            callback(element);
        }
    });

    if (document.body) {
        observer.observe(document.body, { childList: true, subtree: true });
    } else {
        console.debug('Document body not yet available, waiting for DOMContentLoaded...');
        window.addEventListener('DOMContentLoaded', () => {
            observer.observe(document.body, { childList: true, subtree: true });
        });
    }
}
// Example usage for calculations-summary
onElementAvailable('.calculations-summary', (element) => {
    console.debug('Calculations summary ready:', element);
    // Bind events or perform actions here
});

