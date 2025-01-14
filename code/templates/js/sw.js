const CACHE_NAME = 'SIGUEEC-V1';
const hardCodedurlsToCache = [
  '/bienvenida',
  '/sw.js',
  '/serviceWorkerHandler.js',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js',
  '//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js',
  '{{url_for("static", filename="manifest.webmanifest")}}',
  '{{url_for("static", filename="img/iconBig.png")}}',
  '{{url_for("static", filename="img/iconSmall.png")}}',
  '{{url_for("static", filename="js/addEvaluationEC1.js")}}',
  '{{url_for("static", filename="js/addEvaluationEC2.js")}}',
  '{{url_for("static", filename="js/addEvaluationStudent.js")}}',
  '{{url_for("static", filename="js/addStudent.js")}}',
  '{{url_for("static", filename="js/downloadForm.js")}}',
  '{{url_for("static", filename="js/jsonLoader.js")}}',
  '{{url_for("static", filename="js/populateFormFields.js")}}',
  
  '{{url_for("static", filename="css/button.css")}}',
  '{{url_for("static", filename="css/capta.css")}}',
  '{{url_for("static", filename="css/cartas.css")}}',
  '{{url_for("static", filename="css/dropZone.css")}}',
  '{{url_for("static", filename="css/error.css")}}',
  '{{url_for("static", filename="css/index.css")}}',
  '{{url_for("static", filename="css/nav.css")}}',
  '{{url_for("static", filename="css/success.css")}}',
  '{{url_for("static", filename="css/verticalText.css")}}',
  {{urls_to_cache}}
];

if (typeof urlsToCache !== 'undefined') {
    urlsToCache.push(...hardCodedurlsToCache);
} else {
    var urlsToCache = hardCodedurlsToCache;
}


// Instalar el Service Worker y cachear los recursos
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Archivos cacheados');
        return cache.addAll(urlsToCache);
      })
  );
});

// Interceptar las solicitudes de red
// Estrategia Network First
self.addEventListener('fetch', (event) => {
  event.respondWith(
      fetch(event.request)
          .then((response) => {
              // Si la respuesta es válida, actualiza el cache.
              return caches.open(CACHE_NAME).then((cache) => {
                  cache.put(event.request, response.clone());
                  return response;
              });
          })
          .catch(() => {
              // Si la red falla, usa el cache.
              return caches.match(event.request);
          })
  );
});

// Actualizar el caché cuando cambien los archivos
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});