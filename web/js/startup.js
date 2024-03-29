$(function() {
	var seq = 0;
	var lastHeading = 0;
	var headingThr = 10;

	  function updateMap(lon,lat){
	        var myLatLng = new google.maps.LatLng( lat, lon );
	        google_map.setCenter(myLatLng);   
	        map_marker.setPosition(myLatLng);
	  }
	  function updateMarker(heading){
	  		var diff = Math.abs(heading - lastHeading);
	  		if(diff >= headingThr){
	  			lastHeading = heading;
	  			// To proevent frequent rendering :)
		          map_marker.setOptions(    
		          				{position: google_map.getCenter(),

		                                  icon: {
		                                    rotation: heading,
		                                    path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
		                                    scale: 10,
		                                    fillOpacity: 1,
		                                    fillColor: "#FF0000"
		                                  },

		                                  draggable: true,
		                                  map: google_map}
		          );
      	}
	  }

      var wsuri = "ws://10.8.0.6:1001";

      if ("WebSocket" in window) {
      	var sock = new WebSocket(wsuri);
      } else if ("MozWebSocket" in window) {
      	var sock = new MozWebSocket(wsuri);
      } else {
      	console.log("Browser does not support WebSocket!");
      }

      if (sock) {
         sock.onopen = function() {
            console.log("Telemetry Connected to " + wsuri);
         }

         sock.onclose = function(e) {
            console.log("Connection closed (wasClean = " + e.wasClean + ", code = " + e.code + ", reason = '" + e.reason + "')");
            sock = null;
            setTimeout(function () {location.reload();}, 2*1000);
         }

         sock.onmessage = function(e) {
               //console.log(e.data);
               var obj = JSON.parse(e.data);

               if (obj.type == "flightmode"){
               		document.getElementById("modebox").innerHTML = obj.content.flightmode;
               }
               
               if (obj.type == "sys_status"){
               		
               		gauge_voltage.refresh(obj.content.voltage_battery);
               		gauge_current.refresh(obj.content.current_battery);
               		gauge_battery_remaining.refresh(obj.content.battery_remaining);
               		
               } 

               if (obj.type == "gps"){
               		
               		gauge_satellites_visible.refresh(obj.content.satellites_visible);
               		updateMap(obj.content.lon,obj.content.lat);
               		
               } 

               if (obj.type == "vfr_hud"){
               		
               		gauge_altitude.refresh(obj.content.alt);
               		gauge_climb.refresh(Math.abs(obj.content.climb));
               		updateMarker(obj.content.heading);
               		
               } 

               if (obj.type == "attitude"){
               		
               		gauge_pitch.refresh(Math.abs(obj.content.pitchspeed));
               		gauge_yaw.refresh(Math.abs(obj.content.yawspeed));
               		gauge_roll.refresh(Math.abs(obj.content.rollspeed));
               		
               } 
          }

		setInterval(function(){sendTick()}, 1000);

        function sendTick(){
      		var msg = "{\"type\":\"tick_client\",\"seq\":"+seq+"}";
	      	if (sock) {
	      	   sock.send(msg);
	      	   seq++;
	      	   console.log("Sent: " + msg);
	      	}
      }
        }

});

