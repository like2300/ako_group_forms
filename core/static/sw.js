// sw.js
const CACHE_NAME = 'ako-app-v1';
const urlsToCache = [
  '/',
  '/static/manifest.json',
  // Ajoutez ici d'autres ressources statiques que vous souhaitez mettre en cache
  // Exemple:
  // '/static/css/style.css',
  // '/static/js/main.js',
  // '/static/images/logo.png'
];

// Installation du Service Worker
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Cache ouvert');
        return cache.addAll(urlsToCache);
      })
      .catch(function(error) {
        console.error('Erreur lors de la mise en cache:', error);
      })
  );
});

// Fetch events
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
      .catch(function(error) {
        console.error('Erreur lors de la récupération:', error);
      })
  );
});

// Activation
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});