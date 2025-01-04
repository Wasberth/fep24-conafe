document.addEventListener('DOMContentLoaded', function() {
const evaluationTableBody = document.getElementById('evaluationTableBody');
const addEvaluationBtn = document.getElementById('addEvaluationBtn');
let evaluationCount = 0;

evalTopics = [
    'claridad', 'comprension_lectora', 'comprension_contenidos', 'eficiencia',
    'trabajo_equipo', 'asistencia'
]

function addEvaluation() {
    evaluationCount++;
    topicCount = 0
    const newRow = document.createElement('tr');
    
    newRow.innerHTML = `
        <td>${evaluationCount}</td>
        <td>${typeof inputNombre === 'function'? inputNombre(evaluationCount): `<input type="text" name="nombre${evaluationCount}" class="form-control" required>`}</td>
        ${evalTopics.map((x)=>`<td><select class="form-select" name="${x}${evaluationCount}" required><option value="">Seleccionar</option><option value="D">Deficiente</option><option value="B">Bien</option><option value="MB">Muy Bien</option></select></td>`).join('')}
        <td><textarea name="observaciones${evaluationCount}" class="form-control" rows="2"></textarea></td>
        <td><button type="button" class="btn btn-danger btn-sm remove-evaluation">Eliminar</button></td>
    `;
    evaluationTableBody.appendChild(newRow);

    newRow.querySelector('.remove-evaluation').addEventListener('click', function() {
        if (evaluationTableBody.children.length > 1) {
            newRow.remove();
            updateEvaluationNumbers();
        }
    });
}

function updateEvaluationNumbers() {
    evaluationCount = 0;
    evaluationTableBody.querySelectorAll('tr').forEach((row, index) => {
        evaluationCount = index + 1;
        row.cells[0].textContent = evaluationCount;

            // Actualiza los atributos name de cada input, select y textarea en la fila
        row.querySelectorAll('input, select, textarea').forEach((field) => {
            if (field.name) {
                // Extrae el nombre base eliminando el número previo al final
                const baseName = field.name.replace(/\d+$/, '');
                // Actualiza el atributo name con el nuevo número
                field.name = `${baseName}${evaluationCount}`;
            }
        });
    });
}

addEvaluationBtn.addEventListener('click', addEvaluation);

prepareForm = function() {
    // Agregar 3 evaluaciones iniciales
    url = window.location.href;

    if (!url.includes('?')) {
        cant = typeof lenOptions !== 'undefined'? lenOptions: 3;
        for (let i = 0; i < cant; i++) {
            addEvaluation();

            if (typeof selName !== 'undefined') {
                console.log(`${selName}${i+1}`)
                document.getElementById(`${selName}${i+1}`).selectedIndex=i;
            }
        }
        return;
    }

    i = 1
    nam = typeof selName !== 'undefined'? selName: 'nombre';
    console.log(nam)
    while (url.includes(`${nam}${i}`)) {
        addEvaluation();
        i++;
    }
}

// Establecer la fecha actual por defecto
document.getElementById('fecha').valueAsDate = new Date();
});