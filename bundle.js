(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){

class ContentManager{

    
    constructor(){
        this.lorem_ipsum = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.";
    
        this.element = document.getElementById("grid_item_content");

        this.generateEntry(
            "3-Torus FlowVis Tool", 
            "https://sfb-trr191.github.io/3-torus-flowvis-tool-tutorial/images/test_main.png",
            "https://sfb-trr191.github.io/3-torus-flowvis-tool/",
            this.lorem_ipsum);
        this.generateEntry(
            "Wire Billiards", 
            "https://upload.wikimedia.org/wikipedia/en/d/d6/Image_coming_soon.png",
            "https://sfb-trr191.github.io/wire-billiards/",
            this.lorem_ipsum);
        this.generateEntry(
            "TODO", 
            "https://upload.wikimedia.org/wikipedia/en/d/d6/Image_coming_soon.png",
            "",
            this.lorem_ipsum);
        //this.generateEntry("General Kenobi");
    }

    generateEntry(display_name, image_url, link_url){
        var entry_main_container = document.createElement("div");
        entry_main_container.className = "entry_main_container";

        var entry_image_wrapper = document.createElement("div");
        entry_image_wrapper.className = "entry_image_wrapper";
        entry_main_container.appendChild(entry_image_wrapper);
        
        var image = document.createElement("img");
        image.src=image_url;
        image.className = "entry_img";        
        entry_image_wrapper.appendChild(image);

        var entry_text_wrapper = document.createElement("div");
        entry_text_wrapper.className = "entry_text_wrapper";
        entry_main_container.appendChild(entry_text_wrapper);

        var link = document.createElement("a");
        link.className = "link";
        link.href = link_url;
        link.innerText = display_name;
        entry_text_wrapper.appendChild(link);

        var node_description = document.createElement("div");
        node_description.className = "description";
        node_description.innerText = this.lorem_ipsum;
        entry_text_wrapper.appendChild(node_description);


        this.element.appendChild(entry_main_container);
    }
}

module.exports = ContentManager;
},{}],2:[function(require,module,exports){

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
},{"./content_manager":1}]},{},[2]);
