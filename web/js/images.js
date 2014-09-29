$(function() {
   var seq = 0;
   var lastHeading = 0;
   var headingThr = 10;

      var wsuri = "ws://10.8.0.6:1002";

      if ("WebSocket" in window) {
         var sock = new WebSocket(wsuri);
      } else if ("MozWebSocket" in window) {
         var sock = new MozWebSocket(wsuri);
      } else {
         console.log("Browser does not support WebSocket!");
      }

      if (sock) {
         sock.onopen = function() {
            console.log("Images Connected to " + wsuri);
         }

         sock.onclose = function(e) {
            console.log("Connection closed (wasClean = " + e.wasClean + ", code = " + e.code + ", reason = '" + e.reason + "')");
            sock = null;
         }

         sock.onmessage = function(e) {
               //console.log("image"); 
               var image = document.getElementById('camera');
               image.src = 'data:image/jpg;base64,'+e.data;
               image_size = e.data.length;

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

