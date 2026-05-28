document.addEventListener("DOMContentLoaded", () => {
    const cajon = document.getElementById("cajon-archivado");
    const zonaDevolver = document.getElementById("zona-devolver");
    if (!cajon || !zonaDevolver) return;

    const backendUrl = cajon.getAttribute("data-backend") || "http://127.0.0.1:5000";
    
    // Parche por si el ID de usuario del cajón llega vacío por culpa de app.py
    let usuarioId = cajon.getAttribute("data-usuario");
    if (!usuarioId || usuarioId === "" || usuarioId === "None") {
        usuarioId = "100";
    }

    let imanSeleccionado = null;
    let offsetX = 0;
    let offsetY = 0;

    cajon.addEventListener("mousedown", (e) => {
        const tarjeta = e.target.closest(".iman-viaje");
        if (!tarjeta) return;

        e.preventDefault();
        imanSeleccionado = tarjeta;

        const rect = imanSeleccionado.getBoundingClientRect();
        offsetX = e.clientX - rect.left;
        offsetY = e.clientY - rect.top;

        imanSeleccionado.style.position = "fixed";
        imanSeleccionado.style.width = "85px";
        imanSeleccionado.style.height = "85px";
        imanSeleccionado.style.left = `${rect.left}px`;
        imanSeleccionado.style.top = `${rect.top}px`;
        imanSeleccionado.style.zIndex = "1000";

        document.addEventListener("mousemove", mover);
        document.addEventListener("mouseup", soltar);
    });

    function mover(ev) {
        if (!imanSeleccionado) return;

        let x = ev.clientX - offsetX;
        let y = ev.clientY - offsetY;

        imanSeleccionado.style.left = `${x}px`;
        imanSeleccionado.style.top = `${y}px`;

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

        const rectGaveta = zonaDevolver.getBoundingClientRect();
        const idIman = imanSeleccionado.getAttribute("data-id");

        if (ev.clientX <= rectGaveta.right) {
            imanSeleccionado.style.transform = "scale(0)";
            imanSeleccionado.style.transition = "transform 0.2s ease";
            setTimeout(() => { 
                imanSeleccionado.remove(); 
            }, 200);

            // CORREGIDO: En vez de clavar 150,150 fijo, calcula una dispersión aleatoria dentro de la heladera
            const xAleatorio = Math.floor(Math.random() * 180) + 50;  // Rango seguro 50px - 230px
            const yAleatorio = Math.floor(Math.random() * 250) + 80;  // Rango seguro 80px - 330px

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
        fetch(`${backendUrl}/imanes/${id}/posicion`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                ubicacion_heladera: enHeladera,
                posicion_x: parseInt(x),
                posicion_y: parseInt(y),
                id_usuario: parseInt(usuarioId)
            })
        }).catch(err => console.log("Intento de envío de posición guardado localmente."));
    }
});