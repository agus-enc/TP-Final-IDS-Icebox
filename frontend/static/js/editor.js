document.addEventListener('DOMContentLoaded', function() {

    // DATOS Y VARIABLES GLOBALES
    const botonAgregar = document.querySelector('.btn-principal');
    const lineaTiempo = document.querySelector('.linea-tiempo');
    let contadorParadas = document.querySelectorAll('.tarjeta-parada').length + 1;

    // MOCKUP DE DATOS (Simulando la base de datos temporalmente)
    const ciudadesMockup = [
        { id: 101, nombre: "Madrid, España" },
        { id: 102, nombre: "Barcelona, España" },
        { id: 205, nombre: "Roma, Italia" },
        { id: 206, nombre: "Milán, Italia" },
        { id: 310, nombre: "París, Francia" },
        { id: 415, nombre: "Londres, Reino Unido" },
        { id: 501, nombre: "Buenos Aires, Argentina" }
    ];

    let textareaActivo = null;
    const overlayTexto = document.getElementById('overlay-enfoque-texto');

    // FUNCIONES "FÁBRICA" (Definiciones)

    // Autoguardado
    function protegerConAutoguardado(elementoTextarea) {
        elementoTextarea.addEventListener('input', function() {
            const texto = elementoTextarea.value;
            const llaveUnica = elementoTextarea.id;
            localStorage.setItem(llaveUnica, texto);
        });
    }

    // Modo Zen para Textareas
    function habilitarModoZen(elementoTextarea) {
        elementoTextarea.addEventListener('focus', function() {
            textareaActivo = this;
            this.classList.add('modo-zen');
            if (overlayTexto) overlayTexto.classList.add('activo');
            document.body.style.overflow = 'hidden';
        });
    }

    function salirModoZen() {
        if (textareaActivo) {
            textareaActivo.classList.remove('modo-zen');
            textareaActivo.blur();
            textareaActivo = null;
        }
        if (overlayTexto) overlayTexto.classList.remove('activo');
        document.body.style.overflow = '';
    }

    // Buscador Autocompletable
    function inicializarBuscadorCiudad(wrapper) {
        const inputVisible = wrapper.querySelector('.input-buscador-ciudad');
        const inputOculto = wrapper.querySelector('input[type="hidden"]');
        const listaResultados = wrapper.querySelector('.lista-resultados-ciudad');

        if (!inputVisible || !inputOculto || !listaResultados) return;

        inputVisible.addEventListener('input', function() {
            const valorBuscado = this.value.toLowerCase().trim();
            listaResultados.innerHTML = '';

            if (valorBuscado.length === 0) {
                listaResultados.classList.remove('activa');
                inputOculto.value = '';
                return;
            }

            const coincidencias = ciudadesMockup.filter(ciudad =>
                ciudad.nombre.toLowerCase().includes(valorBuscado)
            );

            if (coincidencias.length > 0) {
                coincidencias.forEach(ciudad => {
                    const li = document.createElement('li');
                    li.textContent = ciudad.nombre;

                    li.addEventListener('click', function() {
                        inputVisible.value = ciudad.nombre;
                        inputOculto.value = ciudad.id;
                        listaResultados.classList.remove('activa');
                    });

                    listaResultados.appendChild(li);
                });
                listaResultados.classList.add('activa');
            } else {
                const li = document.createElement('li');
                li.textContent = "No se encontraron ciudades...";
                li.style.color = "#999";
                li.style.cursor = "default";
                listaResultados.appendChild(li);
                listaResultados.classList.add('activa');
            }
        });
    }

    // INICIALIZACIÓN DE LA BASE (On Load)

    // Iniciar Buscadores Base
    const wrappersBuscador = document.querySelectorAll('.buscador-ciudad-wrapper');
    for (const wrapper of wrappersBuscador) {
        inicializarBuscadorCiudad(wrapper);
    }

    // Iniciar Textareas Base (Recuperar memoria, autoguardar y Zen)
    const textosParadas = document.querySelectorAll('.textarea-elegante');
    for (const texto of textosParadas){
        const borradorGuardado = localStorage.getItem(texto.id);
        if (borradorGuardado) {
            texto.value = borradorGuardado;
        }
        if (texto.id) {
            protegerConAutoguardado(texto);
            habilitarModoZen(texto);
        }
    }

    // Iniciar Botones de Guardar Base (Limpiar memoria)
    const botonesGuardarBase = document.querySelectorAll('.btn-guardar-parada');
    for (const btn of botonesGuardarBase) {
        btn.addEventListener('click', function() {
            const tarjetaPadre = this.closest('.tarjeta-parada');
            const textareaLocal = tarjetaPadre.querySelector('.textarea-elegante');
            if (textareaLocal && textareaLocal.id) {
                localStorage.removeItem(textareaLocal.id);
            }
        });
    }

    // HEADER / PORTADA

    const inputPortada = document.getElementById('foto-portada');
    const headerPortada = document.getElementById('header-portada');
    const btnBorrarPortada = document.getElementById('btn-borrar-portada');

    if (inputPortada && headerPortada) {
        inputPortada.addEventListener('change', function(event) {
            const archivo = event.target.files[0];
            if (archivo) {
                const urlImagenTemporal = URL.createObjectURL(archivo);
                headerPortada.style.backgroundImage = `url('${urlImagenTemporal}')`;
            }
        });

        if (btnBorrarPortada) {
            btnBorrarPortada.addEventListener('click', function() {
                headerPortada.style.backgroundImage = 'none';
                inputPortada.value = "";
            });
        }
    }

    // LÍNEA DE TIEMPO (Clonación e Imanes)

    // Delegación de Eventos para Imanes
    if (lineaTiempo) {
        lineaTiempo.addEventListener('change', function(e) {
            if (e.target.matches('input[type="file"]')) {
                const archivo = e.target.files[0];
                if (archivo) {
                    const urlImagenTemporal = URL.createObjectURL(archivo);
                    const labelIman = e.target.previousElementSibling;

                    if (labelIman && labelIman.classList.contains('contenedor-foto-iman')) {
                        labelIman.style.backgroundImage = `url('${urlImagenTemporal}')`;
                        labelIman.classList.remove('vacio');
                        labelIman.innerHTML = '';
                    }
                }
            }
        });
    }

    // Clonador de paradas vacias
    botonAgregar.addEventListener('click', function() {
        const tarjetaBase = document.querySelector('.tarjeta-parada');
        const nuevaTarjeta = tarjetaBase.cloneNode(true);

        // Clonar Buscador
        const wrapperBuscadorClonado = nuevaTarjeta.querySelector('.buscador-ciudad-wrapper');
        const inputVisibleClonado = nuevaTarjeta.querySelector('.input-buscador-ciudad');
        const inputOcultoClonado = nuevaTarjeta.querySelector('input[type="hidden"]');
        const listaResultadosClonado = nuevaTarjeta.querySelector('.lista-resultados-ciudad');

        if (wrapperBuscadorClonado) {
            wrapperBuscadorClonado.id = "wrapper-ciudad-" + contadorParadas;
            inputVisibleClonado.id = "input-ciudad-" + contadorParadas;
            inputVisibleClonado.value = "";
            inputOcultoClonado.id = "hidden-ciudad-" + contadorParadas;
            inputOcultoClonado.name = "ciudad_parada_" + contadorParadas;
            inputOcultoClonado.value = "";
            listaResultadosClonado.id = "resultados-ciudad-" + contadorParadas;
            listaResultadosClonado.innerHTML = '';
            listaResultadosClonado.classList.remove('activa');
            inicializarBuscadorCiudad(wrapperBuscadorClonado);
        }

        // Clonar Textarea
        const textareaClonado = nuevaTarjeta.querySelector('.textarea-elegante');
        if (textareaClonado) {
            textareaClonado.value = "";
            textareaClonado.id = "texto-parada-" + contadorParadas;
            textareaClonado.name = "texto_parada_" + contadorParadas;
            protegerConAutoguardado(textareaClonado);
            habilitarModoZen(textareaClonado);
        }

        // Clonar Imán
        const contenedorIman = nuevaTarjeta.querySelector('.contenedor-foto-iman');
        const inputIman = nuevaTarjeta.querySelector('input[type="file"]');

        if (contenedorIman && inputIman){
            contenedorIman.className = "contenedor-foto-iman vacio";
            contenedorIman.style.backgroundImage = 'none';
            contenedorIman.innerHTML = `
                <span class="icono-mas">+</span>
                <p>Subir Imán</p>
            `;
            contenedorIman.setAttribute('for', "foto-parada-" + contadorParadas);
            inputIman.id = "foto-parada-" + contadorParadas;
            inputIman.name = "foto_parada_" + contadorParadas;
        }

        // Clonar Botones (Guardar y Eliminar)
        const botonEliminarNuevo = nuevaTarjeta.querySelector('.btn-eliminar-parada');
        botonEliminarNuevo.addEventListener('click', function() {
            if (textareaClonado) {
                localStorage.removeItem(textareaClonado.id);
            }
            nuevaTarjeta.remove();
        });

        const botonGuardarNuevo = nuevaTarjeta.querySelector('.btn-guardar-parada');
        if (botonGuardarNuevo) {
            botonGuardarNuevo.addEventListener('click', function() {
                if (textareaClonado) {
                    localStorage.removeItem(textareaClonado.id);
                }
            });
        }

        contadorParadas++;
        lineaTiempo.appendChild(nuevaTarjeta);
    });

    // MODALES Y EVENTOS GLOBALES DE CIERRE

    // Visor Lightbox (Foto de Portada)
    const visorModal = document.getElementById('visor-foto-modal');
    const imagenVisor = document.getElementById('imagen-visor');
    const btnCerrarVisor = document.querySelector('.btn-cerrar-visor');
    const overlayPortada = document.querySelector('.overlay-portada');

    if (visorModal && overlayPortada) {
        overlayPortada.addEventListener('click', function() {
            const bgImage = headerPortada.style.backgroundImage;
            if (bgImage && bgImage !== 'none') {
                const urlLimpia = bgImage.replace(/^url\(["']?/, '').replace(/["']?\)$/, '');
                imagenVisor.src = urlLimpia;
                visorModal.classList.add('activo');
            }
        });

        btnCerrarVisor.addEventListener('click', function() {
            visorModal.classList.remove('activo');
        });

        visorModal.addEventListener('click', function(e) {
            if (e.target === visorModal) visorModal.classList.remove('activo');
        });
    }

    // Cierres con tecla ESCAPE (Modo Zen y Visor)
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            salirModoZen();
            if (visorModal && visorModal.classList.contains('activo')) {
                visorModal.classList.remove('activo');
            }
        }
    });

    // Cierre con clic de Modo Zen
    if (overlayTexto) {
        overlayTexto.addEventListener('click', salirModoZen);
    }

    // Cierre con clic fuera del Buscador
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.buscador-ciudad-wrapper')) {
            const listasAbiertas = document.querySelectorAll('.lista-resultados-ciudad.activa');
            listasAbiertas.forEach(lista => lista.classList.remove('activa'));
        }
    });

});