document.addEventListener('DOMContentLoaded', function() {

    const botonAgregar = document.querySelector('.btn-principal');
    const lineaTiempo = document.querySelector('.linea-tiempo');
    let contadorParadas = 1;

    botonAgregar.addEventListener('click', function() {

        const tarjetaBase = document.querySelector('.tarjeta-parada');

        const nuevaTarjeta = tarjetaBase.cloneNode(true)

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
        if (textareaClonado) {
            textareaClonado.id = "texto-parada-" + contadorParadas;
            textareaClonado.name = "texto_parada_" + contadorParadas;
        }

        const labelIman = nuevaTarjeta.querySelector('label.contenedor-foto-iman');
        const inputIman = nuevaTarjeta.querySelector('input[type="file"]');

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
            nuevaTarjeta.remove();
        });

        lineaTiempo.appendChild(nuevaTarjeta)
    });

});