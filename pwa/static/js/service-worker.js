// static/js/service-worker.js
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('static-cache').then(cache => {
            return cache.addAll([
                '/',
                '/offline',
                '/static/css/style.css',
                '/static/js/app.js',
                '/static/images/icon-192x192.png',
                '/static/images/icon-512x512.png',
                '/manifest.json'
            ]);
        })
    );
    console.log('Service Worker installed');
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        }).catch(() => {
            return caches.match('/offline');
        })
    );
});
