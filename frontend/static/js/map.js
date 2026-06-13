const map = L.map('map', { // Limites del mapa 
  minZoom: 2,
  maxBounds: [
    [-90, -180], 
    [90, 180]
  ],
  maxBoundsViscosity: 1.0
}).setView([27, 0], 2);

// Tiles (OpenStreetMap)
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  noWrap: true,
  attribution: '&copy; OpenStreetMap'
}).addTo(map);

// Resaltar el país al pasar el mouse
function highlightFeature(e) { 
    var layer = e.target;
    layer.setStyle({
        weight: 2,
        color: '#696969ac',
        dashArray: '',
        fillOpacity: 0.7
    });
    info.update(layer.feature.properties);
}
function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

function cargarImanesEnSidebar(codigoPais) {
  const sidebarContent = document.querySelector('.sidebar-content');
  sidebarContent.innerHTML = ''; 

  const imanes = DATOS_IMANES[codigoPais] || [];

  if (imanes.length === 0) {
    sidebarContent.innerHTML = '<p>Aún no hay imanes aquí.</p>';
    return;
  }

  // Creamos los botones (imanes)
  imanes.forEach(iman => {
    const contenedor = document.createElement('div');
    contenedor.className = 'iman-contenedor';

    const botonIman = document.createElement('button');
    botonIman.className = 'iman-viaje';
    
    const imagenElemento = document.createElement('img'); // Imagen Iman
    imagenElemento.src = iman.imagen_url;
    imagenElemento.alt = `${iman.nombre_ciudad}`;
    imagenElemento.className = 'iman-imagen-real';
    
    botonIman.appendChild(imagenElemento);
    
    botonIman.onclick = () => {
        const textoParaMostrar = iman.relato || "Sin relato disponible para esta parada.";
        abrirResenia(textoParaMostrar);
    };

    const bloqueTexto = document.createElement('div');
    bloqueTexto.className = 'iman-texto-abajo';

    const destinoDiv = document.createElement('div');
    destinoDiv.className = 'iman-destino';
    destinoDiv.innerText = iman.nombre_ciudad; // Nombre de la ciudad

    bloqueTexto.appendChild(destinoDiv);

    contenedor.appendChild(botonIman);  
    contenedor.appendChild(bloqueTexto); 
    
    sidebarContent.appendChild(contenedor);
  });
}

function abrirResenia(relato) {
    const modal = document.getElementById('modal-resenia');
    const contenido = document.getElementById('contenido-resenia'); 
    
    if (modal && contenido) {
        contenido.innerText = relato; 
        modal.classList.add('activo');
        document.body.classList.add('modal-abierto'); 
    } else {
        alert("Error. La reseña no se ha podido cargar."); 
    }
}

function cerrarModal() {
    const modal = document.getElementById('modal-resenia');
    if (modal) {
        modal.classList.remove('activo');
        document.body.classList.remove('modal-abierto');
    }
}

// Cerrar el modal al hacer clic en el fondo
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal-resenia');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                cerrarModal();
            }
        });
    }
});

var geojson;

const urlPaises = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json';

fetch(urlPaises)
  .then(response => response.json())
  .then(data => {
    geojson = L.geoJson(data, {
      style: function(feature) {
        const esVisitado = PAISES_VISITADOS.includes(feature.id);
        return {
          color: "#2b2b2b29", 
          weight: 1.5,
          fillColor: esVisitado ? "#9A8C98" : "#2b81c800",
          fillOpacity: esVisitado ? 0.6 : 0.1
        };
      },
      onEachFeature: function(feature, layer) {
        layer.on({
          click: function(e) {
            const esVisitado = PAISES_VISITADOS.includes(feature.id);

            if (!esVisitado) { // Popup para países no visitados
              L.popup() 
                .setLatLng(e.latlng)
                .setContent(`<b>Este país no ha sido visitado</b>`)
                .openOn(map);
            } else { // Sidebar para países visitados
              const sidebar = document.getElementById('sidebar');
              if (sidebar) {
                sidebar.classList.add('active');
                cargarImanesEnSidebar(feature.id);
              }
            }
          },
          mouseover: highlightFeature,
          mouseout: resetHighlight
        });
      }
    }).addTo(map);
  })
  .catch(function(error) {
    console.error("Error al cargar las divisiones del mundo:", error);
  });

var info = L.control(); // Control para mostrar información 

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); 
    this.update();
    return this._div;
};
info.update = function (props) {
    this._div.innerHTML = '<h4>Información del País</h4>' +  (props ?
        '<b>' + props.name + '</b>'
        : 'Pasa el cursor sobre un país');
};
info.addTo(map);

// Botón de compartir
const shareControl = L.control({ position: 'topright' });

shareControl.onAdd = function (map) {
    const div = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');

    div.innerHTML = `
        <button id="btn-compartir" class="btn-compartir-mapa">
            🔗 Compartir Mapa
        </button>
    `;
    
    div.onclick = function() {
        const urlCompartir = window.location.origin + '/mapa/' + USUARIO_ID + '?token=' + TOKEN_MAPA;
        navigator.clipboard.writeText(urlCompartir).then(() => {
            alert("¡Link copiado al portapapeles!");
        });
    };
    
    return div;
};

shareControl.addTo(map);