   
    navigator.geolocation.getCurrentPosition(function(position) {
        console.log("Latitude:", position.coords.latitude);
        console.log("Longitude:", position.coords.longitude);
      }, function(error) {
        console.error("Erro de geolocalização:", error.message);
      });
       