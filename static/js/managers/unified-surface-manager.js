/**
 * @fileoverview Provides a unified interface for managing surface-related data and UI interactions.
 * This manager combines the responsibilities of data management and UI control for all surfaces.
 */

import EndpointService from '../services/endpoint-service.js';

class UnifiedSurfaceManager {
    /**
     * Constructs a new UnifiedSurfaceManager.
     * This class is designed as a singleton.
     */
    constructor() {
        if (UnifiedSurfaceManager.instance) {
            return UnifiedSurfaceManager.instance;
        }
        UnifiedSurfaceManager.instance = this;

        this.endpointService = new EndpointService();
        this.surfaces = {}; // In-memory store for surface data

        this._initialize();
    }

    /**
     * Initializes the UnifiedSurfaceManager, setting up event listeners and initial state.
     * @private
     */
    _initialize() {
        this._initializeEventListeners();
        console.log("UnifiedSurfaceManager initialized and event listeners are set up.");
    }

    /**
     * Sets up all necessary event listeners for surface-related UI elements.
     * @private
     */
    _initializeEventListeners() {
        // Example: Event listener for a button to add a blockage
        const addBlockageButton = document.getElementById('add-blockage-button');
        if (addBlockageButton) {
            addBlockageButton.addEventListener('click', () => {
                // Logic to get surfaceId and blockageData from the form
                const surfaceId = document.getElementById('surface-select').value;
                const blockageData = {
                    type: document.getElementById('blockage-type').value,
                    dimensions: {
                        width: parseFloat(document.getElementById('blockage-width').value),
                        height: parseFloat(document.getElementById('blockage-height').value)
                    }
                };
                this.addBlockage(surfaceId, blockageData);
            });
        }

        // Example: Event listener for a dropdown to change a wall's type
        const wallTypeSelect = document.getElementById('wall-type-select');
        if (wallTypeSelect) {
            wallTypeSelect.addEventListener('change', (event) => {
                const wallId = 'wall1'; // Example: assuming a single wall for now
                const newType = event.target.value;
                this.updateSurfaceProperty(wallId, 'type', newType);
            });
        }

        // Add more listeners for other surface interactions as needed
    }

    /**
     * Adds a blockage to a specified surface.
     * @param {string} surfaceId - The ID of the surface (e.g., 'wall1', 'ceiling').
     * @param {object} blockageData - Data for the new blockage.
     */
    async addBlockage(surfaceId, blockageData) {
        if (!this.surfaces[surfaceId]) {
            this.surfaces[surfaceId] = { blockages: [] };
        }
        this.surfaces[surfaceId].blockages.push(blockageData);

        // After adding the blockage, recalculate the summary
        await this._recalculateBlockageSummary();
        this.refreshSurfaceUI(surfaceId);
    }

    /**
     * Removes a blockage from a specified surface.
     * @param {string} surfaceId - The ID of the surface.
     * @param {string} blockageId - The ID of the blockage to remove.
     */
    async removeBlockage(surfaceId, blockageId) {
        if (this.surfaces[surfaceId] && this.surfaces[surfaceId].blockages) {
            this.surfaces[surfaceId].blockages = this.surfaces[surfaceId].blockages.filter(b => b.id !== blockageId);
            await this._recalculateBlockageSummary();
            this.refreshSurfaceUI(surfaceId);
        }
    }

    /**
     * Updates a property of a specific surface.
     * @param {string} surfaceId - The ID of the surface.
     * @param {string} property - The property to update (e.g., 'type', 'material').
     * @param {*} value - The new value for the property.
     */
    updateSurfaceProperty(surfaceId, property, value) {
        if (!this.surfaces[surfaceId]) {
            this.surfaces[surfaceId] = {};
        }
        this.surfaces[surfaceId][property] = value;
        console.log(`Surface ${surfaceId} property ${property} updated to ${value}.`);
        this.refreshSurfaceUI(surfaceId);
    }

    /**
     * Recalculates the blockage summary by calling the backend.
     * @private
     */
    async _recalculateBlockageSummary() {
        try {
            const allBlockages = Object.values(this.surfaces).flatMap(s => s.blockages || []);
            const summary = await this.endpointService.calculateBlockageSummary(allBlockages);
            // Update the UI with the new summary
            const summaryElement = document.getElementById('blockage-summary');
            if (summaryElement) {
                summaryElement.textContent = `Total blockage area: ${summary.totalArea.toFixed(2)} sq meters`;
            }
        } catch (error) {
            console.error("Error recalculating blockage summary:", error);
            // Optionally, display an error to the user
        }
    }

    /**
     * Refreshes the UI for a specific surface to reflect its current state.
     * @param {string} surfaceId - The ID of the surface to refresh.
     */
    refreshSurfaceUI(surfaceId) {
        const surface = this.surfaces[surfaceId];
        if (!surface) return;

        // Example: Update the display for the number of blockages
        const blockageCountElement = document.getElementById(`${surfaceId}-blockage-count`);
        if (blockageCountElement) {
            blockageCountElement.textContent = surface.blockages ? surface.blockages.length : 0;
        }

        // Example: Update the display for the wall type
        const wallTypeElement = document.getElementById(`${surfaceId}-type-display`);
        if (wallTypeElement) {
            wallTypeElement.textContent = surface.type || 'N/A';
        }

        console.log(`UI for surface ${surfaceId} has been refreshed.`);
    }

    /**
     * Retrieves all surface data.
     * @returns {object} The current state of all surfaces.
     */
    getAllSurfaceData() {
        return this.surfaces;
    }
}

// Export the class as the default export
export default UnifiedSurfaceManager;