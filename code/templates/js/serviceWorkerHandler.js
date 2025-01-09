window.addEventListener('load', function() {
    let displayMode = 'browser';
    const mqStandAlone = '(display-mode: standalone)';
    if (navigator.standalone || window.matchMedia(mqStandAlone).matches) {
        displayMode = 'standalone';
    }

    if (displayMode === 'standalone') {
        document.getElementById('login-menu').style.display = 'none';
        let onlineItems = document.getElementsByClassName('online');
        for (let i = 0; i < onlineItems.length; i++) {
            element = onlineItems[i];

            children = element.children
            for (let j = 0; j < children.length; j++) {
                child = children[j];

                if (child.tagName !== 'A') return;

                child.style.textDecoration = 'line-through';
                child.removeAttribute('href');
            }
        }
    }

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register("{{ url_for('service_worker') }}")
            .then(reg => console.log('Service Worker registrado:', reg))
            .catch(err => console.error('Error al registrar el Service Worker:', err));
    }
});

