if (!window.FormStateManager) {
    class FormStateManager {
        static updateDimensions(newDimensions) {
            // Validate dimensions before merging
            if (!Object.values(newDimensions).every(value => value > 0)) {
                window.errorUtils?.displayError('Invalid dimensions provided.'); // Display error if dimensions are invalid
                return; // Exit if validation fails
            }
            window.FormState.dimensions = { 
                ...window.FormState.dimensions, // Merge updated dimensions
                ...newDimensions 
            };
            window.dispatchEvent(new CustomEvent('formStateUpdated', { detail: { dimensions: window.FormState.dimensions } }));
        }

        static updateSurfaces(surfaces) {
            window.FormState.surfaces = surfaces;
            window.dispatchEvent(new CustomEvent('formStateUpdated', { detail: { surfaces } }));
        }

        // Add more methods as needed for other FormState updates
    }

    window.FormStateManager = FormStateManager;
}