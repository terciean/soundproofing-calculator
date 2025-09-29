// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\managers\cost-handler.js

class CostHandler {
    constructor() {
        this.totalCostContainer = document.getElementById('total-cost'); // Assuming an element for total cost
        this.detailedCostContainer = document.getElementById('detailed-cost'); // Assuming an element for detailed breakdown
    }

    /**
     * Displays the cost estimates in the UI.
     * @param {object} costData - An object containing cost details.
     *   Example: { totalCost: 1234.56, breakdown: { materials: [...], labor: [...] } }
     */
    displayCosts(costData) {
        if (!this.totalCostContainer) {
            console.error('Total cost container not found.');
            return;
        }

        this.totalCostContainer.innerHTML = '';
        this.detailedCostContainer.innerHTML = '';

        if (!costData || !costData.totalCost) {
            this.totalCostContainer.innerHTML = '<p>Cost estimation not available.</p>';
            return;
        }

        this.totalCostContainer.innerHTML = `Total Estimated Cost: <strong>$${costData.totalCost.toFixed(2)}</strong>`;

        if (costData.breakdown && this.detailedCostContainer) {
            let breakdownHtml = '<h4>Cost Breakdown:</h4>';
            for (const category in costData.breakdown) {
                if (costData.breakdown.hasOwnProperty(category)) {
                    breakdownHtml += `<h5>${category.charAt(0).toUpperCase() + category.slice(1)}</h5>`;
                    if (Array.isArray(costData.breakdown[category])) {
                        breakdownHtml += '<ul>';
                        costData.breakdown[category].forEach(item => {
                            breakdownHtml += `<li>${item.name}: $${item.cost.toFixed(2)} (${item.quantity} ${item.unit})</li>`;
                        });
                        breakdownHtml += '</ul>';
                    } else if (typeof costData.breakdown[category] === 'object') {
                        breakdownHtml += '<ul>';
                        for (const subCategory in costData.breakdown[category]) {
                            if (costData.breakdown[category].hasOwnProperty(subCategory)) {
                                breakdownHtml += `<li>${subCategory}: $${costData.breakdown[category][subCategory].toFixed(2)}</li>`;
                            }
                        }
                        breakdownHtml += '</ul>';
                    }
                }
            }
            this.detailedCostContainer.innerHTML = breakdownHtml;
        }

        console.log('Costs displayed.', costData);
    }
}

export default CostHandler;
