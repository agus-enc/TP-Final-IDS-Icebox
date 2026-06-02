document.addEventListener('DOMContentLoaded', function() {

    // DATOS Y VARIABLES GLOBALES
    const botonAgregar = document.getElementById('btn-agregar-parada');
    const lineaTiempo = document.querySelector('.linea-tiempo');
    let contadorParadas = document.querySelectorAll('.tarjeta-parada').length + 1;

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

            constGrid = coincidencia = CIUDADES_DB.filter(ciudad =>
                ciudad.nombre.toLowerCase().includes(valorBuscado) ||
                (ciudad.pais && ciudad.pais.toLowerCase().includes(valorBuscado))
            );

            if (coincidencias.length > 0) {
                coincidencias.forEach(ciudad => {
                    const li = document.createElement('li');

                    // AHORA EL EDITOR TAMBIÉN MUESTRA "CIUDAD, PAÍS"
                    li.textContent = `${ciudad.nombre}, ${ciudad.pais}`;

                    li.addEventListener('click', function() {
                        inputVisible.value = `${ciudad.nombre}, ${ciudad.pais}`;
                        inputOculto.value = ciudad.id_ciudad;
                        listaResultados.classList.remove('activa');
                        const tarjeta = wrapper.closest('.tarjeta-parada');
                        const inputPais = tarjeta.querySelector('.input-pais-iman');
                        if (inputPais && ciudad.pais) {
                            inputPais.value = ciudad.pais;
                        }
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
    const wrappersBuscador = document.querySelectorAll('.tarjeta-parada .buscador-ciudad-wrapper');
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
                document.getElementById('flag-borrar-portada').value = 'true';
            });
        }
    }

    // LÍNEA DE TIEMPO (Clonación e Imanes)

    // Interfaz dinámica para los tipos de imán
    // LÍNEA DE TIEMPO: NUEVA LÓGICA DE IMANES
    if (lineaTiempo) {

        // 1. Cuando suben una foto (Imán Personalizado)
        lineaTiempo.addEventListener('change', function(e) {
            if (e.target.matches('input[type="file"].input-archivo-iman')) {
                const archivo = e.target.files[0];
                const seccion = e.target.closest('.seccion-iman');

                if (archivo) {
                    const urlTemporal = URL.createObjectURL(archivo);
                    const label = seccion.querySelector('.contenedor-foto-iman');

                    label.style.backgroundImage = `url('${urlTemporal}')`;
                    label.classList.remove('vacio');
                    label.innerHTML = '';

                    seccion.querySelector('.btn-eliminar-iman').style.display = 'flex';
                    seccion.querySelector('.input-tipo-iman').value = 'personalizado';
                    seccion.querySelector('.checkbox-iman-oficial').checked = false;
                }
            }

            // 2. Cuando tocan el Toggle (Imán Oficial)
            if (e.target.matches('.checkbox-iman-oficial')) {
                const seccion = e.target.closest('.seccion-iman');
                const inputTipo = seccion.querySelector('.input-tipo-iman');
                const label = seccion.querySelector('.contenedor-foto-iman');

                if (e.target.checked) {
                    inputTipo.value = 'predeterminado';

                    // Limpiar la foto si el usuario tenía una foto subida
                    seccion.querySelector('.input-archivo-iman').value = '';
                    label.style.backgroundImage = 'none';
                    label.classList.add('vacio');
                    label.innerHTML = `<span class="icono-mas">+</span><p>Subir Imán</p>`;
                    seccion.querySelector('.btn-eliminar-iman').style.display = 'none';
                } else {
                    inputTipo.value = 'ninguno';

                    // NUEVO: Si apagan el oficial, destruimos la bandera pre-cargada
                    label.style.backgroundImage = 'none';
                    label.classList.add('vacio');
                    label.innerHTML = `<span class="icono-mas">+</span><p>Subir Imán</p>`;
                }
            }
        });

        // 3. Cuando tocan la X para borrar la foto
        lineaTiempo.addEventListener('click', function(e) {
            const btnEliminar = e.target.closest('.btn-eliminar-iman');
            if (btnEliminar) {
                const seccion = btnEliminar.closest('.seccion-iman');
                const label = seccion.querySelector('.contenedor-foto-iman');

                seccion.querySelector('.input-archivo-iman').value = '';
                label.style.backgroundImage = 'none';
                label.classList.add('vacio');
                label.innerHTML = `<span class="icono-mas">+</span><p>Subir Imán</p>`;

                btnEliminar.style.display = 'none';
                seccion.querySelector('.input-tipo-iman').value = 'ninguno';
            }
        });
    }

    // Delegación de eventos para Eliminar Parada (Sirve para viejas y nuevas)
    if (lineaTiempo) {
        lineaTiempo.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn-eliminar-parada')) {
                const tarjeta = e.target.closest('.tarjeta-parada');
                const inputId = tarjeta.querySelector('.hidden-id-parada');

                // Si la tarjeta ya existía en la BD (tiene ID), anotamos su ID para borrarlo
                if (inputId && inputId.value) {
                    const inputBorradas = document.getElementById('input-paradas-borradas');
                    if (inputBorradas.value) {
                        inputBorradas.value += ',' + inputId.value; // Ej: "101,105"
                    } else {
                        inputBorradas.value = inputId.value; // Ej: "101"
                    }
                }

                // Limpiar localStorage para que no reviva el texto fantasma
                const textarea = tarjeta.querySelector('.textarea-elegante');
                if (textarea && textarea.id) localStorage.removeItem(textarea.id);

                // Eliminar visualmente y quitar del formulario
                tarjeta.remove();
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
        const inputOcultoClonado = wrapperBuscadorClonado.querySelector('input[type="hidden"]');
        const listaResultadosClonado = nuevaTarjeta.querySelector('.lista-resultados-ciudad');
        const inputIdParada = nuevaTarjeta.querySelector('.hidden-id-parada');

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

        if (inputIdParada) {
            inputIdParada.name = "id_parada_" + contadorParadas;
            inputIdParada.value = ""; // VITAL: Le borramos el ID porque es una parada NUEVA
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
        
        // 4. Clonar la Sección del Imán (NUEVA UI)
        const seccionIman = nuevaTarjeta.querySelector('.seccion-iman');
        if (seccionIman) {
            seccionIman.id = "seccion-iman-" + contadorParadas;

            // Reset Input Oculto
            const inputTipo = seccionIman.querySelector('.input-tipo-iman');
            if(inputTipo) {
                inputTipo.name = "tipo_iman_" + contadorParadas;
                inputTipo.value = "ninguno";
            }

            // Reset Archivo y Visuales
            const inputArchivo = seccionIman.querySelector('.input-archivo-iman');
            const contenedorFoto = seccionIman.querySelector('.contenedor-foto-iman');
            const btnEliminar = seccionIman.querySelector('.btn-eliminar-iman');

            if (inputArchivo && contenedorFoto) {
                inputArchivo.id = "foto-parada-" + contadorParadas;
                inputArchivo.name = "archivo_iman_" + contadorParadas;
                inputArchivo.value = "";

                contenedorFoto.setAttribute('for', "foto-parada-" + contadorParadas);
                contenedorFoto.className = "contenedor-foto-iman vacio";
                contenedorFoto.style.backgroundImage = 'none';
                contenedorFoto.innerHTML = `<span class="icono-mas">+</span><p>Subir Imán</p>`;
            }
            if (btnEliminar) btnEliminar.style.display = 'none';

            // Reset Toggle y País
            const toggleOficial = seccionIman.querySelector('.checkbox-iman-oficial');
            if (toggleOficial) toggleOficial.checked = false;

            const inputPais = seccionIman.querySelector('.input-pais-iman');
            if (inputPais) {
                inputPais.name = "pais_iman_" + contadorParadas;
                inputPais.value = "";
            }
        }

        contadorParadas++;
        lineaTiempo.appendChild(nuevaTarjeta);
        nuevaTarjeta.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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

    // DETECTOR AUTOMÁTICO DE ENFOQUE DESDE HELADERA O CAJÓN
    const parametrosUrl = new URLSearchParams(window.location.search);
    const idCiudadABuscar = parametrosUrl.get("buscar_id_ciudad");

    if (idCiudadABuscar) {
        // Un pequeño timeout garantiza que los textareas carguen sus valores desde el LocalStorage primero
        setTimeout(() => {
            // Buscamos el input oculto que guarda el id_ciudad en cada tarjeta
            const inputsOcultosCiudades = document.querySelectorAll(".tarjeta-parada input[type='hidden'][id^='hidden-ciudad-']");
            
            inputsOcultosCiudades.forEach(inputOculto => {
                // Comparamos si el ID de la ciudad coincide con el de la URL
                if (inputOculto.value === idCiudadABuscar) {
                    
                    const tarjetaParada = inputOculto.closest(".tarjeta-parada") || inputOculto.closest("[class*='tarjeta']");
                    
                    if (tarjetaParada) {
                        // Scroll fluido hacia el medio del contenedor
                        tarjetaParada.scrollIntoView({
                            behavior: "smooth",
                            block: "center"
                        });
                    }
                }
            });
        }, 400);
    }
});