document.addEventListener('DOMContentLoaded', function() {
    const evaluationTableBody = document.getElementById('evaluationTableBody');
    const addEvaluationBtn = document.getElementById('addEvaluationBtn');
    let evaluationCount = 0;
    
    function addEvaluation() {
        evaluationCount++;
        topicCount = 0
        const newRow = document.createElement('tr');
        
        newRow.innerHTML = `        
            <td>${evaluationCount}</td>
            <td><input type="text" name="apellido1_${evaluationCount}" class="form-control" placeholder="Apellido Materno" required></td>
            <td><input type="text" name="apellido2_${evaluationCount}" class="form-control" placeholder="Apellido Paterno" required></td>
            <td><input type="text" name="nombre${evaluationCount}" class="form-control" placeholder="Nombre (s)" required></td>
            <td><input type="date" name="fecha_nacimiento${evaluationCount} class="form-control" required></td>
            <td><input type="text" name="curp${evaluationCount}" class="form-control" placeholder="CURP" required></td>
            <td><select name="sexo${evaluationCount}" class="form-control" placeholder="Sexo"><option value="M">Masculino</option><option value="F">Femenino</option></select></td>
            <td><select name="acta_nacimiento${evaluationCount}" class="form-control" placeholder="Acta de nacimiento"><option value="true">Sí</option><option value="false">No</option></select></td>
            <td><select name="fotos${evaluationCount}" class="form-control" placeholder="Fotos"><option value="true">Sí</option><option value="false">No</option></select></td>
            <td>
                <div class="form-check">
                    <input name="acta_testimonial" class="form-check-input" type="checkbox" value="" id="acta_check_${evaluationCount}">
                    <label class="form-check-label" for="acta_check_${evaluationCount}">
                        Acta testimonial
                    </label>
                </div>
                <div class="form-check">
                    <input name="cartilla_vacunación" class="form-check-input" type="checkbox" value="" id="vacuna_check_${evaluationCount}">
                    <label class="form-check-label" for="vacuna_check_${evaluationCount}">
                        Cartilla de vacunación
                    </label>
                </div>
                <div class="form-check">
                    <input name="fe_bautizo" class="form-check-input" type="checkbox" value="" id="bautizo_check_${evaluationCount}">
                    <label class="form-check-label" for="bautizo_check_${evaluationCount}">
                        Fe de bautizo
                    </label>
                </div>
            </td>
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
    addEvaluation();
    
    // Establecer la fecha actual por defecto
    document.getElementById('fecha').valueAsDate = new Date();
    });