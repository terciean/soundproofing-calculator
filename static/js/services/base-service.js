// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\services\base-service.js

class BaseService {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
        this.cache = new Map(); // Simple in-memory cache
    }

    /**
     * Makes an HTTP request to the specified endpoint.
     * @param {string} endpoint - The API endpoint (e.g., '/recommendations').
     * @param {string} method - The HTTP method (e.g., 'GET', 'POST').
     * @param {object} [data=null] - The data to send with the request (for POST/PUT).
     * @param {boolean} [useCache=false] - Whether to use caching for GET requests.
     * @returns {Promise<object>} - A promise that resolves with the JSON response.
     */
    async request(endpoint, method = 'GET', data = null, useCache = false) {
        const url = `${this.baseURL}${endpoint}`;
        const cacheKey = `${method}-${url}-${JSON.stringify(data)}`;

        if (useCache && method === 'GET' && this.cache.has(cacheKey)) {
            console.log(`[BaseService] Cache hit for ${url}`);
            return this.cache.get(cacheKey);
        }

        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ message: response.statusText }));
                throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorData.message}`);
            }

            const result = await response.json();

            if (useCache && method === 'GET') {
                this.cache.set(cacheKey, result);
            }

            return result;
        } catch (error) {
            console.error(`[BaseService] Request to ${url} failed:`, error);
            // Integrate with a dedicated error logging module later
            // For now, re-throw to allow calling modules to handle
            throw error;
        }
    }

    /**
     * Clears the entire cache or a specific entry.
     * @param {string} [cacheKey=null] - The specific cache key to clear. If null, clears all.
     */
    clearCache(cacheKey = null) {
        if (cacheKey) {
            this.cache.delete(cacheKey);
            console.log(`[BaseService] Cleared cache for key: ${cacheKey}`);
        } else {
            this.cache.clear();
            console.log('[BaseService] Cleared all cache entries.');
        }
    }

    // Placeholder for future error logging integration
    logError(error, context = {}) {
        console.error('Error logged:', error, context);
        // This would eventually send errors to a centralized error logging service
    }
}

// Export the BaseService class for use in other modules
export default BaseService;
