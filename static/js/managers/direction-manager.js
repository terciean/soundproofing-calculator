// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\managers\direction-manager.js

class DirectionManager {
    constructor(inputElementIds = []) {
        this.inputElements = inputElementIds.map(id => document.getElementById(id)).filter(el => el);
        this.validDirections = new Set(['north', 'south', 'east', 'west', 'up', 'down']); // Extend as needed
    }

    /**
     * Retrieves selected noise direction values from UI elements.
     * Assumes input elements are checkboxes or similar with 'value' attributes.
     * @returns {string[]} An array of selected and validated directions.
     * @throws {Error} If any selected direction is invalid.
     */
    getDirections() {
        const selectedDirections = [];
        this.inputElements.forEach(input => {
            if (input.checked) {
                const direction = input.value.toLowerCase();
                if (!this.validDirections.has(direction)) {
                    throw new Error(`Invalid noise direction selected: ${direction}`);
                }
                selectedDirections.push(direction);
            }
        });
        return selectedDirections;
    }

    /**
     * Sets the state of UI elements based on provided noise direction values.
     * @param {string[]} directions - An array of directions to set as selected.
     */
    setDirections(directions) {
        this.inputElements.forEach(input => {
            const direction = input.value.toLowerCase();
            if (directions.includes(direction)) {
                input.checked = true;
            } else {
                input.checked = false;
            }
        });
        console.log('Directions set in UI:', directions);
    }

    /**
     * Validates a single direction string.
     * @param {string} direction - The direction string to validate.
     * @returns {boolean} True if the direction is valid, false otherwise.
     */
    isValidDirection(direction) {
        return this.validDirections.has(direction.toLowerCase());
    }
}

export default DirectionManager;
