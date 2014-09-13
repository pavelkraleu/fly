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
               		g.refresh(obj.content.voltage_battery);
               		//g.refresh(100);
               } 
          }
        }

});