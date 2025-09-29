// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\utils\form-state.js

class FormStateManager {
    constructor() {
        if (FormStateManager.instance) {
            return FormStateManager.instance;
        }

        this.state = {
            currentSection: null,
            completedSections: new Set()
        };

        FormStateManager.instance = this;
    }

    /**
     * Returns the singleton instance of FormStateManager.
     * @returns {FormStateManager} The singleton instance.
     */
    static getInstance() {
        if (!FormStateManager.instance) {
            FormStateManager.instance = new FormStateManager();
        }
        return FormStateManager.instance;
    }

    /**
     * Retrieves the current state of the form.
     * @returns {object} The current form state.
     */
    getState() {
        return { ...this.state, completedSections: Array.from(this.state.completedSections) };
    }

    /**
     * Updates the current active section of the form.
     * @param {string} sectionId - The ID of the current section.
     */
    updateCurrentSection(sectionId) {
        this.state.currentSection = sectionId;
        console.log(`Form state: Current section updated to ${sectionId}`);
    }

    /**
     * Marks a section as completed.
     * @param {string} sectionId - The ID of the section to mark as complete.
     */
    markSectionComplete(sectionId) {
        this.state.completedSections.add(sectionId);
        console.log(`Form state: Section ${sectionId} marked as complete.`);
    }

    /**
     * Checks if a section is completed.
     * @param {string} sectionId - The ID of the section to check.
     * @returns {boolean} True if the section is completed, false otherwise.
     */
    isSectionComplete(sectionId) {
        return this.state.completedSections.has(sectionId);
    }

    /**
     * Resets the form state.
     */
    resetState() {
        this.state = {
            currentSection: null,
            completedSections: new Set()
        };
        console.log('Form state reset.');
    }
}

export default FormStateManager;
