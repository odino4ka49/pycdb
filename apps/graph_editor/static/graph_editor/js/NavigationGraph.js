ZOOMPYCDB.namespace("ZOOMPYCDB.NavigationGraph");
ZOOMPYCDB.NavigationGraph = function(model,elements){
    var model = model,
        canvas = elements.canvas,
        body = elements.body,
        ismouseover = false,
        mouse_coord = {"x": 0,"y":0},
        scale,
        zoom,
        drag,
        dragback,
        rectdrag,
        svg,
        force,
        container,
        dragline,
        dragline_coord,
        selection_rect,
        sel_start,
        last_mouse_pos,
        lines_path,
        nodes_path,
        background_image,
        zscale,
        cc,
        svg_group,
        graph_data,
        config_data,
        force_graph,
        
        initialize = function(){
        	graph_data = model.getForceGraph();
        	config_data = model.getConfigData();
        	force_graph = jQuery.extend(true,{},graph_data);
        	force_graph.nodes = graph_data.nodes;
		    force_graph.rels = graph_data.rels;
        	refresh();
        	//graph_data.rels = jQuery.extend(true,[],force_graph.rels);
        	ZOOMPYCDB.test = graph_data;
        },
        
        refresh = function (){
        	var lines,
        		nodes,
        		type,
		        force = d3.layout.force()
				    .charge(function(d) { return -120; })
				    .linkDistance(function(d) { return Math.max(d.target.size,d.source.size); })
				    .gravity(0.1);
        	if(graph_data===undefined) return;
	    	force.nodes(force_graph.nodes)
	        	.links(force_graph.rels)
	        	.start();

	        lines = lines_path.selectAll("line")
		        .data(force_graph.rels);
		 
		   // Enter any new links
		    lines.enter().append("line");
		    lines.attr("style",function(d){
                    type = config_data.rels.filter(function(r){return r.id === d.cid;})[0];
                    if(d.selected==2)
                        return "stroke:lightgrey;stroke-width:1;fill:none";
                    else
                        return "stroke:"+ type.color+";fill:none;stroke-width:"+ 1+";fill:none";
                })
                .attr("class", function(d) {
                    type = config_data.rels.filter(function(r){return r.id === d.cid;})[0];
                    return type.shape;
                })
		        .attr("x1", function(d) { return d.source.x; })
		        .attr("y1", function(d) { return d.source.y; })
		        .attr("x2", function(d) { return d.target.x; })
		        .attr("y2", function(d) { return d.target.y; });
		        
		    // Exit any old links.
		    lines.exit().remove();

			nodes = nodes_path.selectAll(".node")
		      	.data(force_graph.nodes);
		    nodes.enter().append("path")
		      .attr("class", "node");
            nodes.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
		      .attr("d", d3.svg.symbol()
                .size(function(d) { return d.size* d.size; })
                .type(function(d) {
                    var default_node = config_data.nodes.filter(function (e) { return e.id === d.cid;})[0];
                    if(d.image||(default_node.image&& d.shape=="default"))
                        return "square";
                    else if(d.shape=="default"){
                        return default_node.shape;
                    }
                    return d.shape;
                }))
                .attr("fill",function(d){
                    var default_node = config_data.nodes.filter(function (e) { return e.id === d.cid;})[0];
                    if(d.image||(default_node.image&& d.shape=="default"))
                        return "white";
                    else if(d.color=="default")
                        return default_node.color;
                    return d.color;
                });
		      
		    nodes.exit().remove();
		    
		    var nodes_img = nodes_path.selectAll("image").data(force_graph.nodes);
            nodes_img.enter().append("image");
            nodes_img
		      .call(force.drag)
		      .on("dblclick",function(d){
		            d.isCurrentlyFocused = !d.isCurrentlyFocused;
		            if(d.isCurrentlyFocused) d.size=d.size*2;
		            else d.size = d.size/2;
		            filterGraph();
					refresh();
		        })
		        .attr("xlink:href",function(d){
                    var default_node = config_data.nodes.filter(function (e) { return e.id === d.cid;})[0];
                    if(d.image)
                        return d.image;
                    else if(default_node.image&& d.shape=="default")
                        return default_node.image;
                    else
                        return "";
                })
                //.attr("transform", function(d) { return "translate(" + (d.x- d.size/2) + "," + (d.y- d.size/2) + ")"; })
                .attr("width",function(d) { return d.size;})
                .attr("height",function(d) {return d.size;})
                .attr("class",function(d){
                    if(d.selected==2)
                        return "grey";
                    else if(d.inselection)
                        return "inselection";
                    else if(d.chosen)
                        return "chosen";
                    else
                        return null;
                });
            nodes_img.exit().remove();
		    
		    texts = nodes_path.selectAll("text")
               .data(force_graph.nodes);
            texts.enter()
               .append("text")
               .attr("class","nodetext")
               .attr("font-family", "sans-serif")
               .attr("fill", "black")
               //.attr("x", function(d) {return d.x+ d.size/2;})
               //.attr("y", function(d) {return d.y- d.size/2;})
               .text(function(d){return d.title;});
            texts.exit().remove();
		    
		    force.on("tick", function() {
		    	var height = svg[0][0].clientHeight,
		    		width = svg[0][0].clientWidth;
		    		
		    	force.size([width,height]);
			    lines.attr("x1", function(d) { return d.source.x; })
			        .attr("y1", function(d) { return d.source.y; })
			        .attr("x2", function(d) { return d.target.x; })
			        .attr("y2", function(d) { return d.target.y; });
			
			    //nodes.attr("cx", function(d) { return d.x; })
    		    	//.attr("cy", function(d) { return d.y; });
    		    nodes.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
    		   	nodes_img.attr("transform", function(d) { return "translate(" + (d.x- d.size/2) + "," + (d.y- d.size/2) + ")"; });
    		   	
    		    texts
	                .attr("x", function(d) {return d.x+ d.size/2;})
	                .attr("y", function(d) {return d.y- d.size/2;});
    		  });
        },
        
        filterGraph = function(){
        	var newNodes = [];
		    var newLinks = [];
		
		    for (var i = 0; i < graph_data.rels.length ; i++) {
		        var link = graph_data.rels[i];
		        if (link.target.isCurrentlyFocused || link.source.isCurrentlyFocused) {
		            newLinks.push(link);
		            addNodeIfNotThere(link.source,newNodes);
		            addNodeIfNotThere(link.target,newNodes);
		        }
		    }
		    // if none are selected reinstate the whole dataset
		    if (newNodes.length > 0) {
		        force_graph.rels = newLinks;
		        force_graph.nodes = newNodes;
		    }
		    else {
		        force_graph.nodes = graph_data.nodes;
		        force_graph.rels = graph_data.rels;
		    }
		    
		    function addNodeIfNotThere( node, nodes) {
		        for ( var i=0; i < nodes.length; i++) {
		            if ((nodes[i].id == node.id) && (nodes[i].cid == node.cid)) return i;
		        }
		        return nodes.push(node) -1;
		    }
        },
        
        zoomed = function(){
            scale = d3.event.scale;
            container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
        };
        
        zoom = d3.behavior.zoom()
	        .scaleExtent([0.1, 60])
	        .on("zoom", zoomed);
        scale = 1;
        svg = canvas.call(zoom)
	        .on("dblclick.zoom", null);
        container = svg.append("g");
    lines_path = container.append("g");
    nodes_path = container.append("g");
    
    $(document).on("graph_changed",function(){
        initialize();
    });
     
    return{
    };
};