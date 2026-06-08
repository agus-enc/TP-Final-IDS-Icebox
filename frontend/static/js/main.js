document.addEventListener('DOMContentLoaded', () => {
   
    // 1. Hacer desaparecer los carteles de alerta de Flask a los 3 segundos
    const alerts = document.querySelectorAll('.flash-message');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 3000);
    });

    // 2. LÓGICA DE DETECCIÓN DE RUTA DE FLASK Y CLICKS EN VIVO
    
    const list = document.querySelectorAll('.router ul .list');
    const currentUrl = window.location.pathname;

    list.forEach((item) => {
        // --- PARTE A: Lo que pasa cuando la página recién carga ---
        item.classList.remove('active');
        const link = item.querySelector('a').getAttribute('href');
       
        if (currentUrl.includes(link) || (currentUrl === '/' && link.includes('heladera'))) {
            item.classList.add('active');
        }

        // --- PARTE B: Lo que pasa cuando haces clic (NUEVO) ---
        item.addEventListener('click', function() {
            // Le sacamos la clase active a todos los botones
            list.forEach(li => li.classList.remove('active'));
            // Se la ponemos solo al que acabas de clickear
            this.classList.add('active');
        });
    });
});

// Lógica para el menú desplegable del usuario
// =========================================================
// 👤 LÓGICA INTEGRADA: MENÚ DESPLEGABLE Y MODAL DE AJUSTES
// =========================================================
document.addEventListener('DOMContentLoaded', function() {
    const userMenuTrigger = document.getElementById('user-menu-trigger');
    const userDropdown = document.getElementById('user-dropdown');
    const btnAbrirAjustes = document.getElementById('btn-abrir-ajustes');
    const modalAjustes = document.getElementById('modal-ajustes-usuario');
    const btnCerrarAjustes = document.getElementById('btn-cerrar-ajustes');
    const btnCancelarAjustes = document.getElementById('btn-cancelar-ajustes');

    if (userMenuTrigger && userDropdown) {
        
        // Al hacer clic en el botón/área de usuario
        userMenuTrigger.addEventListener('click', function(event) {

            // CASO TUYO: Si hicieron clic exactamente en "Ajustes de Usuario"
            if (event.target.closest('#btn-abrir-ajustes')) {
                event.preventDefault();
                event.stopPropagation(); // Evita que el click reactive el menú padre

                console.log("¡EL BOTÓN SI RESPONDE AL CLIC!");
                
                userDropdown.classList.remove('show'); // Escondemos el dropdown

                
                if (modalAjustes) {
                    modalAjustes.classList.add('activo');
                }
                return; // Cortamos la ejecución acá
            }

            // Si el clic vino de cualquier otro enlace del dropdown (Cerrar Sesión, Admin), dejamos que siga viaje
            if (event.target.closest('.dropdown-item')) {
                return; 
            }

            // Comportamiento normal: Abrir o cerrar el menú desplegable al tocar el botón de usuario
            event.preventDefault(); 
            event.stopPropagation(); 
            userDropdown.classList.toggle('show');
        });

        // Si hacen clic en cualquier otro lado de la pantalla, se cierra solo el dropdown
        window.addEventListener('click', function(event) {
            if (!userMenuTrigger.contains(event.target)) {
                userDropdown.classList.remove('show');
            }
        });
    }

 // Funciones exclusivas para cerrar tu modal de Ajustes
    if (modalAjustes) {
        function cerrarModalAjustes() {
            modalAjustes.classList.remove('activo'); 
            const form = document.getElementById('form-ajustes-usuario');
            if (form) form.reset(); // Limpia los inputs para que no queden contraseñas escritas
        }

        if (btnCerrarAjustes) btnCerrarAjustes.addEventListener('click', cerrarModalAjustes);
        if (btnCancelarAjustes) btnCancelarAjustes.addEventListener('click', cerrarModalAjustes);
        
        // Cerrar si tocan la parte oscura de afuera del recuadro
        modalAjustes.addEventListener('click', function(e) {
            if (e.target === modalAjustes) cerrarModalAjustes();
        });
    }
});

