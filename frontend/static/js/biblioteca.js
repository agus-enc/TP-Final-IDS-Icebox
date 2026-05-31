document.addEventListener("DOMContentLoaded", () => {
    const mueble = document.getElementById("mueble-libros");
    const modalEliminar = document.getElementById('modal-eliminar');
    const listaEliminar = document.getElementById('lista-viajes-eliminar');
    
    if (!mueble || !modalEliminar || !listaEliminar) return;

    function organizarEstantes() {
        const todosLosLibros = Array.from(mueble.querySelectorAll('.book'));
        const estantes = mueble.querySelectorAll('.subshelf');
        todosLosLibros.forEach((libro, index) => {
            const indiceEstante = Math.floor(index / 10);
            if (estantes[indiceEstante]) estantes[indiceEstante].appendChild(libro);
        });
    }

    organizarEstantes();

    document.getElementById('btn-abrir-eliminar')?.addEventListener('click', () => {
        armarListaModal();
        modalEliminar.classList.remove('oculto');
    });

    document.getElementById('btn-cerrar-eliminar')?.addEventListener('click', () => {
        modalEliminar.classList.add('oculto');
    });

    function armarListaModal() {
        listaEliminar.innerHTML = "";
        const librosDisponibles = document.querySelectorAll('.book');
        librosDisponibles.forEach(libro => {
            const id = libro.getAttribute('data-id');
            const destino = libro.getAttribute('data-destino');
            const fila = document.createElement('div'); fila.className = "fila-eliminar";
            fila.innerHTML = `<span>${destino}</span><button class="btn-biblioteca-accion" style="padding: 4px 10px; font-size: 0.75rem;">Eliminar</button>`;
            fila.querySelector('button').addEventListener('click', () => confirmarEliminacionLibro(id, destino, libro));
            listaEliminar.appendChild(fila);
        });
    }

    async function confirmarEliminacionLibro(id, destino, elementoLibro) {
        const resultado = await Swal.fire({ title: '¿Eliminar viaje?', text: `Borrar ${destino}`, icon: 'warning', 
            showCancelButton: true, confirmButtonColor: '#22223B', cancelButtonColor: '#a4a9ae' });
        if (resultado.isConfirmed) {
            modalEliminar.classList.add('oculto');
            elementoLibro.remove(); 
            organizarEstantes();
            Swal.fire({ title: '¡Removido!', icon: 'success', timer: 1500, showConfirmButton: false });
        }
    }
});