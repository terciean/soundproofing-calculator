// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\form-logging\form-logger.js

import LoggingService from '../services/logging-service.js';

class FormLogger extends LoggingService {
    constructor() {
        super('Form');
    }

    logFormEvent(eventName, data) {
        this.info(`Event: ${eventName}, Data: ${JSON.stringify(data)}`);
    }

    logFormSubmission(formData) {
        this.info(`Form Submission: ${JSON.stringify(formData)}`);
    }

    logFormError(errorMessage, errorDetails) {
        this.error(`Form Error: ${errorMessage}`, errorDetails);
    }
}

export default FormLogger;
