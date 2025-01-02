document.addEventListener('DOMContentLoaded', function() {
const evaluationTableBody = document.getElementById('evaluationTableBody');
const addEvaluationBtn = document.getElementById('addEvaluationBtn');
let evaluationCount = 0;

evalTopics = [
    'lengua', 'español', 'matematicas', 'cencias_naturales', 'ciencias_sociales'
]

parciales = 4

function addEvaluation() {
    evaluationCount++;
    topicCount = 0
    const newRow = document.createElement('tr');
    
    newRow.innerHTML = `        
        <td>${evaluationCount}</td>
        <td><input type="text" name="nombre${evaluationCount}" class="form-control" placeholder="Nombre completo" required></td>
        ${[...Array(parciales + 2).keys()].map((i)=>(evalTopics.map((x)=>`<td><input type="number" name="${x}${i+1}_${evaluationCount}" class="form-control" min="0" max="10" required></td>`).join(''))).join('')}
        <td><input type="number" name="promedio${evaluationCount}" class="form-control" placeholder="Promedio"></td>
        <td><select name="examen${evaluationCount}" class="form-control" placeholder="Examen"><option value="true">Sí</option><option value="false">No</option></select></td>
        <td><select name="situacion${evaluationCount}" class="form-control" placeholder="Situación">
            <option disabled>Para primaria</option>
            <option value="A" selected>Promovido</option>
            <option value="B">Baja</option>
            <option value="C">Certifica</option>
            <option value="E">Caso especial</option>
            <option value="N">No promueve</option>
            <option value="P">Permanece en el nivel (Promovido a 2do año del nivel)</option>
            <option disabled>Para Preescolar</option>
            <option value="CE">Constancia</option>
            <option value="D">Diploma</option></select></td>
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

// Agregar 3 evaluaciones iniciales
for (let i = 0; i < 3; i++) {
    addEvaluation();
}

// Establecer la fecha actual por defecto
document.getElementById('fecha').valueAsDate = new Date();
});