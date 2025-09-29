// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\services\logging-service.js

class LoggingService {
    constructor(context) {
        this.context = context || 'App';
    }

    log(message, level = 'info') {
        console.log(`[${this.context}] [${level.toUpperCase()}] ${message}`);
    }

    info(message) {
        this.log(message, 'info');
    }

    warn(message) {
        this.log(message, 'warn');
    }

    error(message, error) {
        console.error(`[${this.context}] [ERROR] ${message}`, error);
    }
}

export default LoggingService;
