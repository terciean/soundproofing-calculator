if (!window.SurfaceManager) {
    class SurfaceManager {
        constructor() {
            this.initialized = false;
            this.surfaces = new Map();
            this.blockages = {
                wall: new Map(),
                floor: new Map(),
                ceiling: new Map()
            };
            this.blockageCounters = {
                wall: 1,
                floor: 1,
                ceiling: 1
            };
            this.modals = {};
            
            // Initialize FormState if needed
            if (!window.FormState) {
                window.FormState = {};
            }
            if (!window.FormState.blockages) {
                window.FormState.blockages = {
                    wall: [],
                    floor: [],
                    ceiling: []
                };
            }
            if (!window.FormState.blockageAreas) {
                window.FormState.blockageAreas = {
                    wall: 0,
                    floor: 0,
                    ceiling: 0
                };
            }

            // Bind methods
            this.initializeAfterDOM = this.initializeAfterDOM.bind(this);
            this.handleBlockageFormSubmit = this.handleBlockageFormSubmit.bind(this);
            this.openModal = this.openModal.bind(this);
            this.closeModal = this.closeModal.bind(this);
            this.bindEvents = this.bindEvents.bind(this);
            this.addBlockage = this.addBlockage.bind(this);
            this.removeBlockage = this.removeBlockage.bind(this);
            this.setupExistingBlockages = this.setupExistingBlockages.bind(this);
        }

        initialize() {
            if (this.initialized) return;

            // Wait for DOM to be ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', this.initializeAfterDOM);
            } else {
                this.initializeAfterDOM();
            }
        }

        initializeAfterDOM() {
            console.log('Initializing SurfaceManager...');
            
            // Ensure the surface features section exists
            const surfaceFeaturesSection = document.getElementById('surface-details');
            if (!surfaceFeaturesSection) {
                console.error('Surface features section not found');
                return;
            }

            this.bindEvents();
            this.setupExistingBlockages();
            
            this.initialized = true;
            window.dispatchEvent(new CustomEvent('surfaceManagerInitialized'));
        }

        setupExistingBlockages() {
            console.log('Setting up existing blockages...');
            if (window.FormState?.blockages) {
                Object.entries(window.FormState.blockages).forEach(([surface, blockages]) => {
                    if (Array.isArray(blockages)) {
                        blockages.forEach(blockage => {
                            this.addBlockage(surface, blockage);
                        });
                        this.updateBlockageSummary(surface);
                    }
                });
            }
        }

        bindEvents() {
            if (this.eventsbound) return;
            
            // Blockage buttons for all surfaces
            ['wall', 'floor', 'ceiling'].forEach(surface => {
                const addBlockageBtn = document.getElementById(`add-${surface}-blockage`);
                if (addBlockageBtn) {
                    addBlockageBtn.addEventListener('click', () => {
                        const modal = document.getElementById(`${surface}-blockage-modal`);
                        if (modal) {
                            modal.style.display = 'block';
                            modal.classList.add('active');
                        }
                    });
                }
            });

            // Modal event handlers
            ['wall', 'floor', 'ceiling'].forEach(surface => {
                const modal = document.getElementById(`${surface}-blockage-modal`);
                if (modal) {
                    // Close buttons
                    const closeButtons = modal.querySelectorAll('.close-modal, .cancel-blockage');
                    closeButtons.forEach(button => {
                        button.addEventListener('click', () => {
                            modal.style.display = 'none';
                            modal.classList.remove('active');
                        });
                    });

                    // Close on outside click
                    modal.addEventListener('click', (e) => {
                        if (e.target === modal) {
                            modal.style.display = 'none';
                            modal.classList.remove('active');
                        }
                    });

                    // Form submission
                    const form = modal.querySelector(`#${surface}-blockage-form`);
                    if (form) {
                        form.addEventListener('submit', (e) => {
                            e.preventDefault();
                            this.handleBlockageFormSubmit(surface, e.target);
                        });
                    }
                }
            });

            // Remove blockage buttons
            document.addEventListener('click', (e) => {
                if (e.target.classList.contains('remove-blockage')) {
                    const blockageItem = e.target.closest('.blockage-item');
                    if (blockageItem) {
                        const surface = blockageItem.dataset.surface;
                        const blockageId = blockageItem.dataset.blockageId;
                        this.removeBlockage(surface, blockageId);
                    }
                }
            });
            
            this.eventsbound = true;
        }

        openModal(surface) {
            console.log(`Opening ${surface} modal`);
            const modal = document.getElementById(`${surface}-blockage-modal`);
            if (modal) {
                modal.style.display = 'block';
                modal.classList.add('active');
                const form = modal.querySelector(`#${surface}-blockage-form`);
                if (form) {
                    form.reset();
                    const firstInput = form.querySelector('select, input');
                    if (firstInput) firstInput.focus();
                }
            }
        }

        closeModal(surface) {
            const modal = document.getElementById(`${surface}-blockage-modal`);
            if (modal) {
                modal.style.display = 'none';
                modal.classList.remove('active');
            }
        }

        handleBlockageFormSubmit(surface, form) {
            console.log(`Handling ${surface} blockage form submit`);
            const formData = new FormData(form);
            const blockageType = formData.get('type');
            
            // Set default dimensions for electrical outlets
            let width = parseFloat(formData.get('width')) || 0;
            let height = parseFloat(formData.get('height')) || 0;
            
            if (blockageType === 'electrical-outlet') {
                width = width || 0.1;  // Default 10cm width
                height = height || 0.1; // Default 10cm height
            }

            const blockageData = {
                id: this.blockageCounters[surface]++,
                surface,
                type: blockageType,
                width: width,
                length: parseFloat(formData.get('length')) || 0,
                height: height,
                notes: formData.get('notes') || ''
            };

            if (surface === 'wall') {
                blockageData.wall = formData.get('wall');
            }

            this.addBlockage(surface, blockageData);
            this.closeModal(surface);
            form.reset();
        }

        addBlockage(surface, blockageData) {
            console.log(`Adding ${surface} blockage:`, blockageData);
            
            // Store in FormState
            if (!Array.isArray(window.FormState.blockages[surface])) {
                window.FormState.blockages[surface] = [];
            }
            window.FormState.blockages[surface].push(blockageData);
            
            // Update UI
            let blockagesList;
            if (surface === 'wall') {
                blockagesList = document.getElementById(`${blockageData.wall}-wall-blockages`);
            } else {
                blockagesList = document.getElementById(`${surface}-blockages`);
            }
            
            if (!blockagesList) {
                console.warn(`Blockages list for ${surface} not found`);
                return;
            }

            const typeLabel = this.getTypeLabel(surface, blockageData.type);
            const dimensions = surface === 'wall'
                ? `${blockageData.width}m × ${blockageData.height}m (${(blockageData.width * blockageData.height).toFixed(2)}m²)`
                : `${blockageData.width}m × ${blockageData.length}m (${(blockageData.width * blockageData.length).toFixed(2)}m²)`;

            const wallLabel = surface === 'wall' 
                ? `<div class="blockage-wall">${blockageData.wall.charAt(0).toUpperCase() + blockageData.wall.slice(1)} Wall</div>`
                : '';

            const blockageHtml = `
                <div class="blockage-item" data-blockage-id="${blockageData.id}" data-surface="${surface}" ${surface === 'wall' ? `data-wall="${blockageData.wall}"` : ''}>
                    <div class="blockage-info">
                        ${wallLabel}
                        <div class="blockage-type">${typeLabel}</div>
                        <div class="blockage-dimensions">${dimensions}</div>
                        ${blockageData.notes ? `<div class="blockage-notes">${blockageData.notes}</div>` : ''}
                    </div>
                    <div class="blockage-actions">
                        <button type="button" class="remove-blockage" title="Remove blockage">×</button>
                    </div>
                </div>
            `;

            blockagesList.insertAdjacentHTML('beforeend', blockageHtml);
            this.blockages[surface].set(blockageData.id.toString(), blockageData);
            this.updateBlockageSummary(surface);
        }

        removeBlockage(surface, blockageId) {
            const blockageItem = document.querySelector(`.blockage-item[data-surface="${surface}"][data-blockage-id="${blockageId}"]`);
            if (blockageItem) {
                blockageItem.remove();
                this.blockages[surface].delete(blockageId);
                
                // Update FormState
                if (Array.isArray(window.FormState.blockages[surface])) {
                    window.FormState.blockages[surface] = window.FormState.blockages[surface].filter(
                        b => b.id.toString() !== blockageId.toString()
                    );
                }
                
                this.updateBlockageSummary(surface);
            }
        }

        updateBlockageSummary(surface) {
            let totalArea = 0;
            let totalCount = 0;

            this.blockages[surface].forEach(blockage => {
                totalCount++;
                if (surface === 'wall') {
                    totalArea += blockage.width * blockage.height;
                } else {
                    totalArea += blockage.width * blockage.length;
                }
            });

            const totalBlockagesElement = document.getElementById(`${surface}-total-blockages`);
            const totalAreaElement = document.getElementById(`${surface}-total-blockage-area`);

            if (totalBlockagesElement) totalBlockagesElement.textContent = totalCount;
            if (totalAreaElement) totalAreaElement.textContent = totalArea.toFixed(2);

            // Update FormState
            window.FormState.blockageAreas[surface] = totalArea;
            
            // Dispatch event for other components
            window.dispatchEvent(new CustomEvent('blockagesUpdated', {
                detail: { surface, totalArea, totalCount }
            }));
        }

        getTypeLabel(surface, type) {
            return type.split('-').map(word => 
                word.charAt(0).toUpperCase() + word.slice(1)
            ).join(' ');
        }
    }

    window.SurfaceManager = SurfaceManager;
}

// Initialize manager
if (!window.surfaceManager) {
    window.surfaceManager = new SurfaceManager();
    window.surfaceManager.initialize();
}