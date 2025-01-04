const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('file-info');

// Manejar el evento de clic en la zona de drop
dropZone.addEventListener('click', () => fileInput.click());

// Prevenir el comportamiento por defecto del navegador
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Manejar el evento de soltar archivo
dropZone.addEventListener('drop', handleDrop, false);

// Manejar el evento de seleccionar archivo
fileInput.addEventListener('change', handleFileSelect, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

function handleFileSelect(e) {
    const files = e.target.files;
    handleFiles(files);
}

function handleFiles(files) {
    if (files.length > 0) {
        const file = files[0];
        if (file.type === "application/json") {
            readJSONFile(file);
        } else {
            alert("El archivo que subiste no es un archivo válido de la CONAFE. Por favor, asegúrate de que tu archivo tenga un nombre similar a 'Formulario.json'.");
        }
    }
}

function readJSONFile(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const json = JSON.parse(e.target.result);
            const {url, ...formData} = json;

            let redirectUrl = url + '?';

            for (const field in formData) {
                redirectUrl += `${field}=${formData[field]}&`;
            }

            window.location.replace(redirectUrl);
            //fileInfo.innerHTML = `<div class="alert alert-success">Archivo JSON "${file.name}" cargado correctamente.</div>`;
        } catch (error) {
            console.error("Error al parsear el JSON:", error);
            fileInfo.innerHTML = `<div class="alert alert-danger">Error al leer el archivo proporcionado: ${error.message}</div>`;
        }
    };
    reader.readAsText(file);
}