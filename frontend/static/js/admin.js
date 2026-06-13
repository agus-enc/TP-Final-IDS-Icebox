document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('miGrafico');
    
    if (canvas) {
        const ctx = canvas.getContext('2d');
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labelsCiudades, // Variables recibidas del Backend
                datasets: [{
                    label: 'Cantidad de Visitas', 
                    data: dataVisitas, // Variables recibidas del Backend
                    backgroundColor: '#7485e6', // El mismo lila de tu PDF
                    borderColor: '#333333', // Borde oscuro
                    borderWidth: 2,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false 
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1 // Los saltos de los números en el eje Y
                        }
                    }
                }
            }
        });
    }

    // --- LÓGICA NUEVA: TEXTO DE RESUMEN DE IMANES ---
    
    // 1. Calculamos el total de imanes sumando el array
    const totalImanes = dataImanes.reduce((a, b) => a + b, 0);
    
    // 2. Buscamos cuántos están en la heladera (el label que sea 1 o true)
    let cantHeladera = 0;
    const indexHeladera = labelsImanes.findIndex(label => label == 1 || label === true || label === 'true');
    if (indexHeladera !== -1) {
        cantHeladera = dataImanes[indexHeladera];
    }

    // 3. Escribimos la oración en el HTML (acordate de tener el <p id="resumen-imanes"></p> en tu HTML)
    const textoResumen = document.getElementById('resumen-imanes');
    if (textoResumen) {
        textoResumen.innerHTML = `Hay un TOTAL de <strong>${totalImanes} imanes</strong> en el sistema.<br>Actualmente, <strong>${cantHeladera} figuran en la heladera</strong>.`;
    }

    // 4. Transformamos los 0 y 1 de la BD a texto legible para la leyenda
    const etiquetasLegibles = labelsImanes.map(label => {
        return (label == 1 || label === true || label === 'true') ? 'En Heladera' : 'En Cajón';
    });

    const ctxImanes = document.getElementById('graficoImanes');
    if (ctxImanes) {
        new Chart(ctxImanes.getContext('2d'), {
            type: 'pie',
            data: {
                labels: labelsImanes,
                datasets: [{
                    data: dataImanes,
                    backgroundColor: ['#7485e6', '#a3b1ff'], 
                    borderColor: '#333333',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

});