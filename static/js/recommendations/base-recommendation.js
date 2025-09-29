// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\recommendations\base-recommendation.js

/**
 * Represents a base structure for a soundproofing recommendation.
 * This class can be extended by more specific recommendation types.
 */
class BaseRecommendation {
    constructor({
        id = `rec-${Date.now()}`,
        name = 'Unnamed Recommendation',
        description = '',
        type = 'general', // e.g., 'wall', 'ceiling', 'floor', 'overall'
        materials = [],
        cost = 0,
        stcRating = null,
        details = {}
    } = {}) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.type = type;
        this.materials = materials;
        this.cost = cost;
        this.stcRating = stcRating;
        this.details = details;
    }

    /**
     * Returns a plain object representation of the recommendation.
     * @returns {object} The recommendation data as a plain object.
     */
    toObject() {
        return {
            id: this.id,
            name: this.name,
            description: this.description,
            type: this.type,
            materials: this.materials,
            cost: this.cost,
            stcRating: this.stcRating,
            details: this.details
        };
    }

    /**
     * Provides a string summary of the recommendation.
     * @returns {string} A summary string.
     */
    getSummary() {
        return `${this.name} (${this.type}): ${this.description}. Estimated Cost: $${this.cost.toFixed(2)}. STC: ${this.stcRating || 'N/A'}`;
    }

    // Placeholder for potential utility methods
    /**
     * Filters an array of recommendations based on a criteria.
     * @param {Array<BaseRecommendation>} recommendations - The array of recommendations to filter.
     * @param {function} filterFn - The filtering function.
     * @returns {Array<BaseRecommendation>} The filtered array.
     */
    static filter(recommendations, filterFn) {
        return recommendations.filter(filterFn);
    }

    /**
     * Sorts an array of recommendations based on a comparator.
     * @param {Array<BaseRecommendation>} recommendations - The array of recommendations to sort.
     * @param {function} compareFn - The comparison function.
     * @returns {Array<BaseRecommendation>} The sorted array.
     */
    static sort(recommendations, compareFn) {
        return [...recommendations].sort(compareFn);
    }
}

export default BaseRecommendation;
