if (!window.FormState) {
    window.FormState = {
        currentStep: 0,
        dimensions: {
            length: null,
            width: null,
            height: null
        },
        roomType: null,
        surfaces: {},
        blockages: {
            wall: [],
            floor: [],
            ceiling: []
        },
        blockageAreas: {
            wall: 0,
            floor: 0,
            ceiling: 0
        },
        noiseData: {
            type: null,
            intensity: 3,
            time: [],
            direction: []
        },
        recommendations: {
            primary: null,
            alternatives: []
        },
        costs: {
            wall: 0,
            floor: 0,
            ceiling: 0,
            total: 0
        },
        
        updateState(key, value) {
            if (key in this) {
                this[key] = value;
                this.notifyStateChange(key);
            }
        },

        notifyStateChange(key) {
            window.dispatchEvent(new CustomEvent('formStateChanged', {
                detail: {
                    key,
                    value: this[key],
                    state: { ...this }
                }
            }));
        },

        getBlockagesByWall(wall) {
            return this.blockages.wall.filter(b => b.wall === wall);
        },

        getTotalBlockageArea() {
            return {
                wall: this.blockages.wall.reduce((total, b) => total + (b.width * b.height), 0),
                floor: this.blockages.floor.reduce((total, b) => total + (b.width * b.length), 0),
                ceiling: this.blockages.ceiling.reduce((total, b) => total + (b.width * b.length), 0)
            };
        },

        reset() {
            this.currentStep = 0;
            this.dimensions = { length: null, width: null, height: null };
            this.roomType = null;
            this.surfaces = {};
            this.blockages = {
                wall: [],
                floor: [],
                ceiling: []
            };
            this.blockageAreas = {
                wall: 0,
                floor: 0,
                ceiling: 0
            };
            this.noiseData = {
                type: null,
                intensity: 3,
                time: [],
                direction: []
            };
            this.recommendations = {
                primary: null,
                alternatives: []
            };
            this.costs = {
                wall: 0,
                floor: 0,
                ceiling: 0,
                total: 0
            };
            this.notifyStateChange('reset');
        }
    };
} 