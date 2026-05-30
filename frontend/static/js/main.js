// URL base para conectar con el servidor del backend (Puerto 5000)
const BACKEND_URL = "http://127.0.0.1:5000";

document.addEventListener('DOMContentLoaded', () => {
   
    // 1. Hacer desaparecer los carteles de alerta de Flask a los 3 segundos
    const alerts = document.querySelectorAll('.flash-message');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 3000);
    });

    // 2. LÓGICA DE DETECCIÓN DE RUTA DE FLASK
    const list = document.querySelectorAll('.router ul .list');
    const currentUrl = window.location.pathname;

    list.forEach((item) => {
        // Limpiamos cualquier clase active previa
        item.classList.remove('active');

        // Sacamos la dirección a la que apunta el botón
        const link = item.querySelector('a').getAttribute('href');
       
        // Comparamos si la URL actual coincide con el botón o si estamos en la raíz (home)
        if (currentUrl.includes(link) || (currentUrl === '/' && link.includes('heladera'))) {
            item.classList.add('active');
        }
    });
});

// Lógica para el menú desplegable del usuario
document.addEventListener('DOMContentLoaded', function() {
    const userMenuTrigger = document.getElementById('user-menu-trigger');
    const userDropdown = document.getElementById('user-dropdown');

    if (userMenuTrigger && userDropdown) {
        // Al hacer clic en el botón de usuario, muestra u oculta
        userMenuTrigger.addEventListener('click', function(event) {
            event.preventDefault(); // Frena el '#' para que no salte la pantalla
            event.stopPropagation(); // Evita que el evento "explote" hacia el window
            userDropdown.classList.toggle('show');
        });

        // Si hacen clic en cualquier otro lado de la pantalla, se cierra solo
        window.addEventListener('click', function(event) {
            if (!userMenuTrigger.contains(event.target)) {
                userDropdown.classList.remove('show');
            }
        });
    }
});