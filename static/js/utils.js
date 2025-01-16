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
    soundproofing: new Map(),
    noiseData: {
        type: null,
        intensity: 3,
        time: [],
        direction: []
    }
};


async function initializeApplication() {
    try {
        if (document.readyState === 'loading') {
            await new Promise(resolve => document.addEventListener('DOMContentLoaded', resolve));
        }

        

        await waitForDependency('errorUtils');

        const managers = [
            { name: 'roomManager' },
            { name: 'roomCalculator' },
            { name: 'surfaceManager' },
            { name: 'wallManager' },
            { name: 'soundproofingManager' },
            { name: 'workflowManager' }
        ];

        for (const manager of managers) {
            try {
                await initializeManagerWithDependencies({
                    name: manager.name,
                    dependencies: window.InitializationState.dependencies[manager.name]
                });
            } catch (error) {
                console.error(`Failed to initialize ${manager.name}:`, error);
                hideLoadingIndicator();
                throw error;
            }
        }

        console.log('Application initialization complete');
        hideLoadingIndicator();
        return true;
    } catch (error) {
        console.error('Application initialization failed:', error);
        hideLoadingIndicator();
        throw error;
    }
}

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
    try {
        await initializeApplication();
    } catch (error) {
        console.error('Failed to initialize application:', error);
        if (window.errorUtils?.initialized) {
            window.errorUtils.displayError('Failed to initialize application: ' + error.message);
        }
        hideLoadingIndicator();
    }
});

// Global Dependency Tracker
async function waitForDependency(depName) {
    console.log(`Waiting for dependency: ${depName}`);
    return new Promise((resolve) => {
        if (window[depName]?.initialized) {
            console.log(`${depName} already initialized`);
            resolve(true);
            return;
        }

        window.addEventListener(`${depName}Initialized`, () => {
            console.log(`${depName} initialized.`);
            resolve(true);
        }, { once: true });
    });
}
window.waitForDependency = waitForDependency;

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
        window.addEventListener('DOMContentLoaded', () => {
            observer.observe(document.body, { childList: true, subtree: true });
        });
    }
}

async function initializeManagerWithDependencies({ name, dependencies = [] }) {
    console.log(`Initializing ${name} with dependencies:`, dependencies);
    
    // Wait for all dependencies to be initialized
    for (const dep of dependencies) {
        await waitForDependency(dep.toLowerCase());
    }

    // Initialize the manager itself
    const manager = window[name.toLowerCase()];
    if (!manager) {
        throw new Error(`Manager ${name} not found`);
    }

    if (!manager.initialized) {
        await manager.initialize();
    }

    // Wait for initialization event
    await new Promise((resolve) => {
        if (manager.initialized) {
            resolve();
        } else {
            window.addEventListener(`${name.toLowerCase()}Initialized`, () => {
                resolve();
            }, { once: true });
        }
    });

    return true;
}

