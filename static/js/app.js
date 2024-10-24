// static/js/app.js
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/service-worker.js')
        .then(registration => {
            console.log('Service Worker registered with scope:', registration.scope);
        }, err => {
            console.error('Service Worker registration failed:', err);
        });
    });
}
