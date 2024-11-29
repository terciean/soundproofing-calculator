if (!window.SurfaceManager) {
    class SurfaceManager {
        constructor() {
            this.initialized = false;
            this.surfaces = new Map();
            this.dependencies = ['roomManager', 'roomCalculator'];
            this.initPromise = new Promise(resolve => {
                this.initResolver = resolve;
            });
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
            console.log('SurfaceManager: Checking dependencies...');
            for (const dep of this.dependencies) {
                if (!window[dep]?.initialized) {
                    console.log(`SurfaceManager: Waiting for ${dep}...`);
                    await new Promise(resolve => 
                        window.addEventListener(`${dep}Initialized`, resolve, { once: true })
                    );
                    console.log(`SurfaceManager: Detected ${dep}Initialized event.`);
                }
            }
            console.log('SurfaceManager: All dependencies are ready.');
        }

        async initialize() {
            console.log('SurfaceManager: Starting initialization...');
            if (this.initialized) {
                console.log('SurfaceManager: Already initialized');
                return true;
            }

            await this.waitForDOM();
            await this.waitForDependencies();
            console.log('SurfaceManager: Dependencies are ready');

            await this.initializeSurfaces();
            await this.createSurfacePanels();
            await this.bindEvents();

            this.initialized = true;
            console.log('SurfaceManager: Initialization complete');
            window.dispatchEvent(new CustomEvent('surfaceManagerInitialized'));
            return true;
        }

        async initializeSurfaces() {
            // Initialize surface types
            const surfaceTypes = ['walls', 'ceiling', 'floor'];
            
            surfaceTypes.forEach(type => {
                if (!this.surfaces.has(type)) {
                    this.surfaces.set(type, {
                        material: null,
                        features: new Set(),
                        area: 0
                    });
                }
            });

            // Initialize FormState surfaces if needed
            if (!window.FormState.surfaces) {
                window.FormState.surfaces = new Map();
            }

            // Update initial areas if dimensions are available
            if (window.roomManager?.dimensions) {
                this.updateDimensions(window.roomManager.dimensions);
            }
        }

        async createSurfacePanels() {
            const surfacesContainer = document.querySelector('.surfaces-container');
            if (!surfacesContainer) {
                throw new Error('Surfaces container not found in DOM');
            }

            const surfaceTypes = ['walls', 'ceiling', 'floor'];
            
            surfacesContainer.innerHTML = surfaceTypes.map(type => `
                <div class="surface-panel" id="${type}-panel">
                    <div class="panel-header">
                        <h3>${type.charAt(0).toUpperCase() + type.slice(1)}</h3>
                        <span class="surface-area">${this.surfaces.get(type)?.area.toFixed(2) || 'N/A'} m²</span>
                    </div>
                    <div class="panel-content">
                        <select class="feature-select" id="${type}-material">
                            <option value="">Select Material</option>
                            <option value="concrete">Concrete</option>
                            <option value="drywall">Drywall</option>
                            <option value="brick">Brick</option>
                        </select>
                        <div class="feature-list" id="${type}-features">
                            <!-- Features will be populated dynamically -->
                        </div>
                    </div>
                </div>
            `).join('');
        }

        async bindEvents() {
            // Bind material selection events
            document.querySelectorAll('.feature-select').forEach(select => {
                select.addEventListener('change', (event) => {
                    const surfaceType = event.target.id.split('-')[0];
                    this.updateMaterial(surfaceType, event.target.value);
                });
            });

            // Bind feature selection events
            document.querySelectorAll('.feature-list').forEach(list => {
                list.addEventListener('change', (event) => {
                    if (event.target.type === 'checkbox') {
                        const surfaceType = event.target.closest('.surface-panel').id.split('-')[0];
                        const feature = event.target.value;
                        this.updateFeature(surfaceType, feature, event.target.checked);
                    }
                });
            });

            // Listen for dimension updates
            window.addEventListener('dimensionsUpdated', (event) => {
                if (event.detail) {
                    this.updateDimensions(event.detail);
                }
            });
        }

        updateMaterial(surfaceType, material) {
            const surface = this.surfaces.get(surfaceType);
            if (surface) {
                surface.material = material;
                this.notifyUpdate(surfaceType);
            }
        }

        updateFeature(surfaceType, feature, isEnabled) {
            const surface = this.surfaces.get(surfaceType);
            if (surface) {
                if (isEnabled) {
                    surface.features.add(feature);
                } else {
                    surface.features.delete(feature);
                }
                this.notifyUpdate(surfaceType);
            }
        }

        updateDimensions(dimensions) {
            const { length, width, height } = dimensions;
            
            // Update surface areas
            const areas = {
                walls: 2 * height * (length + width),
                ceiling: length * width,
                floor: length * width
            };

            // Update each surface's area with validation
            Object.entries(areas).forEach(([surface, area]) => {
                const surfaceData = this.surfaces.get(surface);
                if (!surfaceData) {
                    console.warn(`Surface ${surface} not found`); // Log a warning if the surface is missing
                    return; // Exit if the surface is not found
                }
                surfaceData.area = area;
                
                // Update area display in UI
                const areaDisplay = document.querySelector(`#${surface}-panel .surface-area`);
                if (areaDisplay) {
                    areaDisplay.textContent = `${area.toFixed(2)} m²`;
                }
            });

            this.notifyUpdate();
        }

        notifyUpdate(surfaceType = null) {
            // Update FormState
            this.surfaces.forEach((surface, type) => {
                if (!window.FormState.surfaces.has(type)) {
                    window.FormState.surfaces.set(type, new Set());
                }
                window.FormState.surfaces.get(type).clear();
                surface.features.forEach(feature => {
                    window.FormState.surfaces.get(type).add(feature);
                });
            });

            // Notify workflow manager to update validation state
            if (window.workflowManager?.initialized) {
                window.workflowManager.updateNavigationButtons();
            }

            // Dispatch custom event
            window.dispatchEvent(new CustomEvent('surfacesUpdated', {
                detail: {
                    surfaceType,
                    surfaces: this.surfaces
                }
            }));
        }
    }

    window.SurfaceManager = SurfaceManager;

    if (!window.surfaceManager) {
        window.surfaceManager = new SurfaceManager();
        window.addEventListener('load', async () => {
            const initializeSurfaceManager = async () => {
                try {
                    if (!window.errorUtils?.initialized) {
                        console.log('SurfaceManager: Waiting for errorUtils...');
                        await new Promise(resolve => window.addEventListener('errorUtilsInitialized', resolve, { once: true }));
                        console.log('SurfaceManager: Detected errorUtilsInitialized event');
                    }

                    await window.surfaceManager.initialize();
                    console.log('SurfaceManager: Initialization complete');
                    window.dispatchEvent(new CustomEvent('surfaceManagerInitialized'));
                } catch (error) {
                    console.error('Failed to initialize SurfaceManager:', error);
                    window.errorUtils?.displayError('Failed to initialize surface manager');
                }
            };

            ['roomManagerInitialized', 'roomCalculatorInitialized'].forEach(event => {
                window.addEventListener(event, () => {
                    if (window.roomManager?.initialized && window.roomCalculator?.initialized) {
                        initializeSurfaceManager();
                    }
                }, { once: true });
            });

            // Check immediately in case dependencies are already initialized
            if (window.roomManager?.initialized && window.roomCalculator?.initialized) {
                await initializeSurfaceManager();
            }
        });
    }
}