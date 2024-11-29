if (!window.SoundproofingManager) {
    class SoundproofingManager {
        constructor() {
            this.initialized = false;
            this.initPromise = new Promise(resolve => {
                this.initResolver = resolve;
            });
            this.selectedSolutions = new Map();
            this.noiseReductionGoal = 35;
            this.dependencies = ['roomManager'];
        }

        async waitForDOM() {
            return new Promise(resolve => {
                if (document.readyState === 'complete') {
                    resolve();
                } else {
                    window.addEventListener('load', resolve);
                }
            });
        }

        async waitForDependencies() {
            console.log('SoundproofingManager: Checking dependencies...');
            for (const dep of this.dependencies) {
                if (!window[dep]?.initialized) {
                    console.log(`SoundproofingManager: Waiting for ${dep}...`);
                    await new Promise(resolve => 
                        window.addEventListener(`${dep}Initialized`, resolve, { once: true })
                    );
                    console.log(`SoundproofingManager: Detected ${dep}Initialized event.`);
                }
            }
            console.log('SoundproofingManager: All dependencies are ready.');
        }

        async initialize() {
            console.log('SoundproofingManager: Starting initialization...');
            if (this.initialized) return true;

            await this.waitForDOM();
            await this.waitForDependencies();
            console.log('SoundproofingManager: Dependencies are ready');

            await this.fetchSolutions();
            await this.bindEvents();

            this.initialized = true;
            console.log('SoundproofingManager: Initialization complete');
            window.dispatchEvent(new CustomEvent('soundproofingManagerInitialized'));
            return true;
        }

        async fetchSolutions(surfaceType) {
            if (!surfaceType) {
                console.error('Surface type is undefined. Cannot fetch solutions.');
                window.errorUtils?.displayError('Surface type not defined.');
                return [];
            }

            const url = `http://192.168.0.228:10000/get_solutions/${surfaceType}`;
            try {
                console.log(`Fetching solutions for ${surfaceType} from ${url}`);
                const response = await fetch(url);
                if (!response.ok) throw new Error(`Failed to fetch solutions for ${surfaceType}: ${response.statusText}`);
                const solutions = await response.json();
                console.log(`Successfully fetched solutions for ${surfaceType}:`, solutions);
                return solutions;
            } catch (error) {
                console.error(`Error fetching solutions for ${surfaceType}:`, error);
                window.errorUtils?.displayError(`Failed to fetch solutions for ${surfaceType}`);
                return [];
            }
        }

        updateSolutionsList(containerId, solutions) {
            const container = document.querySelector(`#${containerId} .solution-list`);
            if (!container) return;

            container.innerHTML = solutions.map(solution => `
                <div class="solution-item" data-solution="${solution}">
                    <h5>${solution}</h5>
                    <div class="solution-preview">
                        <span class="noise-reduction">Up to ${this.getNoiseReduction(solution)}dB</span>
                    </div>
                </div>
            `).join('');
        }

        getNoiseReduction(solution) {
            // This would be replaced with actual data from your backend
            return Math.floor(Math.random() * 20) + 40; // Placeholder
        }

        bindEvents() {
            // Noise reduction slider
            const slider = document.getElementById('noise-reduction');
            const valueDisplay = document.getElementById('noise-value');

            if (slider && valueDisplay) {
                slider.addEventListener('input', (e) => {
                    const value = parseInt(e.target.value); // Allow unrestricted values
                    valueDisplay.textContent = value;
                    this.noiseReductionGoal = value; // Update noise reduction goal
                    this.updateRecommendations();
                });
            }

            // Solution selection
            document.querySelectorAll('.solution-item').forEach(item => {
                item.addEventListener('click', () => {
                    const solution = item.dataset.solution;
                    const category = item.closest('.solution-category').id.split('-')[0];
                    
                    this.selectSolution(category, solution);
                    this.updateSolutionDetails(solution);
                });
            });
        }

        selectSolution(category, solution) {
            // Update selection state
            this.selectedSolutions.set(category, solution);
            
            // Update UI
            document.querySelectorAll(`#${category}-solutions .solution-item`).forEach(item => {
                item.classList.toggle('selected', item.dataset.solution === solution);
            });

            // Notify other managers
            if (window.roomManager) {
                window.roomManager.updateSoundproofing(category, solution);
            }
        }

        updateSolutionDetails(solution) {
            const detailsContainer = document.querySelector('.details-content');
            if (!detailsContainer) return;

            // This would be replaced with actual data from your backend
            detailsContainer.innerHTML = `
                <div class="detail-grid">
                    <div class="detail-item">
                        <h5>Noise Reduction</h5>
                        <p>${this.getNoiseReduction(solution)}dB</p>
                    </div>
                    <div class="detail-item">
                        <h5>Installation Time</h5>
                        <p>2-3 days</p>
                    </div>
                    <div class="detail-item">
                        <h5>Cost Range</h5>
                        <p>$$$</p>
                    </div>
                </div>
            `;
        }

        updateRecommendations() {
            // Update recommended solutions based on noise reduction goal
            document.querySelectorAll('.solution-item').forEach(item => {
                const noiseReduction = this.getNoiseReduction(item.dataset.solution);
                item.classList.toggle('recommended', noiseReduction >= this.noiseReductionGoal);
            });
        }
    }
    window.SoundproofingManager = SoundproofingManager;
}

if (!window.soundproofingManager) {
    window.soundproofingManager = new SoundproofingManager();
    
    const initializeSoundproofingManager = async () => {
        try {
            console.log('Starting SoundproofingManager initialization...');
            await window.soundproofingManager.initialize();
            console.log('SoundproofingManager initialization completed successfully');
        } catch (error) {
            console.error('Failed to initialize SoundproofingManager:', error);
            window.errorUtils?.displayError(`Soundproofing manager initialization failed: ${error.message}`);
        }
    };

    // Initialize when DOM is ready
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        initializeSoundproofingManager();
    } else {
        window.addEventListener('DOMContentLoaded', initializeSoundproofingManager);
    }
}