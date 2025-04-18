class Logger {
    constructor(name) {
        this.name = name;
    }

    info(message) {
        console.log(`[${this.name}] INFO: ${message}`);
    }

    warn(message) {
        console.warn(`[${this.name}] WARN: ${message}`);
    }

    error(message) {
        console.error(`[${this.name}] ERROR: ${message}`);
    }
}

module.exports = {
    Logger
};
