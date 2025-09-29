// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\utils\dimensions-input.js

class DimensionsInput {
    constructor() {
        this.lengthInput = document.getElementById('room-length'); // Assuming input field IDs
        this.widthInput = document.getElementById('room-width');
        this.heightInput = document.getElementById('room-height');
    }

    /**
     * Retrieves and validates room dimensions from input fields.
     * @returns {object} An object containing length, width, and height.
     * @throws {Error} If any dimension is invalid or missing.
     */
    getDimensions() {
        const length = parseFloat(this.lengthInput ? this.lengthInput.value : '');
        const width = parseFloat(this.widthInput ? this.widthInput.value : '');
        const height = parseFloat(this.heightInput ? this.heightInput.value : '');

        this._validateDimension(length, 'Length');
        this._validateDimension(width, 'Width');
        this._validateDimension(height, 'Height');

        // Basic range validation (adjust as needed for your application's requirements)
        if (length <= 0 || width <= 0 || height <= 0) {
            throw new Error('Room dimensions must be positive numbers.');
        }
        if (length > 100 || width > 100 || height > 50) { // Example max values
            throw new Error('Room dimensions seem unusually large. Please check your input.');
        }

        return {
            length: length,
            width: width,
            height: height
        };
    }

    /**
     * Validates a single dimension value.
     * @param {number} value - The dimension value to validate.
     * @param {string} name - The name of the dimension (e.g., 'Length').
     * @private
     * @throws {Error} If the value is not a valid number.
     */
    _validateDimension(value, name) {
        if (isNaN(value) || value === null) {
            throw new Error(`${name} must be a valid number.`);
        }
    }
}

export default DimensionsInput;
