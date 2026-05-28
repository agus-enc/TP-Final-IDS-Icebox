document.addEventListener("DOMContentLoaded", () => {
    const puerta = document.getElementById("puerta");
    const zonaGuardar = document.getElementById("zona-guardar");
    if (!puerta || !zonaGuardar) return;

    const backendUrl = puerta.getAttribute("data-backend") || "http://127.0.0.1:5000";
    
    let usuarioId = puerta.getAttribute("data-usuario");
    if (!usuarioId || usuarioId === "" || usuarioId === "None") {
        usuarioId = "100"; 
    }

    let imanSeleccionado = null;
    let offsetX = 0;
    let offsetY = 0;

    puerta.addEventListener("mousedown", (e) => {
        const iman = e.target.closest(".iman-viaje");
        if (!iman) return;

        e.preventDefault();
        imanSeleccionado = iman;
        
        const rect = imanSeleccionado.getBoundingClientRect();
        offsetX = e.clientX - rect.left;
        offsetY = e.clientY - rect.top;
        
        imanSeleccionado.style.zIndex = "1000";

        document.addEventListener("mousemove", mover);
        document.addEventListener("mouseup", soltar);
    });

    function mover(ev) {
        if (!imanSeleccionado) return;
        
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
            const xFinal = parseInt(imanSeleccionado.style.left);
            const yFinal = parseInt(imanSeleccionado.style.top);
            
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
        fetch(`${backendUrl}/imanes/${idIman}/posicion`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                ubicacion_heladera: enHeladera,
                posicion_x: posX,
                posicion_y: posY,
                id_usuario: parseInt(usuarioId)
            })
        }).catch(err => console.log("Fetch controlado. Servidor central offline."));
    }
});