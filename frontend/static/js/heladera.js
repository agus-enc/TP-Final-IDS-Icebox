document.addEventListener("DOMContentLoaded", () => {
    const puerta = document.getElementById("puerta");
    const zonaGuardar = document.getElementById("zona-guardar");
    if (!puerta || !zonaGuardar) return;

    // URL de la API
    let urlDeMiHeladera = puerta.getAttribute("data-backend") || "http://127.0.0.1:5000/endpoints";
    if (urlDeMiHeladera === "http://127.0.0.1:5000") {
        urlDeMiHeladera = "http://127.0.0.1:5000/endpoints";
    }
    
    let usuarioId = puerta.getAttribute("data-usuario");

    let imanSeleccionado = null;
    let offsetX = 0;
    let offsetY = 0;
    let arrastrando = false; 

    puerta.addEventListener("mousedown", (e) => {
        const iman = e.target.closest(".iman-viaje");
        if (!iman) return;

        e.preventDefault();
        imanSeleccionado = iman;
        arrastrando = false;
        
        const rect = imanSeleccionado.getBoundingClientRect();
        offsetX = e.clientX - rect.left;
        offsetY = e.clientY - rect.top;
        
        document.addEventListener("mousemove", mover);
        document.addEventListener("mouseup", soltar);
    });

    // REDIRECCIÓN REPARADA: Usa el Identificador único numérico (id_ciudad)
    puerta.addEventListener("click", (e) => {
        const iman = e.target.closest(".iman-viaje");
        if (!iman) return;

        if (arrastrando) {
            e.preventDefault();
            return; 
        }

        const idViaje = iman.getAttribute("data-viaje");
        const idCiudad = iman.getAttribute("data-id-ciudad");
        
        if (idViaje && idCiudad) {
            window.location.href = `/viajes/${idViaje}/editar?buscar_id_ciudad=${idCiudad}`;
        }
    });

    function mover(ev) {
        if (!imanSeleccionado) return;
        arrastrando = true;
        
        const rectPuerta = puerta.getBoundingClientRect();
        let x = ev.clientX - rectPuerta.left - offsetX;
        let y = ev.clientY - rectPuerta.top - offsetY;
        
        if (x < 0) x = 0;
        if (y < 0) y = 0;
        if (y > rectPuerta.height - imanSeleccionado.offsetHeight) {
            y = rectPuerta.height - imanSeleccionado.offsetHeight;
        }
        
        const limDerecho = rectPuerta.width - imanSeleccionado.offsetWidth;
        if (x > limDerecho + 100) { 
            x = limDerecho + 100;
        }

        imanSeleccionado.style.left = `${x}px`;
        imanSeleccionado.style.top = `${y}px`;
        imanSeleccionado.style.zIndex = "1000";

        const rectGaveta = zonaGuardar.getBoundingClientRect();
        const rectIman = imanSeleccionado.getBoundingClientRect();

        if (
            rectIman.right > rectGaveta.left &&
            rectIman.left < rectGaveta.right &&
            rectIman.bottom > rectGaveta.top &&
            rectIman.top < rectGaveta.bottom
        ) {
            zonaGuardar.classList.add("active");
        } else {
            zonaGuardar.classList.remove("active");
        }
    }

    function soltar() {
        if (!imanSeleccionado) return;
        
        document.removeEventListener("mousemove", mover);
        document.removeEventListener("mouseup", soltar);
        
        if (!arrastrando) {
            imanSeleccionado = null;
            return;
        }

        const idIman = imanSeleccionado.getAttribute("data-id");
        const rectGaveta = zonaGuardar.getBoundingClientRect();
        const rectIman = imanSeleccionado.getBoundingClientRect();

        if (
            rectIman.right > rectGaveta.left &&
            rectIman.left < rectGaveta.right &&
            rectIman.bottom > rectGaveta.top &&
            rectIman.top < rectGaveta.bottom
        ) {
            imanSeleccionado.style.display = "none";
            actualizarEstadoUbicacionBackend(idIman, false, 0, 0); 
        } else {
            const xFinal = parseInt(imanSeleccionado.style.left) || 0;
            const yFinal = parseInt(imanSeleccionado.style.top) || 0;
            
            const rectPuerta = puerta.getBoundingClientRect();
            const limDerecho = rectPuerta.width - imanSeleccionado.offsetWidth;
            
            if (xFinal > limDerecho) {
                imanSeleccionado.style.left = `${limDerecho}px`;
                actualizarEstadoUbicacionBackend(idIman, true, limDerecho, yFinal);
            } else {
                actualizarEstadoUbicacionBackend(idIman, true, xFinal, yFinal);
            }
        }

        imanSeleccionado.style.zIndex = "10"; 
        zonaGuardar.classList.remove("active");
        imanSeleccionado = null;
    }

    function actualizarEstadoUbicacionBackend(idIman, enHeladera, posX, posY) {
        fetch(`${urlDeMiHeladera}/imanes/${idIman}/posicion`, {
            method: "PATCH",
            headers: { 
                "Content-Type": "application/json",
                "X-User-Id": String(usuarioId)
            },
            body: JSON.stringify({
                ubicacion_heladera: enHeladera ? 1 : 0, 
                posicion_x: parseInt(posX),
                posicion_y: parseInt(posY)
            })
        })
        .then(res => console.log("Cambio impactado en Back:", res.status))
        .catch(err => console.log("Error de conexión:", err));
    }
});