
const ContentManager = require("./content_manager");

; (function () {
    "use strict"
    window.addEventListener("load", onStart, false);

    var content_manager;

    function onStart(evt) {
        console.log("onStart");
        content_manager = new ContentManager();        
    }



})();