// CREADOR DE VIAJES
document.addEventListener('DOMContentLoaded', function() {

    const btnNavCrear = document.getElementById('btn-nav-crear'); // Botón '+' del nav
    const modalCreador = document.getElementById('modal-creador-viajes');
    const btnCerrarCreador = document.getElementById('btn-cerrar-creador');
    const btnCrearParada = document.getElementById('btn-crear-parada-creador');
    const lineaTiempoCreador = document.getElementById('linea-tiempo-creador');
    let contadorParadasCreador = 1;

    if (btnNavCrear && modalCreador) {
        btnNavCrear.addEventListener('click', function(event) {
            event.preventDefault();
            modalCreador.classList.add('activo');
            document.body.style.overflow = 'hidden';
        });

        function cerrarModal() {
            modalCreador.classList.remove('activo');
            document.body.style.overflow = '';
        }

        btnCerrarCreador.addEventListener('click', cerrarModal);
        modalCreador.addEventListener('click', function(event) {
            if (event.target === modalCreador) cerrarModal();
        });

        const wrapperPrimeraParada = document.getElementById('wrapper-ciudad-creador-1');
        if (wrapperPrimeraParada) window.inicializarBuscadorCiudades(wrapperPrimeraParada);

        // Clonar Paradas
        btnCrearParada.addEventListener('click', function() {
            contadorParadasCreador++;

            const molde = lineaTiempoCreador.querySelector('.tarjeta-parada-creador');
            const nuevaTarjeta = molde.cloneNode(true);

            // --- LIMPIEZA Y REASIGNACIÓN DEL CLON ---

            // 1. Buscador de Ciudades
            const wrapperCiudad = nuevaTarjeta.querySelector('.buscador-ciudad-wrapper');
            const inputVisible = nuevaTarjeta.querySelector('.input-buscador-ciudad');
            const inputHiddenCiudad = nuevaTarjeta.querySelector('input[type="hidden"][name^="ciudad_parada_"]');
            const ulResultados = nuevaTarjeta.querySelector('.lista-resultados-ciudad');

            if (wrapperCiudad) wrapperCiudad.id = `wrapper-ciudad-creador-${contadorParadasCreador}`;
            if (inputVisible) {
                inputVisible.id = `input-ciudad-creador-${contadorParadasCreador}`;
                inputVisible.value = "";
            }
            if (inputHiddenCiudad) {
                inputHiddenCiudad.name = `ciudad_parada_${contadorParadasCreador}`;
                inputHiddenCiudad.id = `hidden-ciudad-creador-${contadorParadasCreador}`;
                inputHiddenCiudad.value = "";
            }
            if (ulResultados) {
                ulResultados.id = `resultados-ciudad-creador-${contadorParadasCreador}`;
                ulResultados.innerHTML = '';
            }

            // Reseña Oculta
            const inputTextoOculto = nuevaTarjeta.querySelector('input[type="hidden"][name^="texto_parada_"]');
            if (inputTextoOculto) {
                inputTextoOculto.name = `texto_parada_${contadorParadasCreador}`;
                inputTextoOculto.value = "";
            }

            // Clonar Imanes
            const seccionIman = nuevaTarjeta.querySelector('.seccion-iman');
            if (seccionIman) {
                seccionIman.id = "seccion-iman-" + contadorParadasCreador;

                // Reset Input Oculto Principal
                const inputTipo = seccionIman.querySelector('.input-tipo-iman');
                if (inputTipo) {
                    inputTipo.name = "tipo_iman_" + contadorParadasCreador;
                    inputTipo.value = "ninguno";
                }

                // Reset Archivo y Visuales
                const inputArchivo = seccionIman.querySelector('.input-archivo-iman');
                const contenedorFoto = seccionIman.querySelector('.contenedor-foto-iman');

                if (inputArchivo && contenedorFoto) {
                    inputArchivo.id = "foto-parada-creador-" + contadorParadasCreador;
                    inputArchivo.name = "archivo_iman_" + contadorParadasCreador;
                    contenedorFoto.setAttribute('for', "foto-parada-creador-" + contadorParadasCreador);
                }

                window.limpiarContenedorVisualIman(seccionIman);

                // Reset Toggle y País
                const toggleOficial = seccionIman.querySelector('.checkbox-iman-oficial');
                if (toggleOficial) toggleOficial.checked = false;
                const inputPais = seccionIman.querySelector('.input-pais-iman');
                if (inputPais) {
                    inputPais.name = "pais_iman_" + contadorParadasCreador;
                    inputPais.value = "";
                }
            }

            lineaTiempoCreador.appendChild(nuevaTarjeta);
            nuevaTarjeta.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            window.inicializarBuscadorCiudades(wrapperCiudad);
        });

        // Borrado de Paradas e Imanes
        lineaTiempoCreador.addEventListener('click', function(event) {
            if (event.target.classList.contains('btn-eliminar-parada')) {
                const tarjeta = event.target.closest('.tarjeta-parada-creador');
                if (lineaTiempoCreador.querySelectorAll('.tarjeta-parada-creador').length > 1) {
                    tarjeta.remove();
                }
            }
        });

        // Validación
        const formCreador = document.getElementById('form-creador-viaje');

        if (formCreador) {
            formCreador.addEventListener('submit', function(event) {
                window.validarCiudadesViaje(formCreador, event);
            });
        }
    }
});

