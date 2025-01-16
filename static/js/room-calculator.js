if (!window.RoomCalculator) {
    class RoomCalculator {
        constructor() {
            this.initialized = false;
            this.dimensions = {
                length: 0,
                width: 0,
                height: 0
            };
            this.blockageAreas = {
                wall: 0,
                floor: 0,
                ceiling: 0
            };
        }

        initialize() {
            if (this.initialized) return;
            this.bindEvents();
            this.initialized = true;
            window.dispatchEvent(new CustomEvent('roomCalculatorInitialized'));
        }

        bindEvents() {
            const inputs = ['length', 'width', 'height'].map(id => document.getElementById(id));
            inputs.forEach(input => {
                if (input) {
                    input.addEventListener('input', (e) => {
                        const value = parseFloat(e.target.value) || 0;
                        this.dimensions[e.target.id] = value;
                        window.FormState.dimensions[e.target.id] = value;
                        this.updateCalculations();
                    });
                }
            });

            // Listen for blockage updates
            window.addEventListener('blockagesUpdated', (e) => {
                const { surface, totalArea } = e.detail;
                this.blockageAreas[surface] = totalArea;
                this.updateCalculations();
            });
        }

        updateDimensions(newDimensions) {
            this.dimensions = { ...this.dimensions, ...newDimensions };
            window.FormState.dimensions = { ...window.FormState.dimensions, ...newDimensions };
            this.updateCalculations();
        }

        calculateAreas() {
            const { length, width, height } = this.dimensions;
            return {
                walls: 2 * (length * height + width * height) - this.blockageAreas.wall,
                floor: length * width - this.blockageAreas.floor,
                ceiling: length * width - this.blockageAreas.ceiling
            };
        }

        updateCalculations() {
            const areas = this.calculateAreas();
            
            // Update display
            this.updateAreaDisplay('wall-area', areas.walls);
            this.updateAreaDisplay('floor-area', areas.floor);
            this.updateAreaDisplay('ceiling-area', areas.ceiling);

            // Update surface areas in panels
            this.updateSurfaceAreas(areas);
        }

        updateSurfaceAreas(areas) {
            // Update surface area displays in panels
            const wallsPanel = document.querySelector('#walls-panel .surface-area');
            const floorPanel = document.querySelector('#floor-panel .surface-area');
            const ceilingPanel = document.querySelector('#ceiling-panel .surface-area');

            if (wallsPanel) wallsPanel.textContent = `${areas.walls.toFixed(2)} m²`;
            if (floorPanel) floorPanel.textContent = `${areas.floor.toFixed(2)} m²`;
            if (ceilingPanel) ceilingPanel.textContent = `${areas.ceiling.toFixed(2)} m²`;
        }

        updateAreaDisplay(elementId, value) {
            const element = document.getElementById(elementId);
            if (element) {
                element.textContent = value.toFixed(2);
            }
        }
    }

    window.RoomCalculator = RoomCalculator;
}

// Initialize calculator
if (!window.roomCalculator) {
    window.roomCalculator = new RoomCalculator();
    window.roomCalculator.initialize();
}