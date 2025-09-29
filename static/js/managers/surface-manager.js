// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\managers\surface-manager.js

import EndpointService from '../services/endpoint-service.js';

class SurfaceManager {
    constructor() {
        this.endpointService = new EndpointService();
        this.surfaces = {
            walls: [],
            ceiling: null,
            floor: null,
            blockages: []
        };
    }

    /**
     * Adds a blockage (e.g., window, door) to a specified surface.
     * @param {string} surfaceId - The ID of the surface the blockage belongs to.
     * @param {object} blockageData - Data for the new blockage (e.g., { type: 'window', dimensions: { width: 1, height: 1.5 } }).
     */
    addBlockage(surfaceId, blockageData) {
        // In a real application, you'd associate blockages with specific walls/surfaces
        // For now, we'll just add to a general blockages array
        this.surfaces.blockages.push({ surfaceId, ...blockageData });
        console.log(`Blockage added to ${surfaceId}:`, blockageData);
        this._recalculateBlockageSummary();
    }

    /**
     * Removes a blockage.
     * @param {string} blockageId - The ID of the blockage to remove.
     */
    removeBlockage(blockageId) {
        this.surfaces.blockages = this.surfaces.blockages.filter(b => b.id !== blockageId);
        console.log(`Blockage removed: ${blockageId}`);
        this._recalculateBlockageSummary();
    }

    /**
     * Updates the type of a wall.
     * @param {string} wallId - The ID of the wall to update.
     * @param {string} newType - The new type of wall (e.g., 'brick', 'drywall').
     */
    updateWallType(wallId, newType) {
        // Find and update the specific wall
        console.log(`Wall ${wallId} type updated to: ${newType}`);
        // This would likely trigger a recalculation of acoustic properties
    }

    /**
     * Updates a feature on a wall (e.g., adding insulation).
     * @param {string} wallId - The ID of the wall.
     * @param {object} featureData - Data for the feature to update/add.
     */
    updateWallFeature(wallId, featureData) {
        console.log(`Wall ${wallId} feature updated:`, featureData);
    }

    /**
     * Updates a general property of a surface (e.g., ceiling material).
     * @param {string} surfaceType - The type of surface ('ceiling', 'floor').
     * @param {object} propertyData - The property data to update.
     */
    updateSurfaceProperty(surfaceType, propertyData) {
        if (this.surfaces[surfaceType]) {
            this.surfaces[surfaceType] = { ...this.surfaces[surfaceType], ...propertyData };
            console.log(`${surfaceType} property updated:`, propertyData);
        } else {
            console.warn(`Surface type ${surfaceType} not found.`);
        }
    }

    /**
     * Recalculates the blockage summary by calling the backend API.
     * @private
     */
    async _recalculateBlockageSummary() {
        try {
            // In a real scenario, you'd send relevant surface and blockage data
            const summaryData = await this.endpointService.calculateBlockageSummary({
                roomDimensions: { length: 10, width: 8, height: 2.5 }, // Dummy data
                blockages: this.surfaces.blockages
            });
            console.log('Blockage Summary:', summaryData);
            // Update UI with summaryData if needed
        } catch (error) {
            console.error('Failed to recalculate blockage summary:', error);
            // Integrate with DisplayManager or error logging
        }
    }

    /**
     * Retrieves the current state of all surfaces.
     * @returns {object} - The current surfaces data.
     */
    getSurfacesData() {
        return this.surfaces;
    }
}

export default SurfaceManager;
