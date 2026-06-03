document.addEventListener("DOMContentLoaded", () => {
    const cajon = document.getElementById("cajon-archivado");
    const zonaDevolver = document.getElementById("zona-devolver");
    if (!cajon || !zonaDevolver) return;

    let urlDeMiCajon = cajon.getAttribute("data-backend") || "http://127.0.0.1:5000/endpoints";
    if (urlDeMiCajon === "http://127.0.0.1:5000") {
        urlDeMiCajon = "http://127.0.0.1:5000/endpoints";
    }
    
    let usuarioId = cajon.getAttribute("data-usuario");
    if (!usuarioId || usuarioId === "" || usuarioId === "None") {
        usuarioId = "1"; 
    }

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

    // REDIRECCIÓN REPARADA EN EL CAJÓN: Busca por ID numérico de ciudad
    cajon.addEventListener("click", (e) => {
        const tarjeta = e.target.closest(".iman-viaje");
        if (!tarjeta) return;

        if (arrastrando) {
            e.preventDefault();
            return; 
        }

        const idViaje = tarjeta.getAttribute("data-viaje");
        const idCiudad = tarjeta.getAttribute("data-id-ciudad");

        if (idViaje && idCiudad) {
            window.location.href = `/viajes/${idViaje}/editar?buscar_id_ciudad=${idCiudad}`;
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

        if (ev.clientX <= rectGaveta.right) {
            imanSeleccionado.style.transform = "scale(0)";
            imanSeleccionado.style.transition = "transform 0.2s ease";
            setTimeout(() => { 
                imanSeleccionado.remove(); 
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
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                ubicacion_heladera: enHeladera ? 1 : 0,
                posicion_x: parseInt(x),
                posicion_y: parseInt(y),
                id_usuario: parseInt(usuarioId)
            })
        })
        .then(res => console.log("Guardado en Back base:", res.status))
        .catch(err => console.log("Error de conexión:", err));
    }
});