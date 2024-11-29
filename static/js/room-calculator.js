if (!window.RoomCalculator) {
    class RoomCalculator {
        constructor() {
            this.dimensions = { length: 0, width: 0, height: 0 };
            this.initialized = false;
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
            console.log('RoomCalculator: Waiting for dependencies...');
            if (!window.roomManager?.initialized) {
                await new Promise(resolve => 
                    window.addEventListener('roomManagerInitialized', resolve, { once: true })
                );
                console.log('RoomCalculator: Detected roomManagerInitialized event');
            }
            console.log('RoomCalculator: All dependencies are ready.');
        }

        async initialize() {
            console.log('RoomCalculator: Starting initialization...');
            if (this.initialized) return true;

            await this.waitForDOM();
            await this.waitForDependencies();
            console.log('RoomCalculator: Dependencies are ready');

            this.bindDimensionInputs();

            this.initialized = true;
            this.initResolver();
            console.log('RoomCalculator initialized successfully');
            window.dispatchEvent(new CustomEvent('roomCalculatorInitialized'));
            return true;
        }

        bindDimensionInputs() {
            const inputs = document.querySelectorAll('.detail-group input[type="number"]');
            if (!inputs.length) {
                console.warn('No dimension inputs found');
                return; // Exit if no inputs are found
            }
            inputs.forEach(input => {
                input.addEventListener('input', debounce((e) => {
                    const value = parseFloat(e.target.value) || 0;
                    this.dimensions[e.target.id] = value;
                    window.roomManager.updateDimensions(this.dimensions);
                    this.updateAreaDisplay();
                }, 300));
            });
        }

        updateAreaDisplay() {
            try {
                const areas = this.calculateAreas();
                const calculationSection = document.querySelector('#calculation-section .calculations-summary');
                
                if (!calculationSection) {
                    console.error('Calculation section not found');
                    return; // Exit if the calculation section is missing
                }
                
                calculationSection.innerHTML = `
                    <h3>Room Calculations</h3>
                    <div class="calculation-grid">
                        <div class="calculation-item" data-tooltip="Total area of all four walls">
                            <span class="label">Wall Area:</span>
                            <span class="value">${areas.walls.toFixed(2)} m²</span>
                        </div>
                        <div class="calculation-item" data-tooltip="Length × Width">
                            <span class="label">Floor Area:</span>
                            <span class="value">${areas.floor.toFixed(2)} m²</span>
                        </div>
                        <div class="calculation-item" data-tooltip="Same as floor area">
                            <span class="label">Ceiling Area:</span>
                            <span class="value">${areas.ceiling.toFixed(2)} m²</span>
                        </div>
                        <div class="calculation-item total" data-tooltip="Total surface area of the room">
                            <span class="label">Total Surface Area:</span>
                            <span class="value">${areas.total.toFixed(2)} m²</span>
                        </div>
                    </div>
                `;
            } catch (error) {
                this.handleError('Failed to update area display', error); // Use ErrorUtils for better error reporting
            }
        }

        calculateAreas() {
            const { length, width, height } = this.dimensions;
            if (length <= 0 || width <= 0 || height <= 0) {
                return { walls: 0, floor: 0, ceiling: 0, total: 0 }; // Return default values
            }
            return {
                walls: 2 * height * (length + width),
                floor: length * width,
                ceiling: length * width,
                total: 2 * height * (length + width) + 2 * (length * width),
            };
        }

        showError(message) {
            console.error(message);
            window.errorUtils?.displayError(message);
        }

        handleError(context, error) {
            const message = `${context}: ${error.message}`;
            console.error(message, error);
            this.showError(message);
        }
    }

    window.RoomCalculator = RoomCalculator;

    if (!window.roomCalculator) {
        window.roomCalculator = new RoomCalculator();
        window.addEventListener('load', () => {
            const initializeCalculator = async () => {
                try {
                    await window.roomCalculator.initialize();
                } catch (error) {
                    console.error('Failed to initialize RoomCalculator:', error);
                    window.errorUtils?.displayError('Failed to initialize room calculator');
                }
            };

            window.addEventListener('roomManagerInitialized', initializeCalculator, { once: true });

            // Check immediately in case roomManager is already initialized
            if (window.roomManager?.initialized) {
                initializeCalculator();
            }
        });
    }
}