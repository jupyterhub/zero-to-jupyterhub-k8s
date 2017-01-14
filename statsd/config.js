(function() {
    return {
        port: parseInt(process.env.STATSD_PORT) || 8125,
        backends: ["statsd-datadog-backend"],
        datadogApiKey: process.env.DATADOG_API_KEY,
        datadogPrefix: process.env.DATADOG_PREFIX
    };
})()