/* --- LÓGICA GLOBAL DE IMANES -------- */
window.limpiarContenedorVisualIman = function(seccion) {
    const label = seccion.querySelector('.contenedor-foto-iman');
    const inputArchivo = seccion.querySelector('.input-archivo-iman');
    const btnEliminar = seccion.querySelector('.btn-eliminar-iman');

    if (inputArchivo) inputArchivo.value = '';
    if (btnEliminar) btnEliminar.style.display = 'none';
    if (label) {
        label.style.backgroundImage = 'none';
        label.classList.add('vacio');
        label.innerHTML = `<span class="icono-mas">+</span><p>Subir Imán</p>`;
    }
};

// Atrapa clicks del Creador Y del Editor
document.addEventListener('change', function(event) {
    // Imán Personalizado
    if (event.target.matches('input[type="file"].input-archivo-iman')) {
        const archivo = event.target.files[0];
        const seccion = event.target.closest('.seccion-iman');

        if (archivo) {
            const urlTemporal = URL.createObjectURL(archivo);
            const label = seccion.querySelector('.contenedor-foto-iman');

            label.style.backgroundImage = `url('${urlTemporal}')`;
            label.classList.remove('vacio');
            label.innerHTML = '';
            seccion.querySelector('.btn-eliminar-iman').style.display = 'flex';
            seccion.querySelector('.input-tipo-iman').value = 'personalizado';

            const toggleOficial = seccion.querySelector('.checkbox-iman-oficial');
            if (toggleOficial) toggleOficial.checked = false;
        }
    }

    // Imán Oficial
    if (event.target.matches('.checkbox-iman-oficial')) {
        const seccion = event.target.closest('.seccion-iman');
        const inputTipo = seccion.querySelector('.input-tipo-iman');

        if (event.target.checked) {
            inputTipo.value = 'predeterminado';
        } else {
            inputTipo.value = 'ninguno';
        }

        window.limpiarContenedorVisualIman(seccion);
    }
});

// Botón para eliminar iman
document.addEventListener('click', function(event) {
    const btnEliminar = event.target.closest('.btn-eliminar-iman');
    if (btnEliminar) {
        const seccion = btnEliminar.closest('.seccion-iman');
        window.limpiarContenedorVisualIman(seccion);
        seccion.querySelector('.input-tipo-iman').value = 'ninguno';
    }
});

// Validar ciudades antes de guardar
window.validarCiudadesViaje = function(formulario, evento) {
    let formValido = true;
    const inputsOcultos = formulario.querySelectorAll('input[type="hidden"][name^="ciudad_parada_"]');

    inputsOcultos.forEach(input => {
        const inputVisible = input.previousElementSibling;

        if (input.value.trim() === "") {
            formValido = false;
            if (inputVisible) inputVisible.style.border = "2px solid #e74c3c";
        } else {
            if (inputVisible) inputVisible.style.border = "";
        }
    });

    if (!formValido) {
        evento.preventDefault();
        alert("Por favor, selecciona una ciudad válida de la lista en todas tus paradas antes de guardar.");
        return false;
    }
    return true;
};

// Inicializar Buscadores de Ciudades
window.inicializarBuscadorCiudades = function(wrapper) {
    const inputVisible = wrapper.querySelector('.input-buscador-ciudad');
    const inputOculto = wrapper.querySelector('input[type="hidden"]');
    const listaResultados = wrapper.querySelector('.lista-resultados-ciudad');

    if (!inputVisible || !inputOculto || !listaResultados || typeof CIUDADES_DB === 'undefined') return;

    inputVisible.addEventListener('input', function() {
        inputOculto.value = "";
        const valorBuscado = inputVisible.value.toLowerCase().trim();
        listaResultados.innerHTML = '';

        if (valorBuscado.length === 0) {
            listaResultados.classList.remove('activa');
            return;
        }

        const coincidencias = CIUDADES_DB.filter(ciudad =>
            ciudad.nombre.toLowerCase().includes(valorBuscado) ||
            (ciudad.pais && ciudad.pais.toLowerCase().includes(valorBuscado))
        );

        if (coincidencias.length > 0) {
            coincidencias.forEach(ciudad => {
                const li = document.createElement('li');
                li.textContent = `${ciudad.nombre}, ${ciudad.pais}`;

                li.addEventListener('click', function() {
                    inputVisible.value = `${ciudad.nombre}, ${ciudad.pais}`;
                    inputOculto.value = ciudad.id_ciudad;
                    listaResultados.classList.remove('activa');

                    const tarjeta = wrapper.closest('.tarjeta-parada, .tarjeta-parada-creador');
                    if (tarjeta) {
                        const inputPais = tarjeta.querySelector('.input-pais-iman');
                        if (inputPais && ciudad.pais) inputPais.value = ciudad.pais;
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

    document.addEventListener('click', function(event) {
        if (!wrapper.contains(event.target)) listaResultados.classList.remove('activa');
    });
};
