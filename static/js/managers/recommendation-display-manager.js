// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\managers\recommendation-display-manager.js

class RecommendationDisplayManager {
    constructor() {
        this.recommendationsContainer = document.getElementById('recommendations-container'); // Assuming a container ID
        // Add more specific containers for wall, ceiling, floor if needed
    }

    /**
     * Displays the soundproofing recommendations in the UI.
     * @param {object} recommendationsData - An object containing recommendations, potentially categorized by surface type.
     *   Example: { wall: [...], ceiling: [...], floor: [...] }
     */
    displayRecommendations(recommendationsData) {
        if (!this.recommendationsContainer) {
            console.error('Recommendations container not found.');
            return;
        }

        this.recommendationsContainer.innerHTML = ''; // Clear previous recommendations

        if (!recommendationsData || Object.keys(recommendationsData).length === 0) {
            this.recommendationsContainer.innerHTML = '<p>No recommendations found.</p>';
            return;
        }

        // Handle different types of recommendations (e.g., wall, ceiling, floor)
        for (const type in recommendationsData) {
            if (recommendationsData.hasOwnProperty(type)) {
                const solutions = recommendationsData[type];
                if (solutions && solutions.length > 0) {
                    const typeHeader = document.createElement('h3');
                    typeHeader.textContent = `${type.charAt(0).toUpperCase() + type.slice(1)} Recommendations`;
                    this.recommendationsContainer.appendChild(typeHeader);

                    const ul = document.createElement('ul');
                    solutions.forEach(solution => {
                        const li = document.createElement('li');
                        li.innerHTML = `
                            <strong>${solution.name}</strong><br>
                            Material: ${solution.material || 'N/A'}<br>
                            Cost: $${solution.cost ? solution.cost.toFixed(2) : 'N/A'}<br>
                            STC Rating: ${solution.stc_rating || 'N/A'}
                            ${solution.details ? `<br>Details: ${solution.details}` : ''}
                        `;
                        ul.appendChild(li);
                    });
                    this.recommendationsContainer.appendChild(ul);
                }
            }
        }

        console.log('Recommendations displayed.', recommendationsData);
    }

    // Placeholder for future methods to update specific DOM elements
    _updateDOMElement(elementId, content) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = content;
        }
    }
}

export default RecommendationDisplayManager;
