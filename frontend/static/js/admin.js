document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('miGrafico');
    
    if (canvas) {
        const ctx = canvas.getContext('2d');
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labelsCiudades, 
                datasets: [{
                    label: 'Cantidad de Visitas', 
                    data: dataVisitas,
                    backgroundColor: '#7485e6',
                    borderColor: '#333333',
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
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }

    const totalImanes = dataImanes.reduce((a, b) => a + b, 0);
    let cantHeladera = 0;
    const indexHeladera = labelsImanes.findIndex(label => label == 1 || label === true || label === 'true');
    if (indexHeladera !== -1) {
        cantHeladera = dataImanes[indexHeladera];
    }

    const textoResumen = document.getElementById('resumen-imanes');
    if (textoResumen) {
        textoResumen.innerHTML = `Hay un TOTAL de <strong>${totalImanes} imanes</strong> en el sistema.<br>Actualmente, <strong>${cantHeladera} figuran en la heladera</strong>.`;
    }

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

    const ctxResenas = document.getElementById('graficoResenas');
    if (ctxResenas) {
        new Chart(ctxResenas.getContext('2d'), {
            type: 'doughnut', 
            data: {
                labels: labelsResenas, 
                datasets: [{
                    data: dataResenas, 
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
                        position: 'right',
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
            labels: labelsUsuarios,
            datasets: [{
                label: 'Cantidad de Viajes Creados',
                data: dataViajes,
                backgroundColor: ['#7485e6','#a3b1ff','#94a3b8','#cbd5e1','#e2e8f0'],
                borderColor: '#333333',
                borderWidth: 1.5
            }]
        },
        options: {
            indexAxis: 'y', 
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
                        stepSize: 1, 
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