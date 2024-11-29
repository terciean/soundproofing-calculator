if (!window.ErrorUtils) {
    class ErrorUtils {
        constructor() {
            this.initialized = false;
            this.initPromise = new Promise((resolve) => {
                this.initResolver = resolve;
            });
            this.errorContainer = null;
            this.activeErrors = new Set();
            this.maxErrors = 3;
            this.errorTimeout = 5000;
            this.errorQueue = [];
        }

        async initialize() {
            console.log('ErrorUtils: Starting initialization...');
            try {
                console.log('ErrorUtils: Performing setup...');
                await new Promise(resolve => setTimeout(resolve, 500)); // Simulate async setup
                console.log('ErrorUtils: Setup complete.');
        
                this.initialized = true; // Mark as initialized
                this.initResolver(); // Resolve the initialization promise
        
                // Dispatch the initialization event
                window.dispatchEvent(new CustomEvent('errorUtilsInitialized'));
                console.log('ErrorUtils: Initialization complete.');
            } catch (error) {
                console.error('ErrorUtils initialization failed:', error);
                this.createFallbackErrorDisplay(error); // Display fallback error
                throw error; // Propagate the error for further handling
            }
        }
        

        async waitForDOM() {
            return new Promise(resolve => {
                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', resolve, { once: true });
                } else {
                    resolve();
                }
            });
        }

        createFallbackErrorDisplay(error) {
            console.error('ErrorUtils initialization failed:', error);
            if (document.body) {
                const fallbackError = document.createElement('div');
                fallbackError.style.cssText = 'position:fixed;top:10px;right:10px;background:red;color:white;padding:10px;z-index:9999;border-radius:4px;box-shadow:0 2px 4px rgba(0,0,0,0.2);';
                fallbackError.textContent = `ErrorUtils initialization failed: ${error.message}`;
                document.body.appendChild(fallbackError);
                setTimeout(() => fallbackError.remove(), 5000);
            }
        }

        displayError(message, type = 'error') {
            console.error(message); // Always log to console
            
            try {
                if (!this.errorContainer) {
                    console.warn('Error container not found; recreating dynamically.');
                    this.errorContainer = this.createErrorContainer();
                }
                
                const errorElement = document.createElement('div');
                errorElement.className = `error-message ${type}`;
                errorElement.textContent = message;
                
                this.errorContainer.appendChild(errorElement);
                this.activeErrors.add(errorElement);

                if (this.activeErrors.size > this.maxErrors) {
                    const oldestError = this.activeErrors.values().next().value;
                    oldestError.remove();
                    this.activeErrors.delete(oldestError);
                }

                setTimeout(() => {
                    errorElement.remove();
                    this.activeErrors.delete(errorElement);
                }, this.errorTimeout);
            } catch (error) {
                console.error('Failed to display error:', error);
                this.createFallbackErrorDisplay(new Error(message));
            }
        }

        createErrorContainer() {
            let container = document.getElementById('error-container');
            if (!container) {
                container = document.createElement('div');
                container.id = 'error-container';
                container.className = 'error-container';
                container.setAttribute('role', 'alert');
                container.setAttribute('aria-live', 'polite');
                if (document.body) {
                    document.body.insertBefore(container, document.body.firstChild);
                }
            }
            return container;
        }

        processErrorQueue() {
            while (this.errorQueue.length > 0) {
                const err = this.errorQueue.shift();
                this.displayError(err.message, err.type);
            }
        }

        clearErrors() {
            this.activeErrors.forEach(error => error.remove());
            this.activeErrors.clear();
        }

        initializeErrorContainer() {
            if (!document.getElementById('error-container')) {
                const container = document.createElement('div');
                container.id = 'error-container';
                container.className = 'error-container';
                document.body.appendChild(container);
            }
        }
    }

    // Create instance immediately
    window.errorUtils = new ErrorUtils();
    
    // Initialize immediately and handle errors
    const initializeErrorUtils = async () => {
        try {
            if (!window.errorUtils.initialized) {
                console.log('ErrorUtils: Starting initialization...');
                await window.errorUtils.initialize();
                console.log('ErrorUtils: Successfully initialized');
                window.dispatchEvent(new CustomEvent('errorUtilsInitialized'));
            }
        } catch (error) {
            console.error('ErrorUtils: Failed to initialize:', error);
            // Create fallback error display
            const fallbackError = document.createElement('div');
            fallbackError.style.cssText = 'position:fixed;top:10px;right:10px;background:red;color:white;padding:10px;z-index:9999;border-radius:4px;box-shadow:0 2px 4px rgba(0,0,0,0.2);';
            fallbackError.textContent = 'Error system initialization failed';
            if (document.body) {
                document.body.appendChild(fallbackError);
                setTimeout(() => fallbackError.remove(), 5000);
            }
        }
    };

    // Start initialization based on document state
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeErrorUtils, { once: true });
    } else {
        initializeErrorUtils();
    }
}

// Make safeDisplayError globally available
window.safeDisplayError = (message, type = 'error') => {
    console.error(message); // Always log to console
    
    if (window.errorUtils?.initialized) {
        window.errorUtils.displayError(message, type);
    } else {
        // Create temporary error display
        const tempError = document.createElement('div');
        tempError.style.cssText = 'position:fixed;top:10px;right:10px;background:red;color:white;padding:10px;z-index:9999;border-radius:4px;box-shadow:0 2px 4px rgba(0,0,0,0.2);';
        tempError.textContent = message;
        if (document.body) {
            document.body.appendChild(tempError);
            setTimeout(() => tempError.remove(), 5000);
        }
        
        // Queue error for when ErrorUtils initializes
        if (window.errorUtils) {
            window.errorUtils.errorQueue.push({ message, type });
        }
    }
};