seq = 0;


$(function() {
      wsuri = "ws://10.0.0.46:10000";

      if ("WebSocket" in window) {
      	sock = new WebSocket(wsuri);
      } else if ("MozWebSocket" in window) {
      	sock = new MozWebSocket(wsuri);
      } else {
      	console.log("Browser does not support WebSocket!");
      }

      if (sock) {
         sock.onopen = function() {
            console.log("Connected to " + wsuri);
         }

         sock.onclose = function(e) {
            console.log("Connection closed (wasClean = " + e.wasClean + ", code = " + e.code + ", reason = '" + e.reason + "')");
            sock = null;
         }

         sock.onmessage = function(e) {
               console.log(e.data);
               obj = JSON.parse(e.data);
               
               if (obj.type == "sys_status"){
               		
               		gauge_voltage.refresh(obj.content.voltage_battery);
               		gauge_current.refresh(obj.content.current_battery);
               		gauge_battery_remaining.refresh(obj.content.battery_remaining);
               		
               } 

               if (obj.type == "gps"){
               		
               		gauge_satellites_visible.refresh(obj.content.satellites_visible);
               		
               } 

               if (obj.type == "vfr_hud"){
               		
               		gauge_altitude.refresh(obj.content.alt);
               		gauge_climb.refresh(obj.content.climb);
               		
               } 
          }

		setInterval(function(){sendTick()}, 1000);

        function sendTick(){
      		msg = "{\"type\":\"tick_client\",\"seq\":"+seq+"}";
	      	if (sock) {
	      	   sock.send(msg);
	      	   seq++;
	      	   console.log("Sent: " + msg);
	      	}
      }
        }

});

