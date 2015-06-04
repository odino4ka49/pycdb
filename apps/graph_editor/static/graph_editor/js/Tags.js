ZOOMPYCDB.namespace("ZOOMPYCDB.Tags");
ZOOMPYCDB.Tags = function(model,elements){
	var tag_data,
		storage = model.storage,
		temp_data = model.temp,
		panel = elements.panel,
		list = panel.select("#tags"),//.first(),
		chosen_list = panel.select("#chosen_tags"),//.first(),
	
	
	checkTag = function(id){
		$(document).trigger("tag_added",id);
	},
	refreshChosenTags = function(){
		var chosen_tags_data = temp_data.getChosenTags(),
			chosen_tags = chosen_list.selectAll("li").data(chosen_tags_data);
        chosen_tags.enter()
            	.append("li")
            	.on("click",function(d){$(document).trigger("chosen_tag_removed",d.id);});
        chosen_tags.text(function(d){return d.title;});
        chosen_tags.exit().remove();
		/*chosen_list.empty();
		for(var i=0;i<tags.length;i++){
            var d = tags[i],
            	li = $("<li>"+d.title+"</li>");//.click(function(){$(document).trigger("chosen_tag_removed",d.id);});
            chosen_list.append(li);
       };*/
	},
	setTagInfo = function(){
		//$("<li>hi</li>").appendTo(panel);
		var tags = list.selectAll("a").data(tag_data);
        tags.enter()
            	//.append("li")
            	.append("a")
            	.attr("href", "javascript:void(0);")
            	.on("click",function(d){checkTag(d.id);});
        tags.text(function(d){return d.title;});
        tags.exit().remove();
		/*for(var i=0;i<tag_data.length;i++){
            var d = tag_data[i],
            	a = $("<a href='javascript:void(0);'>"+d.title+"</a>").click(function(){checkTag(d.id);});
            $("<li></li>").appendTo(list).append(a);
       }*/
        try {
          TagCanvas.Start('tagsCanvas','tags',{
            textColour: '#ff00ff',
            outlineColour: '#ff00ff',
            reverse: true,
            depth: 0.8,
            maxSpeed: 0.05
          });
        } catch(e) {
          // something went wrong, hide the canvas container
          document.getElementById('myCanvasContainer').style.display = 'none';
        }
    },
    
    loadTagInfo = function(){
    	/*var filter = function(s){
   			if(s.cid==149) alert("umm");
   			return s.cid==149;
   		};*/
   		tag_data = storage.getTags();
    },
    clean = function(){
    	list.empty();
    };
       
    $(document).on("graph_changed",function(){
    	//clean();
    	loadTagInfo();
   		setTagInfo();
    });
    $(document).on("chosen_tags_list_changed",function(){
    	refreshChosenTags();
    });
    
   return{
   };
       
};