// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\managers\container-manager.js

class ContainerManager {
    constructor() {
        this.containerStates = new Map(); // Stores the state of each container (e.g., 'active', 'collapsed')
    }

    /**
     * Shows a specific container by making it visible.
     * @param {string} containerId - The ID of the container to show.
     */
    showContainer(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.style.display = 'block'; // Or 'flex', 'grid', etc., based on CSS
            this.containerStates.set(containerId, 'active');
            console.log(`Container ${containerId} shown.`);
        } else {
            console.warn(`Container with ID ${containerId} not found.`);
        }
    }

    /**
     * Hides a specific container by making it invisible.
     * @param {string} containerId - The ID of the container to hide.
     */
    hideContainer(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.style.display = 'none';
            this.containerStates.set(containerId, 'hidden');
            console.log(`Container ${containerId} hidden.`);
        } else {
            console.warn(`Container with ID ${containerId} not found.`);
        }
    }

    /**
     * Toggles the visibility of a specific container.
     * @param {string} containerId - The ID of the container to toggle.
     */
    toggleContainer(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            if (container.style.display === 'none') {
                this.showContainer(containerId);
            } else {
                this.hideContainer(containerId);
            }
            console.log(`Container ${containerId} toggled.`);
        } else {
            console.warn(`Container with ID ${containerId} not found.`);
        }
    }

    /**
     * Dynamically loads content into a specified container.
     * @param {string} containerId - The ID of the container to load content into.
     * @param {string} contentHtml - The HTML string to load into the container.
     */
    loadContent(containerId, contentHtml) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = contentHtml;
            console.log(`Content loaded into container ${containerId}.`);
        } else {
            console.warn(`Container with ID ${containerId} not found for content loading.`);
        }
    }

    /**
     * Sets a custom state for a container.
     * @param {string} containerId - The ID of the container.
     * @param {string} state - The state to set (e.g., 'active', 'collapsed', 'expanded').
     */
    setContainerState(containerId, state) {
        this.containerStates.set(containerId, state);
        console.log(`Container ${containerId} state set to: ${state}`);
        // Optionally, apply CSS classes based on state
        const container = document.getElementById(containerId);
        if (container) {
            container.classList.remove('active', 'collapsed', 'expanded', 'hidden'); // Remove common states
            container.classList.add(state);
        }
    }

    /**
     * Gets the current state of a container.
     * @param {string} containerId - The ID of the container.
     * @returns {string|undefined} The state of the container, or undefined if not managed.
     */
    getContainerState(containerId) {
        return this.containerStates.get(containerId);
    }
}

export default ContainerManager;
