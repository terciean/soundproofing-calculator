// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\main.js

import FormHandlers from './forms/form-handlers-module.js';
import UnifiedSurfaceManager from './managers/unified-surface-manager.js';
import { initializeApp } from './utils/initialize.js';
import ThemeToggle from './utils/theme-toggle.js';
import SolutionProfiles from './solutions/solution-profiles.js';

document.addEventListener('DOMContentLoaded', () => {
    initializeApp(); // Call the initialization function first

    

    const themeToggle = new ThemeToggle();
    // No explicit init() call needed for ThemeToggle as it initializes in constructor

    const solutionProfiles = new SolutionProfiles();
    // Example: Render profiles to a specific container if needed on load
    // solutionProfiles.renderProfiles(document.getElementById('solution-profiles-container'));

    // Initialize other core modules here as they are created
    const formHandlers = new FormHandlers();
    
    const unifiedSurfaceManager= new  UnifiedSurfaceManager();
    
    console.log('Main JavaScript initialized.');


});