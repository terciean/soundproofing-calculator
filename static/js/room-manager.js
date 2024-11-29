if (!window.RoomManager) {
    class RoomManager {
        constructor() {
            this.dimensions = { length: 0, width: 0, height: 0 };
            this.initialized = false;
            this.initPromise = new Promise(resolve => {
                this.initResolver = resolve;
            });
            this.dependencies = ['errorUtils'];
            this.eventsbound = false;
            this.domReady = false;
        }

        async waitForDOM() {
            return new Promise(resolve => {
                const checkDOM = () => {
                    if (document.readyState === 'complete' || document.readyState === 'interactive') {
                        this.domReady = true;
                        resolve();
                    } else {
                        document.addEventListener('DOMContentLoaded', () => {
                            this.domReady = true;
                            resolve();
                        }, { once: true });
                    }
                };
                checkDOM();
            });
        }

        async waitForDependencies() {
            console.log('RoomManager: Waiting for dependencies...');
            try {
                await Promise.all(
                    this.dependencies.map(dep =>
                        new Promise(resolve => {
                            const checkDependency = () => {
                                if (window[dep]?.initialized) {
                                    console.log(`RoomManager: ${dep} dependency ready`);
                                    resolve();
                                } else {
                                    console.log(`RoomManager: Waiting for ${dep}...`);
                                    window.addEventListener(`${dep}Initialized`, checkDependency, { once: true });
                                }
                            };
                            checkDependency();
                        })
                    )
                );
                console.log('RoomManager: All dependencies ready.');
            } catch (error) {
                console.error('RoomManager: Dependency check failed:', error);
                throw new Error('RoomManager dependencies failed to initialize.');
            }
        }

        async bindEvents() {
            if (this.eventsbound) return true;

            try {
                if (!this.domReady) {
                    await this.waitForDOM();
                }

                const dimensionInputs = document.querySelectorAll('.dimension-input');
                dimensionInputs.forEach(input => {
                    input.addEventListener('change', (e) => {
                        this.updateDimensions({
                            [e.target.name]: parseFloat(e.target.value) || 0
                        });
                    });
                });

                this.eventsbound = true;
                console.log('RoomManager: Events bound successfully');
                return true;
            } catch (error) {
                console.error('RoomManager: Failed to bind events:', error);
                throw error;
            }
        }

        async initialize() {
            console.log('RoomManager: Starting initialization...');
            if (this.initialized) return true;

            await this.waitForDOM();

            // Wait for errorUtils to be initialized
            if (!window.errorUtils?.initialized) {
                console.log('RoomManager: Waiting for errorUtils...');
                await new Promise(resolve => 
                    window.addEventListener('errorUtilsInitialized', resolve, { once: true })
                );
                console.log('RoomManager: Detected errorUtilsInitialized event');
            }

            await this.waitForDependencies();
            console.log('RoomManager: Dependencies are ready');

            await this.bindEvents();
            this.initialized = true;

            console.log('RoomManager: Initialization complete');
            window.dispatchEvent(new CustomEvent('roomManagerInitialized'));
            return true;
        }

        updateDimensions(dimensions) {
            try {
                Object.assign(this.dimensions, dimensions);
                window.FormState.dimensions = { ...this.dimensions };
                window.dispatchEvent(new CustomEvent('dimensionsUpdated', { 
                    detail: this.dimensions 
                }));
            } catch (error) {
                console.error('RoomManager: Failed to update dimensions:', error);
                window.errorUtils?.displayError('Failed to update room dimensions');
            }
        }
    }

    window.roomManager = new RoomManager();

    // Initialize RoomManager when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => window.roomManager.initialize());
    } else {
        window.roomManager.initialize();
    }
}