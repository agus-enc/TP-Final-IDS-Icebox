document.addEventListener("DOMContentLoaded", () => {
    const mueble = document.getElementById("mueble-libros");
    const modalEliminar = document.getElementById('modal-eliminar');
    const btnAbrirEliminar = document.getElementById('btn-abrir-eliminar');
    const btnCerrarEliminar = document.getElementById('btn-cerrar-eliminar');

    if (mueble) {
        const todosLosLibros = Array.from(mueble.querySelectorAll('.book'));
        const estantes = mueble.querySelectorAll('.subshelf');
        todosLosLibros.forEach((libro, index) => {
            const indiceEstante = Math.floor(index / 10);
            if (estantes[indiceEstante]) {
                estantes[indiceEstante].appendChild(libro);
            }
        });

        mueble.addEventListener('click', (e) => {
            const libro = e.target.closest('.book');
            
            if (libro) {
                const idViaje = libro.getAttribute('data-id');
                
                if (idViaje) {
                    window.location.href = `/viajes/${idViaje}/editar`;
                }
            }
        });
    }

    if (btnAbrirEliminar) {
        btnAbrirEliminar.addEventListener('click', () => {
            const libros = document.querySelectorAll('.book');
            
            if (libros.length === 0) {
                Swal.fire({
                    title: '¡Atención!',
                    text: 'No hay ningún viaje para eliminar todavía.',
                    icon: 'warning',
                    confirmButtonText: 'Entendido',
                    confirmButtonColor: '#3085d6',
                    background: '#ffffff'
                });
            } else if (modalEliminar) {
                modalEliminar.classList.remove('oculto');
            }
        });
    }

    if (btnCerrarEliminar && modalEliminar) {
        btnCerrarEliminar.addEventListener('click', () => {
            modalEliminar.classList.add('oculto');
        });
    }

    const formulariosEliminar = document.querySelectorAll('.fila-eliminar form');
    
    formulariosEliminar.forEach(form => {
        form.addEventListener('submit', (e) => {
            //  frena el envío inmediato del formulario a Flask
            e.preventDefault(); 

            const nombreViaje = form.closest('.fila-eliminar').querySelector('span').innerText;
            Swal.fire({
                title: '¿Estás seguro?',
                text: `Vas a eliminar el viaje a "${nombreViaje}". Esta acción no se puede deshacer.`,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Volver',
                background: '#ffffff'
            }).then((result) => {
                if (result.isConfirmed) {
                    form.submit(); 
                }
            });
        });
    });
});