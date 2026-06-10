document.addEventListener('DOMContentLoaded', () => {

    const modalEnfoque = document.getElementById('modal-enfoque-foto');
    const btnCerrarModal = document.querySelector('.btn-cerrar-modal-foto');
    const imgEnfoque = document.getElementById('img-enfoque');
    const inputEpigrafe = document.getElementById('input-epigrafe');
    const btnGuardarEpi = document.getElementById('btn-guardar-epigrafe');

    let totalSlots = document.querySelectorAll('.slot-foto-wrapper').length;
    let actualSlotWrapper = null;

    function inicializarSlot(wrapper) {
        const inputFoto = wrapper.querySelector('.input-foto-diario');
        const btnReemplazar = wrapper.querySelector('.btn-reemplazar');
        const btnBorrar = wrapper.querySelector('.btn-borrar');
        const imgPreview = wrapper.querySelector('.img-preview');
        const label = wrapper.querySelector('.slot-foto');
        const controles = wrapper.querySelector('.controles-foto');
        const epigrafeOculto = wrapper.querySelector('.epigrafe-data');

        // CARGAR IMAGEN
        inputFoto.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();

                reader.onload = function(event) {
                    imgPreview.src = event.target.result;
                    imgPreview.style.display = 'block';
                    label.style.display = 'none';
                    controles.style.display = 'flex';
                    wrapper.classList.add('con-foto');

                    const idExistenteInput = wrapper.querySelector('input[name^="id_foto_existente_"]');
                    const borrarImgInput = wrapper.querySelector('.input-borrar-img');
                    if (idExistenteInput && borrarImgInput) borrarImgInput.value = idExistenteInput.value;
                }
                reader.readAsDataURL(this.files[0]);
            }
        });

        if (btnReemplazar) {
            btnReemplazar.addEventListener('click', function(event) {
                event.stopPropagation();
                inputFoto.click();
            });
        }

        if (btnBorrar) {
            btnBorrar.addEventListener('click', function(event) {
                event.stopPropagation();
                inputFoto.value = '';
                imgPreview.src = '';
                imgPreview.style.display = 'none';
                label.style.display = '';
                label.classList.remove('oculto');
                label.classList.add('vacio');
                controles.style.display = 'none';
                epigrafeOculto.value = '';
                wrapper.classList.remove('con-foto');

                const idExistenteInput = wrapper.querySelector('input[name^="id_foto_existente_"]');
                const borrarImgInput = wrapper.querySelector('.input-borrar-img');
                if (idExistenteInput && borrarImgInput) borrarImgInput.value = idExistenteInput.value;
            });
        }

        // MODO ZEN
        wrapper.addEventListener('click', function(event) {
            if (this.classList.contains('con-foto') && !event.target.closest('.btn-control-foto') && event.target.type !== 'file') {
                event.preventDefault();
                actualSlotWrapper = this;
                imgEnfoque.src = imgPreview.src;
                inputEpigrafe.value = epigrafeOculto.value;

                modalEnfoque.classList.add('activo');
                document.body.style.overflow = 'hidden';

                setTimeout(() => inputEpigrafe.focus(), 50);
            }
        });
    }

    // INICIALIZAR LOS SLOTS QUE YA ESTÁN EN EL HTML
    document.querySelectorAll('.slot-foto-wrapper').forEach(wrapper => {
        inicializarSlot(wrapper);
    });

    // LÓGICA DEL MODAL
    btnGuardarEpi.addEventListener('click', () => {
        if (actualSlotWrapper) {
            const epigrafeOculto = actualSlotWrapper.querySelector('.epigrafe-data');
            epigrafeOculto.value = inputEpigrafe.value;
            cerrarModal();
        }
    });

    function cerrarModal() {
        modalEnfoque.classList.remove('activo');
        document.body.style.overflow = 'auto';
        actualSlotWrapper = null;
    }

    btnCerrarModal.addEventListener('click', cerrarModal);

    modalEnfoque.addEventListener('click', (event) => {
        if (event.target === modalEnfoque) cerrarModal();
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && modalEnfoque.classList.contains('activo')) {
            cerrarModal();
        }
    });

    // CLONACIÓN DE PÁGINAS
    const btnAgregarPaginas = document.getElementById('btn-agregar-paginas');

    if (btnAgregarPaginas) {
        btnAgregarPaginas.addEventListener('click', function(event) {
            event.preventDefault();

            const moldeLibro = document.querySelector('.libro-abierto');
            const nuevoLibro = moldeLibro.cloneNode(true);
            const wrappersClonados = nuevoLibro.querySelectorAll('.slot-foto-wrapper');

            wrappersClonados.forEach(wrapper => {
                totalSlots++;

                wrapper.classList.remove('con-foto');

                const imgPreview = wrapper.querySelector('.img-preview');
                if (imgPreview) {
                    imgPreview.src = '';
                    imgPreview.style.display = 'none';
                }

                const controles = wrapper.querySelector('.controles-foto');
                if (controles) controles.style.display = 'none';

                const label = wrapper.querySelector('.slot-foto');
                if (label) {
                    label.style.display = '';
                    label.className = 'slot-foto vacio';
                    label.setAttribute('for', `foto-${totalSlots}`);
                }

                const inputFoto = wrapper.querySelector('.input-foto-diario');
                if (inputFoto) {
                    inputFoto.id = `foto-${totalSlots}`;
                    inputFoto.name = `nueva_foto_${totalSlots}`;
                    inputFoto.value = '';
                }

                const epigrafe = wrapper.querySelector('.epigrafe-data');
                if (epigrafe) {
                    epigrafe.name = `epigrafe_${totalSlots}`;
                    epigrafe.value = '';
                }

                const residuales = wrapper.querySelectorAll('.input-img-actual, .input-borrar-img, input[name^="id_foto_existente"]');
                residuales.forEach(res => res.remove());

                inicializarSlot(wrapper);
            });

            btnAgregarPaginas.parentNode.insertBefore(nuevoLibro, btnAgregarPaginas);
        });
    }
});