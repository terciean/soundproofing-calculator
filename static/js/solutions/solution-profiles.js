// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\solutions\solution-profiles.js

class SolutionProfiles {
    constructor() {
        // This could be populated from a backend API call or a static JSON file
        this.profiles = [
            {
                id: 'profile-1',
                name: 'Basic Noise Reduction',
                description: 'Ideal for reducing general ambient noise.',
                materials: ['drywall', 'insulation'],
                stc_range: '30-40'
            },
            {
                id: 'profile-2',
                name: 'Advanced Sound Blocking',
                description: 'Designed for significant reduction of loud noises.',
                materials: ['mass loaded vinyl', 'double drywall'],
                stc_range: '50-60'
            }
        ];
    }

    /**
     * Retrieves all available solution profiles.
     * @returns {Array<object>} An array of solution profile objects.
     */
    getAllProfiles() {
        return this.profiles;
    }

    /**
     * Retrieves a specific solution profile by its ID.
     * @param {string} profileId - The ID of the solution profile.
     * @returns {object|undefined} The solution profile object, or undefined if not found.
     */
    getProfileById(profileId) {
        return this.profiles.find(profile => profile.id === profileId);
    }

    /**
     * Renders the solution profiles to a specified DOM element.
     * @param {HTMLElement} containerElement - The DOM element to render profiles into.
     */
    renderProfiles(containerElement) {
        if (!containerElement) {
            console.error('Container element for solution profiles not found.');
            return;
        }

        containerElement.innerHTML = ''; // Clear existing content

        this.profiles.forEach(profile => {
            const profileDiv = document.createElement('div');
            profileDiv.className = 'solution-profile-card';
            profileDiv.innerHTML = `
                <h3>${profile.name}</h3>
                <p>${profile.description}</p>
                <p><strong>Materials:</strong> ${profile.materials.join(', ')}</p>
                <p><strong>STC Range:</strong> ${profile.stc_range}</p>
            `;
            containerElement.appendChild(profileDiv);
        });

        console.log('Solution profiles rendered.');
    }
}

export default SolutionProfiles;
