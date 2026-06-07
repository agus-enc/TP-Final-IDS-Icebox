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
});