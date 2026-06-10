document.addEventListener('DOMContentLoaded', () => {

    const inputsFoto = document.querySelectorAll('.input-foto-diario');
    const modalEnfoque = document.getElementById('modal-enfoque-foto');
    const btnCerrarModal = document.querySelector('.btn-cerrar-modal-foto');
    const imgEnfoque = document.getElementById('img-enfoque');
    const inputEpigrafe = document.getElementById('input-epigrafe');
    const btnGuardarEpi = document.getElementById('btn-guardar-epigrafe');

    let currentSlotWrapper = null;

    // CARGAR IMAGEN EN EL SLOT
    inputsFoto.forEach(input => {
        input.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                const wrapper = this.closest('.slot-foto-wrapper');
                const imgPreview = wrapper.querySelector('.img-preview');
                const label = wrapper.querySelector('.slot-foto');
                const controles = wrapper.querySelector('.controles-foto');

                reader.onload = function(e) {
                    imgPreview.src = e.target.result;
                    imgPreview.style.display = 'block'; // Fuerza a mostrar la imagen
                    label.style.display = 'none';       // Fuerza a ocultar el '+'
                    controles.style.display = 'flex';   // Habilita los botones
                    wrapper.classList.add('con-foto');
                    const imgActualInput = wrapper.querySelector('.input-img-actual');
                    const borrarImgInput = wrapper.querySelector('.input-borrar-img');
                    if (imgActualInput && borrarImgInput) borrarImgInput.value = imgActualInput.value;
                }

                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    // LÓGICA DE CADA TARJETA (Abrir, Borrar, Reemplazar)
    document.querySelectorAll('.slot-foto-wrapper').forEach(wrapper => {

        const btnReemplazar = wrapper.querySelector('.btn-reemplazar');
        const btnBorrar = wrapper.querySelector('.btn-borrar');
        const inputFoto = wrapper.querySelector('.input-foto-diario');
        const imgPreview = wrapper.querySelector('.img-preview');
        const label = wrapper.querySelector('.slot-foto');
        const controles = wrapper.querySelector('.controles-foto');
        const epigrafeOculto = wrapper.querySelector('.epigrafe-data');

        // BOTÓN REEMPLAZAR: Simula un clic en el input invisible
        if (btnReemplazar) {
            btnReemplazar.addEventListener('click', function(e) {
                e.stopPropagation(); // Evita que se abra el pop-up de enfoque
                inputFoto.click();
            });
        }

        // BOTÓN BORRAR: Resetea por completo la tarjeta
        if (btnBorrar) {
            btnBorrar.addEventListener('click', function(e) {
                e.stopPropagation(); // Evita que se abra el pop-up
                inputFoto.value = ''; // Limpia el archivo
                imgPreview.src = '';
                imgPreview.style.display = 'none';
                label.style.display = '';
                label.classList.remove('oculto');
                label.classList.add('vacio');
                controles.style.display = 'none';
                epigrafeOculto.value = ''; // Borra el texto del epígrafe
                wrapper.classList.remove('con-foto');
                const imgActualInput = wrapper.querySelector('.input-img-actual');
                const borrarImgInput = wrapper.querySelector('.input-borrar-img');
                if (imgActualInput && borrarImgInput) borrarImgInput.value = imgActualInput.value;
            });
        }

        // CLIC EN LA FOTO: Abrir Modo Zen
        wrapper.addEventListener('click', function(e) {
            // Solo abrimos si tiene foto, y SI NO SE HIZO CLIC EN LOS BOTONES NI EN EL INPUT
            if (this.classList.contains('con-foto') && !e.target.closest('.btn-control-foto') && e.target.type !== 'file') {
                e.preventDefault();

                currentSlotWrapper = this;

                imgEnfoque.src = imgPreview.src;
                inputEpigrafe.value = epigrafeOculto.value;

                modalEnfoque.classList.add('activo');
                document.body.style.overflow = 'hidden';
                inputEpigrafe.focus();
            }
        });
    });

    // GUARDAR EL EPÍGRAFE
    btnGuardarEpi.addEventListener('click', () => {
        if (currentSlotWrapper) {
            const epigrafeOculto = currentSlotWrapper.querySelector('.epigrafe-data');
            epigrafeOculto.value = inputEpigrafe.value;
            cerrarModal();
        }
    });

    // FUNCIONES DE CIERRE DEL MODAL
    function cerrarModal() {
        modalEnfoque.classList.remove('activo');
        document.body.style.overflow = 'auto';
        currentSlotWrapper = null;
    }

    btnCerrarModal.addEventListener('click', cerrarModal);

    modalEnfoque.addEventListener('click', (e) => {
        if (e.target === modalEnfoque) cerrarModal();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modalEnfoque.classList.contains('activo')) {
            cerrarModal();
        }
    });

});