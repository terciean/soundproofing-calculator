// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\managers\display-manager.js

class DisplayManager {
    constructor() {
        this.loadingIndicator = document.getElementById('loading-indicator'); // Assuming a loading indicator element
        this.messageContainer = document.getElementById('message-container'); // Assuming a message display element
        // Add more elements for sections and navigation as needed
    }

    /**
     * Shows a specific UI section.
     * @param {string} sectionId - The ID of the section to show.
     */
    showSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = 'block'; // Or 'flex', 'grid', etc., depending on CSS
        }
    }

    /**
     * Hides a specific UI section.
     * @param {string} sectionId - The ID of the section to hide.
     */
    hideSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = 'none';
        }
    }

    /**
     * Shows the loading indicator.
     */
    showLoadingIndicator() {
        if (this.loadingIndicator) {
            this.loadingIndicator.style.display = 'block';
        }
    }

    /**
     * Hides the loading indicator.
     */
    hideLoadingIndicator() {
        if (this.loadingIndicator) {
            this.loadingIndicator.style.display = 'none';
        }
    }

    /**
     * Displays a message to the user.
     * @param {string} message - The message to display.
     * @param {string} type - The type of message (e.g., 'success', 'error', 'info').
     */
    showMessage(message, type = 'info') {
        if (this.messageContainer) {
            this.messageContainer.textContent = message;
            this.messageContainer.className = `message ${type}`; // Apply CSS class for styling
            this.messageContainer.style.display = 'block';
        }
    }

    /**
     * Clears any displayed messages.
     */
    clearMessage() {
        if (this.messageContainer) {
            this.messageContainer.textContent = '';
            this.messageContainer.className = 'message';
            this.messageContainer.style.display = 'none';
        }
    }

    /**
     * Updates the navigation state (e.g., active step, progress bar).
     * This is a placeholder and would need specific implementation based on your HTML structure.
     */
    updateNavigationState() {
        console.log('Updating navigation state (placeholder).');
        // Example: Highlight current step in a multi-step form
        // const currentStep = this.getCurrentStep();
        // document.querySelectorAll('.nav-step').forEach(step => {
        //     if (step.dataset.step === currentStep) {
        //         step.classList.add('active');
        //     } else {
        //         step.classList.remove('active');
        //     }
        // });
    }
}

export default DisplayManager;
