// URL base del backend de tus compañeros (Puerto 5000)
const BACKEND_API_URL = 'http://127.0.0.1:5000';

document.addEventListener('DOMContentLoaded', () => {
    const imanes = document.querySelectorAll('.iman');
    const heladera = document.getElementById('contenedor-heladera');

    // --- POSICIONAR IMANES DESDE LOS ATRIBUTOS DATA ---
    imanes.forEach(iman => {
        const xInicial = iman.getAttribute('data-x');
        const yInicial = iman.getAttribute('data-y');
        
        iman.style.left = `${xInicial}px`;
        iman.style.top = `${yInicial}px`;
    });
    // ----------------------------------------------------------------------------------

    // Configurar el evento de arrastre para cada imán
    imanes.forEach(iman => {
        iman.addEventListener('mousedown', iniciarArrastre);
    });

    function iniciarArrastre(e) {
        const iman = e.currentTarget;
        
        // Calculamos el desfase inicial del clic dentro del imán
        let offsetX = e.clientX - iman.getBoundingClientRect().left;
        let offsetY = e.clientY - iman.getBoundingClientRect().top;

        function moverMouse(e) {
            const contenedorRect = heladera.getBoundingClientRect();
            
            // Calculamos la posición X e Y relativa a la heladera
            let nuevaX = e.clientX - contenedorRect.left - offsetX;
            let nuevaY = e.clientY - contenedorRect.top - offsetY;

            // Límites para que el imán no se escape de la heladera (o del tablero completo)
            const limiteMaxX = contenedorRect.width - iman.offsetWidth;
            const limiteMaxY = contenedorRect.height - iman.offsetHeight;

            if (nuevaX < 0) nuevaX = 0;
            if (nuevaY < 0) nuevaY = 0;
            if (nuevaX > limiteMaxX) nuevaX = limiteMaxX;
            if (nuevaY > limiteMaxY) nuevaY = limiteMaxY;

            // Aplicamos los estilos en tiempo real mientras arrastramos
            iman.style.left = `${nuevaX}px`;
            iman.style.top = `${nuevaY}px`;
        }

        function soltarMouse() {
            document.removeEventListener('mousemove', moverMouse);
            document.removeEventListener('mouseup', soltarMouse);

            // Obtenemos el ID del imán (viaje) desde el atributo HTML data-id
            const idIman = iman.getAttribute('data-id');
            
            // Leemos la posición final entera (sin 'px')
            const xFinal = parseInt(iman.style.left, 10);
            const yFinal = parseInt(iman.style.top, 10);

            // 💡 LÓGICA TEMPORAL PARA EL CAJÓN:
            // Por ahora, asumimos que si se está moviendo acá adentro está en la heladera (true).
            // Cuando armemos el contenedor del cajón, acá calcularemos si cayó fuera o dentro.
            const estaEnHeladera = true;

            // Disparamos la sincronización con el Backend oficial
            guardarPosicionEnBackend(idIman, xFinal, yFinal, estaEnHeladera);
        }

        document.addEventListener('mousemove', moverMouse);
        document.addEventListener('mouseup', soltarMouse);
    }
});

// FUNCIÓN DE RED: Conexión optimizada con el backend oficial de tus compañeros
function guardarPosicionEnBackend(idIman, x, y, estaEnHeladera) {
    const urlDestino = `${BACKEND_API_URL}/endpoints/imanes/${idIman}/posicion`;

    console.log(`[Fetch] Enviando a API oficial... (Imán ID: ${idIman}, Heladera: ${estaEnHeladera})`);

    fetch(urlDestino, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            posicion_x: x,
            posicion_y: y,
            ubicacion_heladera: estaEnHeladera // <-- Agregado para cumplir la validación del backend
        })
    })
    .then(response => {
        // El backend oficial devuelve status 204 (No Content) cuando todo sale bien
        if (response.status === 204) {
            console.log(`✅ [Base de Datos] ¡Posición del imán ${idIman} guardada con éxito (204)!`);
            return;
        }
        if (!response.ok) {
            throw new Error(`Error en el servidor de Flask. Status: ${response.status}`);
        }
    })
    .catch(error => {
        console.error('❌ [Error de Red] Revisa la conexión con el puerto 5000:', error);
    });
}