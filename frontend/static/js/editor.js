document.addEventListener('DOMContentLoaded', function() {

    // Creacion dinamica de paradas
    const botonAgregar = document.querySelector('.btn-principal');
    const lineaTiempo = document.querySelector('.linea-tiempo');
    let contadorParadas = 1;

    // LocalStorage
    // SECCIÓN A: LA FUNCIÓN FABRICANTE
    // Crea una función que tome un textarea específico y le enseñe a autoguardarse
    function protegerConAutoguardado(elementoTextarea) {

        // 1. Escucha el evento 'input' en este textarea
        elementoTextarea.addEventListener('input', function() {
            // 2. Extrae el texto que el usuario acaba de escribir (su .value)
            const texto = elementoTextarea.value;
            const llaveUnica = elementoTextarea.id;
            // 3. Usa localStorage.setItem(...) para guardarlo.
            localStorage.setItem(llaveUnica, texto)
        });
    }

    // SECCIÓN B: RECUPERAR AL CARGAR LA PÁGINA
    // 1. Usa document.querySelectorAll para buscar TODOS los textareas que existan en la pantalla
    const textosParadas = document.querySelectorAll('.textarea-elegante');
    // 2. Recórrelos usando un bucle (forEach o for...of)
    for (const texto of textosParadas){
        const borradorGuardado = localStorage.getItem(texto.id);
        if (borradorGuardado) {
            texto.value = borradorGuardado;
        }
        if (texto.id) {
            protegerConAutoguardado(texto);
        }
    }

    const botonesGuardarBase = document.querySelectorAll('.btn-guardar-parada')
    for (const btn of botonesGuardarBase) {
        btn.addEventListener('click', function() {
            const tarjetaPadre = this.closest('.tarjeta-parada');
            const textareaLocal = tarjetaPadre.querySelector('.textarea-elegante');
            if (textareaLocal && textareaLocal.id) {
                localStorage.removeItem(textareaLocal.id);
            }
        });
    }

    // SECCIÓN C: INTEGRACIÓN CON TU CLONADOR
    botonAgregar.addEventListener('click', function() {

        const tarjetaBase = document.querySelector('.tarjeta-parada');

        const nuevaTarjeta = tarjetaBase.cloneNode(true);

        const selectClonado = nuevaTarjeta.querySelector('.select-ciudad');
        if (selectClonado) selectClonado.selectedIndex = 0;

        const textareaClonado = nuevaTarjeta.querySelector('.textarea-elegante');
        if (textareaClonado) textareaClonado.value = "";

        const contenedorIman = nuevaTarjeta.querySelector('.contenedor-foto-iman');
        if (contenedorIman){
            contenedorIman.className = "contenedor-foto-iman vacio"
            contenedorIman.innerHTML = `
                <span class="icono-mas">+</span>
                <p>Subir Imán</p>
            `;
        }

        contadorParadas++;
        const labelIman = nuevaTarjeta.querySelector('label.contenedor-foto-iman');
        const inputIman = nuevaTarjeta.querySelector('input[type="file"]');

        if (textareaClonado) {
            textareaClonado.id = "texto-parada-" + contadorParadas;
            textareaClonado.name = "texto_parada_" + contadorParadas;
        }

        if (labelIman && inputIman) {
            labelIman.setAttribute('for', "foto-parada-" + contadorParadas);
            inputIman.id = "foto-parada-" + contadorParadas;
            inputIman.name = "foto_parada_" + contadorParadas;
        }

        if (selectClonado) {
            selectClonado.id = "ciudad-parada-" + contadorParadas;
            selectClonado.name = "ciudad_parada_" + contadorParadas;
        }

        const botonEliminarNuevo = nuevaTarjeta.querySelector('.btn-eliminar-parada');
        botonEliminarNuevo.addEventListener('click', function() {
            if (textareaClonado) {
                localStorage.removeItem(textareaClonado.id);
            }
            nuevaTarjeta.remove();
        });

        if (textareaClonado){
            protegerConAutoguardado(textareaClonado);
        }

        const botonGuardarNuevo = nuevaTarjeta.querySelector('.btn-guardar-parada');
        if (botonGuardarNuevo) {
            botonGuardarNuevo.addEventListener('click', function() {
                if (textareaClonado) {
                    localStorage.removeItem(textareaClonado.id);
                }
            });
        }

        lineaTiempo.appendChild(nuevaTarjeta)
    });

});