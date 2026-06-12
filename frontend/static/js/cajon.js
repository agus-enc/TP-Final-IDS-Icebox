document.addEventListener("DOMContentLoaded", () => {
    const cajon = document.getElementById("cajon-archivado");
    const zonaDevolver = document.getElementById("zona-devolver");
    if (!cajon || !zonaDevolver) return;

    // URL de la API
    let urlDeMiCajon = cajon.getAttribute("data-backend");

    if (urlDeMiCajon && urlDeMiCajon.includes("//backend:")) {
        urlDeMiCajon = `${window.location.protocol}//${window.location.hostname.split(':')[0]}:5000/endpoints`;
    }

    let usuarioId = cajon.getAttribute("data-usuario");

    let imanSeleccionado = null;
    let offsetX = 0;
    let offsetY = 0;
    let arrastrando = false; 

    cajon.addEventListener("mousedown", (e) => {
        const tarjeta = e.target.closest(".iman-viaje");
        if (!tarjeta) return;

        e.preventDefault();
        imanSeleccionado = tarjeta;
        arrastrando = false; 

        const rect = imanSeleccionado.getBoundingClientRect();
        offsetX = e.clientX - rect.left;
        offsetY = e.clientY - rect.top;

        document.addEventListener("mousemove", mover);
        document.addEventListener("mouseup", soltar);
    });

    cajon.addEventListener("click", (e) => {
        const tarjeta = e.target.closest(".iman-viaje");
        if (!tarjeta) return;

        if (!arrastrando) {
            const idViaje = tarjeta.getAttribute("data-viaje");
            const idParada = tarjeta.getAttribute("data-parada");

            if (idViaje && idParada) {
                window.location.href = `/viajes/${idViaje}/editar?buscar_id_parada=${idParada}`;
            }
        }
    });

    function mover(ev) {
        if (!imanSeleccionado) return;
        arrastrando = true; 

        let x = ev.clientX - offsetX;
        let y = ev.clientY - offsetY;

        imanSeleccionado.style.position = "fixed";
        imanSeleccionado.style.width = "130px";
        imanSeleccionado.style.height = "130px";
        imanSeleccionado.style.left = `${x}px`;
        imanSeleccionado.style.top = `${y}px`;
        imanSeleccionado.style.zIndex = "1000";

        const rectGaveta = zonaDevolver.getBoundingClientRect();
        if (ev.clientX <= rectGaveta.right) {
            zonaDevolver.classList.add("active");
        } else {
            zonaDevolver.classList.remove("active");
        }
    }

    function soltar(ev) {
        if (!imanSeleccionado) return;
        
        document.removeEventListener("mousemove", mover);
        document.removeEventListener("mouseup", soltar);

        if (!arrastrando) {
            imanSeleccionado = null;
            return;
        }

        const rectGaveta = zonaDevolver.getBoundingClientRect();
        const idIman = imanSeleccionado.getAttribute("data-id");
        
        // 🌟 Guardamos la referencia fija del elemento para evitar el error de null
        const elementoAEliminar = imanSeleccionado; 

        if (ev.clientX <= rectGaveta.right) {
            elementoAEliminar.style.transform = "scale(0)";
            elementoAEliminar.style.transition = "transform 0.2s ease";
            
            setTimeout(() => { 
                elementoAEliminar.remove(); 
            }, 200);

            const xAleatorio = Math.floor(Math.random() * 180) + 50;  
            const yAleatorio = Math.floor(Math.random() * 250) + 80;  

            enviarCambioPosicion(idIman, true, xAleatorio, yAleatorio);
        } else {
            imanSeleccionado.style.position = "relative";
            imanSeleccionado.style.left = "auto";
            imanSeleccionado.style.top = "auto";
            imanSeleccionado.style.zIndex = "10";
        }

        zonaDevolver.classList.remove("active");
        imanSeleccionado = null;
    }

    function enviarCambioPosicion(id, enHeladera, x, y) {
        fetch(`${urlDeMiCajon}/imanes/${id}/posicion`, {
            method: "PATCH",
            headers: { 
                "Content-Type": "application/json",
                "X-User-Id": String(usuarioId)
            },
            body: JSON.stringify({
                ubicacion_heladera: enHeladera ? 1 : 0, 
                posicion_x: parseInt(x),
                posicion_y: parseInt(y)
            })
        })
        .then(res => {
            if (res.ok) {
                console.log(`¡Éxito! El imán ${id} ya está guardado en la heladera.`);
            } else {
                console.error("El backend recibió la orden pero devolvió un error:", res.status);
            }
        })
        .catch(err => console.log("Error de conexión Cajón:", err));
    }
});