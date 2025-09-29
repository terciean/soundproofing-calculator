// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\surfaces\surface-controller.js

import SurfaceManager from '../managers/surface-manager.js';

class SurfaceController {
    constructor() {
        this.surfaceManager = new SurfaceManager();
        this.addBlockageButton = document.getElementById('add-blockage-button'); // Example UI element
        this.wallTypeSelect = document.getElementById('wall-type-select'); // Example UI element
        // Add more UI elements as needed for other surface controls
    }

    init() {
        if (this.addBlockageButton) {
            this.addBlockageButton.addEventListener('click', this.handleAddBlockage.bind(this));
        }
        if (this.wallTypeSelect) {
            this.wallTypeSelect.addEventListener('change', this.handleWallTypeChange.bind(this));
        }
        // Initialize other event listeners
    }

    /**
     * Handles the click event for adding a blockage.
     */
    handleAddBlockage() {
        // Example: Collect data from UI for a new blockage
        const surfaceId = 'wall-1'; // Get from UI
        const blockageData = { id: `blockage-${Date.now()}`, type: 'window', dimensions: { width: 1, height: 1.5 } }; // Get from UI
        this.surfaceManager.addBlockage(surfaceId, blockageData);
        this.updateBlockageUI();
    }

    /**
     * Handles the change event for wall type selection.
     */
    handleWallTypeChange() {
        const wallId = 'wall-1'; // Get from UI
        const newType = this.wallTypeSelect.value;
        this.surfaceManager.updateWallType(wallId, newType);
        // Update UI to reflect new wall type if necessary
    }

    /**
     * Updates the UI to reflect changes in blockages.
     */
    updateBlockageUI() {
        const blockages = this.surfaceManager.getSurfacesData().blockages;
        console.log('Updating blockage UI with:', blockages);
        // Logic to render/update blockage elements in the DOM
    }

    // Add more methods for other UI interactions and updates
}

export default SurfaceController;
