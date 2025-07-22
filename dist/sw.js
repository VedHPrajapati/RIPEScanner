
// RIPEScanner Service Worker
const CACHE_NAME = 'ripescanner-v1.0.0';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    'https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css',
    'https://unpkg.com/feather-icons'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            }
        )
    );
});
