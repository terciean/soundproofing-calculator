// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\utils\initialize.js

import SurfaceManager from '../managers/surface-manager.js';
import FormHandlers from '../forms/form-handlers-module.js';

/**
 * Performs initial setup and configurations for the application.
 * This function is called once when the application loads.
 */
export function initializeApp() {
    console.log('Initializing application...');

    // 1. Perform initial DOM manipulations or setup
    // Example: Add a class to the body when JS is loaded
    document.body.classList.add('js-loaded');

    // 2. Load initial data (e.g., from local storage or a config endpoint)
    // Placeholder for fetching config from an endpoint
    // fetch('/api/config')
    //     .then(response => response.json())
    //     .then(config => {
    //         console.log('Loaded initial config:', config);
    //         // Store config globally or pass to relevant modules
    //     })
    //     .catch(error => console.error('Failed to load initial config:', error));

    // Example: Load data from local storage
    const savedTheme = localStorage.getItem('appTheme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        console.log(`Loaded theme from local storage: ${savedTheme}`);
    }

    // 3. Set up global event listeners not tied to a specific module
    // Example: Global window resize listener
    window.addEventListener('resize', () => {
        console.log('Window resized!');
        // Potentially trigger responsive UI updates here
    });

    // Initialize SurfaceManager and FormHandlers
    const unifiedSurfaceManager = new SurfaceManager();
    const formHandlers = new FormHandlers(unifiedSurfaceManager);
    formHandlers.init();

    console.log('Application initialization complete.');
}
