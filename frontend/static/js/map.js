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

var geojson;

function highlightFeature(e) { // Resaltar el país al pasar el mouse
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
          fillColor: esVisitado ? "#2b81c8" : "#2b81c800", // Azul si fue, transparente si no
          fillOpacity: esVisitado ? 0.6 : 0.1
        };
      },
      onEachFeature: function(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight
        });
      }
    }).addTo(map);
  })
  .catch(function(error) {
    console.error("Error al cargar las divisiones del mundo:", error);
  });

var info = L.control();

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