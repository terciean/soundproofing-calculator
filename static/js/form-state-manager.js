if (!window.FormStateManager) {
    class FormStateManager {
        static updateDimensions(newDimensions) {
            window.FormState.dimensions = { 
                ...window.FormState.dimensions,
                ...newDimensions 
            };
            window.dispatchEvent(new CustomEvent('formStateUpdated', { detail: { dimensions: window.FormState.dimensions } }));
        }

        static updateSurfaces(surfaces) {
            window.FormState.surfaces = surfaces;
            window.dispatchEvent(new CustomEvent('formStateUpdated', { detail: { surfaces } }));
        }

        static updateBlockages(surface, blockages) {
            window.FormState.blockages[surface] = blockages;
            window.dispatchEvent(new CustomEvent('formStateUpdated', { 
                detail: { 
                    blockages: window.FormState.blockages,
                    surface,
                    surfaceBlockages: blockages
                } 
            }));
        }

        static updateNoiseData(noiseData) {
            window.FormState.noiseData = {
                ...window.FormState.noiseData,
                ...noiseData
            };
            window.dispatchEvent(new CustomEvent('formStateUpdated', { 
                detail: { 
                    noiseData: window.FormState.noiseData
                } 
            }));
        }

        static getBlockageArea(surface) {
            return window.FormState.blockages[surface].reduce((total, blockage) => {
                if (surface === 'wall') {
                    return total + (blockage.width * blockage.height);
                } else {
                    return total + (blockage.width * blockage.length);
                }
            }, 0);
        }

        static getTotalBlockageArea() {
            return {
                wall: this.getBlockageArea('wall'),
                floor: this.getBlockageArea('floor'),
                ceiling: this.getBlockageArea('ceiling')
            };
        }

        static getNoiseSourceSurfaces() {
            const noiseDirections = window.FormState.noiseData?.direction || [];
            const surfaces = {
                walls: [],
                floor: false,
                ceiling: false
            };

            noiseDirections.forEach(direction => {
                if (direction === 'above') surfaces.ceiling = true;
                else if (direction === 'below') surfaces.floor = true;
                else if (['north', 'east', 'south', 'west'].includes(direction)) {
                    surfaces.walls.push(direction);
                }
            });

            return surfaces;
        }

        static getNoisePriority() {
            const { type, intensity, time } = window.FormState.noiseData || {};
            let priority = 'medium';

            // High priority cases
            if (
                (intensity >= 4) || // High/Very High intensity
                (time?.includes('night')) || // Night-time noise
                (['music', 'machinery'].includes(type)) // Specific noise types
            ) {
                priority = 'high';
            }
            // Low priority cases
            else if (
                (intensity <= 2) && // Low/Very Low intensity
                (!time?.includes('night')) // Not night-time
            ) {
                priority = 'low';
            }

            return priority;
        }
    }

    window.FormStateManager = FormStateManager;
}