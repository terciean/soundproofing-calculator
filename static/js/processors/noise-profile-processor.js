// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\processors\noise-profile-processor.js

class NoiseProfileProcessor {
    /**
     * Processes raw noise data, validates it, and transforms it into a standard format.
     * @param {object} rawData - The raw noise data from the frontend.
     * @param {string} rawData.type - The type of noise (e.g., 'traffic', 'neighbors').
     * @param {number} rawData.intensity - The intensity of the noise (0-10).
     * @param {string[]} [rawData.direction] - Optional: Direction(s) of the noise (e.g., ['north', 'east']).
     * @param {number} [rawData.frequency] - Optional: Dominant frequency of the noise.
     * @returns {object} - The processed and validated noise profile.
     * @throws {Error} If required data is missing or invalid.
     */
    processNoiseData(rawData) {
        if (!rawData || typeof rawData.type !== 'string' || !rawData.type.trim()) {
            throw new Error('Noise type is required.');
        }
        if (typeof rawData.intensity === 'undefined' || rawData.intensity === null) {
            throw new Error('Noise intensity is required.');
        }
        if (typeof rawData.intensity !== 'number' || rawData.intensity < 0 || rawData.intensity > 10) {
            throw new Error('Noise intensity must be a number between 0 and 10.');
        }

        const processedData = {
            type: rawData.type.trim(),
            intensity: rawData.intensity,
            direction: Array.isArray(rawData.direction) ? rawData.direction : [],
            frequency: typeof rawData.frequency === 'number' ? rawData.frequency : null // Default to null if not provided
        };

        console.log('Processed Noise Data:', processedData);
        return processedData;
    }
}

export default NoiseProfileProcessor;
