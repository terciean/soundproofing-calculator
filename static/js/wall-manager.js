if (!window.WallManager) {
    class WallManager {
        constructor() {
            this.initialized = false;
            this.features = [];
            this.selectedFeatures = new Set();
            this.initPromise = new Promise((resolve) => {
                this.initResolver = resolve;
            });
            this.dependencies = ['roomManager', 'surfaceManager', 'roomCalculator'];
            this.eventsbound = false;
        }
        async waitForDOM() {
            return new Promise(resolve => {
                if (document.readyState === 'complete' || document.readyState === 'interactive') {
                    resolve();
                } else {
                    window.addEventListener('DOMContentLoaded', resolve);
                }
            });
        }
        async waitForDependencies() {
            console.log('WallManager: Checking dependencies...');
            for (const dep of this.dependencies) {
                await new Promise(resolve => {
                    const checkDependency = () => {
                        if (window[dep]?.initialized) {
                            console.log(`WallManager: ${dep} dependency ready`);
                            resolve();
                        } else {
                            console.log(`WallManager: Waiting for ${dep}...`);
                            window.addEventListener(`${dep}Initialized`, checkDependency, { once: true });
                        }
                    };
                    checkDependency();
                });
            }
            console.log('WallManager: All dependencies ready');
        }

        async createRequiredContainers() {
            const container = document.createElement('div');
            container.id = 'wall-features-content';
            container.className = 'wall-features-content';

            const parentElement = document.querySelector('.wall-features');
            console.log('WallManager: Looking for parent element for wall features...');
            console.log('WallManager: Current DOM:', document.body.innerHTML);
            if (parentElement) {
                parentElement.appendChild(container);
                console.log('WallManager: Required containers created');
            } else {
                console.error('WallManager: Parent element for wall features not found. Please ensure the HTML structure is correct.');
                throw new Error('Parent element for wall features not found');
            }
        }
        async initialize() {
            try {
                console.log('WallManager: Starting initialization');
                await this.waitForDOM();
                await this.waitForDependencies();

                // Log the current state of the DOM
                console.log('WallManager: Current DOM:', document.body.innerHTML);

                // Check if the wall features section is present
                const parentElement = document.querySelector('.wall-features');
                if (!parentElement) {
                    throw new Error('Wall features section not found in the DOM.');
                }

                // Create required containers first
                await this.createRequiredContainers();

                // Fetch solutions and initialize container
                await this.fetchSolutions();

                // Bind events after container is initialized
                await this.bindEvents();

                this.initialized = true;
                this.initResolver();
                console.log('WallManager: Initialization complete');
                return true;
            } catch (error) {
                console.error('WallManager: Initialization failed:', error);
                window.errorUtils?.displayError('Failed to initialize wall manager');
                return false;
            }
        }

        

        

        async fetchSolutions() {
            try {
                console.log('WallManager: Fetching solutions...');
                const response = await fetch('/get_solutions/walls');
                if (!response.ok) {
                    throw new Error(`Failed to fetch wall solutions: ${response.statusText}`);
                }

                const solutions = await response.json();
                if (!Array.isArray(solutions)) {
                    throw new Error('Invalid solutions data received');
                }

                this.features = solutions;
                console.log('WallManager: Solutions fetched:', solutions);

                // Initialize the container after fetching solutions
                await this.initializeContainer();
                return true;
            } catch (error) {
                console.error('WallManager: Failed to fetch solutions:', error);
                window.errorUtils?.displayError('Failed to load wall features');
                throw error;
            }
        }

        async initializeContainer() {
            try {
                const container = document.querySelector('#wall-features-content');
                if (!container) {
                    throw new Error('Wall features container not found');
                }

                const featureElements = this.features
                    .map(feature => this.createFeatureElement(feature))
                    .filter(element => element)
                    .join('');

                container.innerHTML = featureElements;
                console.log('WallManager: Container initialized');
                return true;
            } catch (error) {
                console.error('WallManager: Failed to initialize container:', error);
                throw error;
            }
        }

        async bindEvents() {
            // Panel toggle
            const header = document.querySelector('.wall-features .panel-header');
            const content = document.querySelector('#wall-features-content');

            if (header && content) {
                header.addEventListener('click', () => {
                    content.classList.toggle('active');
                    const icon = header.querySelector('.toggle-icon');
                    if (icon) {
                        icon.textContent = content.classList.contains('active') ? '▼' : '▶';
                    }
                });
            }

            // Feature checkboxes
            const checkboxes = document.querySelectorAll('.wall-features input[type="checkbox"]');
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', (e) => this.handleFeatureChange(e));
            });

            // Material select
            const materialSelect = document.getElementById('wall-material');
            if (materialSelect) {
                materialSelect.addEventListener('change', (e) => {
                    if (window.surfaceManager) {
                        window.surfaceManager.updateMaterial('wall', e.target.value);
                    }
                });
            }

            this.eventsbound = true;
            console.log('WallManager: Events bound successfully');
        }

        handleFeatureChange(event) {
            if (!this.initialized) {
                console.warn('WallManager not initialized');
                return;
            }

            const checkbox = event.target;
            const featureValue = checkbox.value;
            const featureType = checkbox.dataset.type;

            try {
                if (checkbox.checked) {
                    this.selectedFeatures.add(featureValue);
                } else {
                    this.selectedFeatures.delete(featureValue);
                }

                if (window.FormState?.surfaces) {
                    if (!window.FormState.surfaces.has('wall')) {
                        window.FormState.surfaces.set('wall', new Set());
                    }
                    window.FormState.surfaces.get('wall').clear();
                    this.selectedFeatures.forEach(feature => {
                        window.FormState.surfaces.get('wall').add(feature);
                    });
                }

                if (window.surfaceManager) {
                    window.surfaceManager.updateFeatures('wall', Array.from(this.selectedFeatures));
                }

                window.dispatchEvent(new CustomEvent('wallFeaturesChanged', {
                    detail: {
                        features: Array.from(this.selectedFeatures),
                        type: featureType
                    }
                }));

            } catch (error) {
                console.error('Failed to update wall features:', error);
                window.errorUtils?.displayError('Failed to update wall features');
                checkbox.checked = !checkbox.checked;
            }
        }
    }

    window.WallManager = WallManager;

    if (!window.wallManager) {
        window.wallManager = new WallManager();
        document.addEventListener('DOMContentLoaded', () => {
            console.log('DOM fully loaded. Checking dependencies...');
            const checkDependencies = () => {
                const allDependenciesReady = window.roomManager?.initialized && 
                                            window.surfaceManager?.initialized;
                if (allDependenciesReady) {
                    window.wallManager.initialize().then(() => {
                        window.dispatchEvent(new CustomEvent('wallManagerInitialized'));
                    });
                }
            };

            ['roomManagerInitialized', 'surfaceManagerInitialized'].forEach(event => {
                window.addEventListener(event, checkDependencies);
            });
            checkDependencies(); // Check immediately in case already initialized
        });
    }
}