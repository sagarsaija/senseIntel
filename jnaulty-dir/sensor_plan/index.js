// This example requires the Drawing library. Include the libraries=drawing
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=drawing">
function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 37.79582214355469, lng: -122.39362335205078 },
    zoom: 13,
  });
  const drawingManager = new google.maps.drawing.DrawingManager({
    drawingMode: google.maps.drawing.OverlayType.MARKER,
    drawingControl: true,
    drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_CENTER,
      drawingModes: [
        google.maps.drawing.OverlayType.MARKER,
        google.maps.drawing.OverlayType.POLYGON,
      ],
    },
    markerOptions: {
      icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
    },
    circleOptions: {
      fillColor: "#ffff00",
      fillOpacity: 1,
      strokeWeight: 5,
      clickable: false,
      editable: true,
      zIndex: 1,
    },
  });

  drawingManager.setMap(map);
  // Add event listener for overlaycomplete event
  google.maps.event.addListener(drawingManager, 'overlaycomplete', function(event) {
    var overlayType = event.type;
    console.log("Overlay type:", overlayType);
    var overlay = event.overlay;
    
    if (overlayType === "polygon") {
      var coordinates = overlay.getPath().getArray().map(function(latLng) {
        return latLng.toJSON();
      });
      console.log("Polygon coordinates:", coordinates);

      // Example: Use the polygon coordinates for downstream usage
      // performSomeAction(coordinates);
    }
  });

 google.maps.event.addListener(drawingManager, 'overlaycomplete', function(event) {
    var overlayType = event.type;
    console.log("Overlay type:", overlayType);
    var overlay = event.overlay;
    
    if (overlayType === "polygon") {
      var coordinates = overlay.getPath().getArray();
      console.log("Polygon coordinates:", coordinates);

      // Get bounding box of the polygon
      var bounds = new google.maps.LatLngBounds();
      coordinates.forEach(function(coord) {
        bounds.extend(coord);
      });

      // Calculate the number of rows and columns for the grid
      var numCols = 5; // Example: divide the polygon into a 5x5 grid
      var numRows = 5;
      
      var cellWidth = (bounds.getNorthEast().lng() - bounds.getSouthWest().lng()) / numCols;
      var cellHeight = (bounds.getNorthEast().lat() - bounds.getSouthWest().lat()) / numRows;

      // Loop through each cell in the grid and place a sensor at the center if it's within the polygon
      for (var i = 0; i < numRows; i++) {
        for (var j = 0; j < numCols; j++) {
          var cellCenter = {
            lat: bounds.getSouthWest().lat() + (i + 0.5) * cellHeight,
            lng: bounds.getSouthWest().lng() + (j + 0.5) * cellWidth
          };
          // Check if cellCenter is within the polygon
          if (google.maps.geometry.poly.containsLocation(cellCenter, overlay)) {
            var sensorMarker = new google.maps.Marker({
              position: cellCenter,
              map: map,
              title: 'Sensor Location'
            });
          }
        }
      }
    }
  });
}

window.initMap = initMap;
