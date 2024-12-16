document.getElementById('downloadBtn').addEventListener('click', function () {
    // Encuentra el formulario en la página
    const form = document.querySelector('#downloadableForm');
    if (!form) {
        alert('No se encontró ningún formulario en la página.');
        return;
    }

    // Crear un objeto para almacenar los datos del formulario
    const formData = {};

    // Iterar sobre los elementos del formulario
    const elements = form.elements;
    for (let element of elements) {
        console.log(element)
        if (element.name && !element.disabled) {
            if (element.type === 'checkbox' || element.type === 'radio') {
                // Guardar el valor de los checkboxes y radios seleccionados
                formData[element.name] = element.checked;
            } else {
                // Guardar los valores de otros tipos de input
                formData[element.name] = element.value;
            }
        }
    }

    // Convierte el objeto a JSON
    const jsonData = JSON.stringify(formData, null, 4);

    // Crea un archivo Blob con los datos
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    // Crea un enlace para descargar el archivo
    const a = document.createElement('a');
    a.href = url;
    a.download = 'formulario.json'; // Nombre del archivo descargado
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    // Libera la URL del objeto Blob
    URL.revokeObjectURL(url);
});
