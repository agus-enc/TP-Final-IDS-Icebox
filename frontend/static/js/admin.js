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
                labels: etiquetasLegibles,
                datasets: [{
                    data: dataImanes,
                    backgroundColor: ['#7485e6', '#cbd5e1'], 
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

    // --- GRÁFICO 3: RESEÑAS POR CIUDAD (Dona) ---
    const ctxResenas = document.getElementById('graficoResenas');
    if (ctxResenas) {
        new Chart(ctxResenas.getContext('2d'), {
            type: 'doughnut', 
            data: {
                labels: labelsResenas, // Las ciudades que vienen del back
                datasets: [{
                    data: dataResenas, // Las cantidades de reseñas
                    // Gama de lilas, azules y grises en degradé
                    backgroundColor: ['#7485e6', '#a3b1ff', '#cbd5e1', '#94a3b8', '#e2e8f0'], 
                    borderColor: '#333333',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right', // Leyenda al costado para que no tape el gráfico
                        labels: {
                            color: '#333333',
                            font: {
                                size: 13,
                                weight: '600'
                            }
                        }
                    }
                }
            }
        });
    }

    const ctxUsuarios = document.getElementById('graficoUsuarios').getContext('2d');
    new Chart(ctxUsuarios, {
        type: 'bar', 
        data: {
            labels: labelsUsuarios, // Usa la constante global del HTML
            datasets: [{
                label: 'Cantidad de Viajes Creados',
                data: dataViajes,     // Usa la constante global del HTML
                backgroundColor: ['#7485e6','#a3b1ff','#94a3b8','#cbd5e1','#e2e8f0'],
                borderColor: '#333333',
                borderWidth: 1.5
            }]
        },
        options: {
            indexAxis: 'y', // Hace que las barras sean horizontales
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false 
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1, // Números enteros
                        color: '#333333'
                    }
                },
                y: {
                    ticks: {
                        color: '#333333'
                    }
                }
            }
        }
    });

});