// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\managers\event-manager.js

class EventManager {
    constructor() {
        if (EventManager.instance) {
            return EventManager.instance;
        }

        this.listeners = new Map(); // Stores event names as keys and arrays of listener functions as values

        EventManager.instance = this;
    }

    /**
     * Returns the singleton instance of EventManager.
     * @returns {EventManager} The singleton instance.
     */
    static getInstance() {
        if (!EventManager.instance) {
            EventManager.instance = new EventManager();
        }
        return EventManager.instance;
    }

    /**
     * Subscribes a listener function to a specific event.
     * @param {string} eventName - The name of the event to subscribe to.
     * @param {function} listener - The function to call when the event is published.
     */
    subscribe(eventName, listener) {
        if (!this.listeners.has(eventName)) {
            this.listeners.set(eventName, []);
        }
        this.listeners.get(eventName).push(listener);
        console.log(`Subscribed to event: ${eventName}`);
    }

    /**
     * Unsubscribes a listener function from a specific event.
     * @param {string} eventName - The name of the event to unsubscribe from.
     * @param {function} listener - The function to remove.
     */
    unsubscribe(eventName, listener) {
        if (!this.listeners.has(eventName)) {
            return;
        }
        const currentListeners = this.listeners.get(eventName);
        const index = currentListeners.indexOf(listener);
        if (index > -1) {
            currentListeners.splice(index, 1);
            console.log(`Unsubscribed from event: ${eventName}`);
        }
    }

    /**
     * Publishes an event, calling all subscribed listener functions.
     * @param {string} eventName - The name of the event to publish.
     * @param {any} [data] - Optional data to pass to the listeners.
     */
    publish(eventName, data) {
        if (!this.listeners.has(eventName)) {
            return;
        }
        console.log(`Publishing event: ${eventName}`, data);
        this.listeners.get(eventName).forEach(listener => {
            try {
                listener(data);
            } catch (error) {
                console.error(`Error in event listener for ${eventName}:`, error);
                // Potentially integrate with a global error logging system here
            }
        });
    }

    /**
     * Clears all listeners for a specific event, or all listeners for all events.
     * @param {string} [eventName] - The name of the event to clear listeners for. If not provided, clears all.
     */
    clearListeners(eventName) {
        if (eventName) {
            this.listeners.delete(eventName);
            console.log(`Cleared all listeners for event: ${eventName}`);
        } else {
            this.listeners.clear();
            console.log('Cleared all event listeners.');
        }
    }
}

export default EventManager;
