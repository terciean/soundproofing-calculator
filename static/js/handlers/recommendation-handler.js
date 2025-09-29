// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\handlers\recommendation-handler.js

import EndpointService from '../services/endpoint-service.js';
import RecommendationDisplayManager from '../managers/recommendation-display-manager.js';

class RecommendationHandler {
    constructor() {
        this.endpointService = new EndpointService();
        this.recommendationDisplayManager = new RecommendationDisplayManager();
    }

    /**
     * Orchestrates the process of fetching and displaying soundproofing recommendations.
     * @param {object} formData - The user input data required for generating recommendations.
     */
    async generateAndDisplayRecommendations(formData) {
        try {
            // Pre-processing: You might transform formData here if needed before sending to backend
            console.log('RecommendationHandler: Generating recommendations with data:', formData);

            // Fetch recommendations from the backend
            const rawRecommendations = await this.endpointService.getRecommendations(formData);

            // Post-processing: You might filter, sort, or enhance rawRecommendations here
            const processedRecommendations = this._processRawRecommendations(rawRecommendations);
            console.log('RecommendationHandler: Processed recommendations:', processedRecommendations);

            // Display recommendations in the UI
            this.recommendationDisplayManager.displayRecommendations(processedRecommendations);

            console.log('RecommendationHandler: Recommendations successfully generated and displayed.');
            return processedRecommendations;
        } catch (error) {
            console.error('RecommendationHandler: Error generating or displaying recommendations:', error);
            // Re-throw the error to allow higher-level error handling (e.g., by DisplayManager)
            throw error;
        }
    }

    /**
     * Internal method to process raw recommendations received from the backend.
     * This is a placeholder for any filtering, sorting, or data transformation logic.
     * @param {object} rawRecommendations - The raw recommendation data from the backend.
     * @returns {object} The processed recommendation data.
     * @private
     */
    _processRawRecommendations(rawRecommendations) {
        // Example: Ensure recommendations are in a consistent format
        // For now, just return as is, assuming backend provides suitable format
        return rawRecommendations;
    }
}

export default RecommendationHandler;
