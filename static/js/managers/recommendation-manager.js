// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\managers\recommendation-manager.js

import RecommendationHandler from '../handlers/recommendation-handler.js';

class RecommendationManager {
    constructor() {
        this.recommendationHandler = new RecommendationHandler();
        this.recommendationHistory = []; // Simple in-memory history
        this.currentStrategy = 'default'; // Placeholder for different strategies
    }

    /**
     * Requests recommendations based on user input and current strategy.
     * @param {object} formData - The user input data.
     * @returns {Promise<object>} A promise that resolves with the recommendations.
     */
    async getRecommendations(formData) {
        try {
            console.log(`RecommendationManager: Using strategy '${this.currentStrategy}' to get recommendations.`);
            const recommendations = await this.recommendationHandler.generateAndDisplayRecommendations(formData);
            this._addToHistory(recommendations);
            return recommendations;
        } catch (error) {
            console.error('RecommendationManager: Error getting recommendations:', error);
            throw error;
        }
    }

    /**
     * Sets the recommendation strategy to be used.
     * @param {string} strategyName - The name of the strategy (e.g., 'cost-effective', 'high-performance').
     */
    setStrategy(strategyName) {
        // In a more complex system, this might involve loading different handler implementations
        this.currentStrategy = strategyName;
        console.log(`Recommendation strategy set to: ${strategyName}`);
    }

    /**
     * Retrieves the recommendation history.
     * @returns {Array<object>} An array of past recommendations.
     */
    getHistory() {
        return [...this.recommendationHistory]; // Return a copy to prevent external modification
    }

    /**
     * Adds recommendations to the history.
     * @param {object} recommendations - The recommendations to add.
     * @private
     */
    _addToHistory(recommendations) {
        this.recommendationHistory.push({ timestamp: new Date(), recommendations });
        // Limit history size if needed
        if (this.recommendationHistory.length > 10) {
            this.recommendationHistory.shift();
        }
    }

    /**
     * Clears the recommendation history.
     */
    clearHistory() {
        this.recommendationHistory = [];
        console.log('Recommendation history cleared.');
    }
}

export default RecommendationManager;
