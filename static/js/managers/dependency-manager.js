// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\managers\dependency-manager.js

class DependencyManager {
    constructor() {
        this.loadedScripts = new Set(); // Registry of successfully loaded script URLs
        this.loadingPromises = new Map(); // Map of URL to Promise for scripts currently loading
    }

    /**
     * Dynamically loads a JavaScript file.
     * @param {string} url - The URL of the JavaScript file to load.
     * @returns {Promise<void>} A promise that resolves when the script is loaded, or rejects on error.
     */
    loadScript(url) {
        if (this.loadedScripts.has(url)) {
            console.log(`Script already loaded: ${url}`);
            return Promise.resolve();
        }

        if (this.loadingPromises.has(url)) {
            console.log(`Script already loading: ${url}`);
            return this.loadingPromises.get(url);
        }

        const promise = new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = url;
            script.async = true; // Load asynchronously

            script.onload = () => {
                this.loadedScripts.add(url);
                this.loadingPromises.delete(url);
                console.log(`Script loaded successfully: ${url}`);
                resolve();
            };

            script.onerror = (error) => {
                this.loadingPromises.delete(url);
                console.error(`Failed to load script: ${url}`, error);
                reject(new Error(`Failed to load script: ${url}`));
            };

            document.head.appendChild(script);
        });

        this.loadingPromises.set(url, promise);
        return promise;
    }

    /**
     * Loads multiple JavaScript files and ensures all are loaded.
     * @param {string[]} urls - An array of URLs of JavaScript files to load.
     * @returns {Promise<void[]>} A promise that resolves when all scripts are loaded.
     */
    loadScripts(urls) {
        const promises = urls.map(url => this.loadScript(url));
        return Promise.all(promises);
    }

    /**
     * Checks if a script has been successfully loaded.
     * @param {string} url - The URL of the script to check.
     * @returns {boolean} True if the script is loaded, false otherwise.
     */
    isScriptLoaded(url) {
        return this.loadedScripts.has(url);
    }

    /**
     * Clears the registry of loaded scripts.
     * Useful for testing or specific scenarios where scripts need to be reloaded.
     */
    clearLoadedScripts() {
        this.loadedScripts.clear();
        this.loadingPromises.clear();
        console.log('DependencyManager: Cleared all loaded script registries.');
    }
}

export default DependencyManager;
