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

document.addEventListener('DOMContentLoaded', function() {

    // MOCKUP: LÓGICA DEL CREADOR DE VIAJES

    const btnNavCrear = document.getElementById('btn-nav-crear'); // Botón '+' del nav
    const modalCreador = document.getElementById('modal-creador-viajes');
    const btnCerrarCreador = document.getElementById('btn-cerrar-creador');
    const btnCrearParada = document.getElementById('btn-crear-parada-creador');
    const lineaTiempoCreador = document.getElementById('linea-tiempo-creador');
    const formCreador = document.getElementById('form-creador-viaje');

    let contadorParadasCreador = 1;

    if (btnNavCrear && modalCreador) {

        btnNavCrear.addEventListener('click', function(e) {
            e.preventDefault();
            modalCreador.classList.add('activo');
            document.body.style.overflow = 'hidden'; // Evita scrollear la página de fondo
        });

        function cerrarModal() {
            modalCreador.classList.remove('activo');
            document.body.style.overflow = 'auto'; // Devuelve el scroll al body
        }

        btnCerrarCreador.addEventListener('click', cerrarModal);
        modalCreador.addEventListener('click', function(e) {
            if (e.target === modalCreador) cerrarModal();
        });

        // 3. Clonar Paradas
        btnCrearParada.addEventListener('click', function() {
            contadorParadasCreador++;

            const molde = lineaTiempoCreador.querySelector('.tarjeta-parada-creador');
            const nuevaTarjeta = molde.cloneNode(true);

            // LIMPIEZA DEL CLON
            const inputCiudad = nuevaTarjeta.querySelector('.input-buscador-ciudad');
            if (inputCiudad) inputCiudad.value = '';

            const labelIman = nuevaTarjeta.querySelector('.contenedor-foto-iman');
            const inputIman = nuevaTarjeta.querySelector('input[type="file"]');

            if (labelIman && inputIman) {
                const nuevoId = `foto-parada-creador-${contadorParadasCreador}`;
                inputIman.id = nuevoId;
                labelIman.setAttribute('for', nuevoId);
                inputIman.value = ''; // Vaciamos la foto clonada
            }

            // Inyectamos el clon al final y bajamos la pantalla
            lineaTiempoCreador.appendChild(nuevaTarjeta);
            nuevaTarjeta.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        });

        // 3.5. Borrado con Delegación de Eventos
        lineaTiempoCreador.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn-eliminar-parada')) {
                const tarjeta = e.target.closest('.tarjeta-parada-creador');
                if (lineaTiempoCreador.querySelectorAll('.tarjeta-parada-creador').length > 1) {
                    tarjeta.remove();
                }
            }
        });

        // 4. Prevenir envío de formulario (Mockup)
        formCreador.addEventListener('submit', function(e) {
            e.preventDefault();
            const totalParadas = document.querySelectorAll('.tarjeta-parada-creador').length;
            alert(`¡Mockup UI Exitoso! 🚀\nEn el futuro, esto enviará al backend un viaje con ${totalParadas} paradas iniciales.`);
            cerrarModal();
        });
    }
});