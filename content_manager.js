
class ContentManager{

    
    constructor(){
        this.lorem_ipsum = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.";
    
        this.element = document.getElementById("grid_item_content");

        this.generateEntry(
            "3-Torus FlowVis Tool", 
            "https://sfb-trr191.github.io/3-torus-flowvis-tool-tutorial/images/test_main.png",
            "3-torus-flowvis-tool.html",
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

    generateEntry(display_name, image_url, link_url, description){
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
        node_description.innerText = description;
        entry_text_wrapper.appendChild(node_description);


        this.element.appendChild(entry_main_container);
    }
}

module.exports = ContentManager;