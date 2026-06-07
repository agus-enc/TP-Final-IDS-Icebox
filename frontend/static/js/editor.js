document.addEventListener('DOMContentLoaded', function() {

    // DATOS Y VARIABLES GLOBALES
    const botonAgregar = document.getElementById('btn-agregar-parada');
    const lineaTiempo = document.querySelector('.linea-tiempo');
    let contadorParadas = document.querySelectorAll('.tarjeta-parada').length + 1;
    let textareaActivo = null;
    const overlayTexto = document.getElementById('overlay-enfoque-texto');

    // FUNCIONES GENERALES
    // Autoguardado
    const formEditor = document.getElementById('formulario-viaje-maestro');
    let idViajeActual = null;
    function protegerConAutoguardado(elementoTextarea) {
        elementoTextarea.addEventListener('input', function() {
            const texto = elementoTextarea.value;
            const llaveUnica = `draft_viaje_${idViajeActual}_${elementoTextarea.id}`;
            localStorage.setItem(llaveUnica, texto);
        });
    }

    // Inyecta borradores del local storage si los hay y vuelve a guardar
    if (formEditor) {
        const textareasEditor = formEditor.querySelectorAll('textarea');
        idViajeActual = formEditor.dataset.idViaje;
        textareasEditor.forEach(textarea => {
            const llaveUnica = `draft_viaje_${idViajeActual}_${textarea.id}`;
            const textoGuardado = localStorage.getItem(llaveUnica);

            if (textoGuardado) textarea.value = textoGuardado;

            protegerConAutoguardado(textarea);
            habilitarModoZen(textarea);
        });
    }

    // Modo Zen para Textareas
    function habilitarModoZen(elementoTextarea) {
        elementoTextarea.addEventListener('focus', function() {
            textareaActivo = elementoTextarea;
            elementoTextarea.classList.add('modo-zen');
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

    // INICIALIZACIÓN DE LA BASE (On Load)
    // Iniciar Buscadores Base
    const wrappersBuscador = document.querySelectorAll('.tarjeta-parada .buscador-ciudad-wrapper');
    for (const wrapper of wrappersBuscador) {
        window.inicializarBuscadorCiudades(wrapper);
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
                if (textarea && textarea.id) {
                    localStorage.removeItem(`draft_viaje_${idViajeActual}_${textarea.id}`);
                }

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
            window.inicializarBuscadorCiudades(wrapperBuscadorClonado);
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

            // Solo reasignamos los ID y for dinámicos
            if (inputArchivo && contenedorFoto) {
                inputArchivo.id = "foto-parada-" + contadorParadas;
                inputArchivo.name = "archivo_iman_" + contadorParadas;
                contenedorFoto.setAttribute('for', "foto-parada-" + contadorParadas);
            }

            window.limpiarContenedorVisualIman(seccionIman);

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
        // Esperamos 400 ms para asegurar que Jinja2 y el CSS hayan renderizado
        // completamente las dimensiones de las tarjetas antes de calcular el scroll.
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
    // VALIDACIÓN Y GARBAGE COLLECTION AL GUARDAR
    if (formEditor) {
        formEditor.addEventListener('submit', function(e) {

            // 1. Llamamos al Guardia de Seguridad Global
            const esValido = window.validarCiudadesViaje(formEditor, e);

            // 2. Garbage Collection: Limpiar el disco SOLO si el formulario pasó la prueba
            if (esValido) {
                const prefijo = `draft_viaje_${idViajeActual}_`;
                for (let i = localStorage.length - 1; i >= 0; i--) {
                    const key = localStorage.key(i);
                    if (key && key.startsWith(prefijo)) {
                        localStorage.removeItem(key);
                    }
                }
            }
        });
    }
});