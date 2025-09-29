// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\services\endpoint-service.js

import BaseService from './base-service.js';

class EndpointService extends BaseService {
    constructor() {
        super();
    }

    /**
     * Fetches soundproofing recommendations from the backend.
     * @param {object} data - The data required for recommendations (e.g., room dimensions, noise profile).
     * @returns {Promise<object>} - A promise that resolves with the recommendations.
     */
    async getRecommendations(data) {
        try {
            return await this.request('/recommendations', 'POST', data);
        } catch (error) {
            this.logError(error, { endpoint: '/recommendations', data });
            throw error;
        }
    }

    /**
     * Calculates costs for soundproofing solutions.
     * @param {object} data - The data required for cost calculation.
     * @returns {Promise<object>} - A promise that resolves with the cost details.
     */
    async calculateCosts(data) {
        try {
            return await this.request('/calculate-costs', 'POST', data);
        } catch (error) {
            this.logError(error, { endpoint: '/calculate-costs', data });
            throw error;
        }
    }

    /**
     * Processes user inputs.
     * @param {object} data - The user input data.
     * @returns {Promise<object>} - A promise that resolves with the processing result.
     */
    async processInputs(data) {
        try {
            return await this.request('/process-inputs', 'POST', data);
        } catch (error) {
            this.logError(error, { endpoint: '/process-inputs', data });
            throw error;
        }
    }

    /**
     * Calculates blockage summary.
     * @param {object} data - The data required for blockage summary.
     * @returns {Promise<object>} - A promise that resolves with the blockage summary.
     */
    async calculateBlockageSummary(data) {
        try {
            return await this.request('/calculate_blockage_summary', 'POST', data);
        } catch (error) {
            this.logError(error, { endpoint: '/calculate_blockage_summary', data });
            throw error;
        }
    }

    /**
     * Fetches solutions by surface type.
     * @param {string} surfaceType - The type of surface (e.g., 'wall', 'ceiling', 'floor').
     * @returns {Promise<object>} - A promise that resolves with the solutions for the given surface type.
     */
    async getSolutionsByType(surfaceType) {
        try {
            return await this.request(`/solutions/${surfaceType}`, 'GET', null, true);
        } catch (error) {
            this.logError(error, { endpoint: `/solutions/${surfaceType}` });
            throw error;
        }
    }
}

export default EndpointService;
