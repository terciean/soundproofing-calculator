/**
 * Utility functions for resetting frontend singleton states during testing.
 */

/**
 * Reset all frontend singletons stored in the window object
 */
export function resetFrontendSingletons() {
  console.log('Resetting all frontend singletons for testing');
  
  // Reset all window-based singletons
  if (window.baseService) {
    try {
      if (typeof window.baseService.cleanup === 'function') {
        window.baseService.cleanup();
      }
    } catch (e) {
      console.warn('Error cleaning up baseService:', e);
    }
    window.baseService = null;
  }
  
  if (window.workflowManager) {
    try {
      if (typeof window.workflowManager.cleanup === 'function') {
        window.workflowManager.cleanup();
      }
    } catch (e) {
      console.warn('Error cleaning up workflowManager:', e);
    }
    window.workflowManager = null;
  }
  
  if (window.consolidatedErrorManager) {
    try {
      if (typeof window.consolidatedErrorManager.cleanup === 'function') {
        window.consolidatedErrorManager.cleanup();
      }
    } catch (e) {
      console.warn('Error cleaning up consolidatedErrorManager:', e);
    }
    window.consolidatedErrorManager = null;
  }
  
  if (window.dataService) {
    try {
      if (typeof window.dataService.cleanup === 'function') {
        window.dataService.cleanup();
      }
    } catch (e) {
      console.warn('Error cleaning up dataService:', e);
    }
    window.dataService = null;
  }
  
  if (window.costManager) {
    try {
      if (typeof window.costManager.cleanup === 'function') {
        window.costManager.cleanup();
      }
    } catch (e) {
      console.warn('Error cleaning up costManager:', e);
    }
    window.costManager = null;
  }
  
  if (window.roomManager) {
    try {
      if (typeof window.roomManager.cleanup === 'function') {
        window.roomManager.cleanup();
      }
    } catch (e) {
      console.warn('Error cleaning up roomManager:', e);
    }
    window.roomManager = null;
  }
  
  // Reset any other singleton cleanup flags
  window.singletonCleanupRegistered = false;
  
  // Force garbage collection if available (mainly for testing environments)
  if (window.gc && typeof window.gc === 'function') {
    try {
      window.gc();
    } catch (e) {
      // Ignore errors - gc() might not be available
    }
  }
  
  console.log('Frontend singletons reset complete');
}

/**
 * Reset a specific frontend singleton by name
 * @param {string} singletonName - Name of the singleton to reset
 */
export function resetSpecificSingleton(singletonName) {
  if (window[singletonName]) {
    try {
      if (typeof window[singletonName].cleanup === 'function') {
        window[singletonName].cleanup();
      }
    } catch (e) {
      console.warn(`Error cleaning up ${singletonName}:`, e);
    }
    window[singletonName] = null;
    console.log(`${singletonName} singleton reset`);
  }
}

/**
 * Create mock implementations for testing
 */
export const MockSingletons = {
  /**
   * Create a mock WorkflowManager for testing
   */
  createMockWorkflowManager() {
    return {
      currentStep: 1,
      workflows: new Map(),
      
      createWorkflow(id) {
        this.workflows.set(id, { step: 1, data: {} });
        return this.workflows.get(id);
      },
      
      updateWorkflow(id, data) {
        if (this.workflows.has(id)) {
          Object.assign(this.workflows.get(id).data, data);
        }
      },
      
      nextStep() {
        this.currentStep = Math.min(this.currentStep + 1, 4);
      },
      
      previousStep() {
        this.currentStep = Math.max(this.currentStep - 1, 1);
      },
      
      cleanup() {
        this.workflows.clear();
        console.log('MockWorkflowManager cleaned up');
      }
    };
  },
  
  /**
   * Create a mock ConsolidatedErrorManager for testing
   */
  createMockErrorManager() {
    return {
      errors: [],
      
      logError(error, context = '') {
        this.errors.push({ error, context, timestamp: Date.now() });
        console.log('Mock error logged:', error);
      },
      
      clearErrors() {
        this.errors = [];
      },
      
      getErrors() {
        return [...this.errors];
      },
      
      cleanup() {
        this.clearErrors();
        console.log('MockErrorManager cleaned up');
      }
    };
  },
  
  /**
   * Create a mock DataService for testing
   */
  createMockDataService() {
    return {
      cache: new Map(),
      
      async fetchData(endpoint) {
        // Return mock data based on endpoint
        const mockData = {
          '/api/solutions': { solutions: [] },
          '/api/materials': { materials: [] },
          '/api/calculate': { result: 'mock calculation' }
        };
        
        return mockData[endpoint] || { data: 'mock response' };
      },
      
      cacheData(key, data) {
        this.cache.set(key, data);
      },
      
      getCachedData(key) {
        return this.cache.get(key);
      },
      
      cleanup() {
        this.cache.clear();
        console.log('MockDataService cleaned up');
      }
    };
  }
};

/**
 * Set up a complete test environment with mock singletons
 */
export function setupTestEnvironment() {
  resetFrontendSingletons();
  
  // Set up mock singletons
  window.workflowManager = MockSingletons.createMockWorkflowManager();
  window.consolidatedErrorManager = MockSingletons.createMockErrorManager();
  window.dataService = MockSingletons.createMockDataService();
  
  console.log('Test environment setup complete with mock singletons');
}

/**
 * Tear down test environment
 */
export function teardownTestEnvironment() {
  resetFrontendSingletons();
  console.log('Test environment teardown complete');
}

/**
 * Utility to check if all singletons are properly reset
 */
export function verifySingletonsReset() {
  const singletonNames = [
    'baseService',
    'workflowManager', 
    'consolidatedErrorManager',
    'dataService',
    'costManager',
    'roomManager'
  ];
  
  const unresetSingletons = singletonNames.filter(name => window[name] !== null && window[name] !== undefined);
  
  if (unresetSingletons.length > 0) {
    console.warn('The following singletons were not properly reset:', unresetSingletons);
    return false;
  }
  
  console.log('All singletons properly reset');
  return true;
}