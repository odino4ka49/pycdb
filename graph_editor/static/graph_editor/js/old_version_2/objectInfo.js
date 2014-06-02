function ObjectInfo(){}ObjectInfo.prototype.setSearchWidget = function(data){    $('#search').append(data);    $("#ui-id-1").on("click",function(d){        var cid = $("#search_string_cid").val();        var id = $("#search_string_id").val();        $(document).trigger("object_found",[cid,id]);        $(document).trigger("zoomto",[cid,id]);        //zoomTo(cid,id);        //selectObject(cid,id);    });}ObjectInfo.prototype.setConfigData = function(data){    this.graph_configuration_data = data;}ObjectInfo.prototype.selectObject = function(selected_object){    this.object = selected_object;    this.relation = undefined;    var frm = $("obj_node_info");    $("#obj_node_info").removeClass("hidden");    $("#search_neighbors").removeClass("hidden");    $("#obj_rel_info").addClass("hidden");    var config_data = this.graph_configuration_data;    $.each(selected_object, function(key, value){        var $ctrl = $('[name='+key+']');        if($ctrl[0]!=undefined){            switch($ctrl[0].type)            {                case "number":                case "text":                case "list":                    $ctrl.val(value);                    break;                case "color":                    var color = value;                    if(color == "default"){                        $("input[name='color_default']").prop('checked',true);                        $("input[name='color']").attr("disabled",true);                        if(config_data!=undefined)                            color = $.grep(config_data[0], function(e){ return (e.id == selected_object.cid); })[0].color;                    }                    else{                        $("input[name='color_default']").prop('checked',false);                        $("input[name='color']").attr("disabled",false);                    }                    $ctrl[0].value=color;                    break;                case "checkbox":                    /*$ctrl.each(function(){                        if($(this).attr('value') == value) {  $(this).attr("checked",value); }                    });*/                    break;            }        }    });};ObjectInfo.prototype.selectRelation = function(object){    this.object = undefined;    this.relation = object;    $("#obj_node_info").addClass("hidden");    $("#search_neighbors").addClass("hidden");    $("#obj_rel_info").removeClass("hidden");};ObjectInfo.prototype.setObjectConfigData = function(fields,vals,protos,protos_vals){    $("#obj_attrs div").remove();    this.fields = fields;    this.protos_vals = protos_vals;    this.protos = protos;    $.each(fields,        function(i,key){            var checked = protos[key]? "checked":"";            $('#obj_attrs').append(                $("<div>"+key+": <input type='checkbox' onclick=checkDefaultPair('"+key+"') name='"+key+"_default'"+checked+"><input type='"+key+"' name='"+key+"' value="+vals[i]+"></div>")            );            checkDefaultPair(key);        })}ObjectInfo.prototype.setRelationConfigData = function(fields,vals){    $("#obj_config_info div div").remove();    this.fields = fields;    this.protos_vals = undefined;    this.protos = undefined;    $.each(fields,        function(i,key){            $('#obj_config_info div').append(                $("<div>"+key+": <input type='"+key+"' name='"+key+"' value="+vals[i]+"></div>")            );        })}ObjectInfo.prototype.saveObject = function(){    if(this.object==undefined)        return;    if(!$("input[name='color_default']").is(":checked")){        this.object.color=$("input[name='color']").val();    }    else{        this.object.color = "default";    }    this.object.size=$("input[name='size']").val();    this.object.shape=$("input[name='shape']").val();    this.object.title=$("input[name='name']").val();    return this.object;}ObjectInfo.prototype.getRelationAttrs = function(){    var rel = new Object();    rel.id = this.relation.id;    rel.cid = this.relation.cid;    for(var i=0;i<this.fields.length;i++){        rel[this.fields[i]] = $("#obj_config_info input[name="+this.fields[i]+"]").val();    }    return rel;}ObjectInfo.prototype.getObjectAttributes = function(){    var attr = new Object();    for(var i=0;i<this.fields.length;i++){        var key = this.fields[i];        if($("input[name='"+key+"_default'").is(":checked")){            attr[key] = "default";        }        else{            attr[key] = $("input[name='"+key+"'").val();        }    }    return attr;}ObjectInfo.prototype.setDefaultValue = function(pairname){    var proto;    if(pairname==="color"){        proto = this.object;        if((this.graph_configuration_data!=undefined)&&(proto!=undefined)){            var color = $.grep(this.graph_configuration_data[0], function(e){ return (e.id == proto.cid); })[0].color;            $("input[name='color']")[0].value = color;        }    }    else{        proto = this.protos_vals[pairname];        $("input[name='"+pairname+"'").val(proto);    }}ObjectInfo.prototype.deleteNode = function(){    if(this.object!=undefined)        $(document).trigger("delete_node",this.object);}ObjectInfo.prototype.deleteRelation = function(){    if(this.relation!=undefined)        $(document).trigger("delete_rel",this.relation);}function deleteTheNode(){    $(document).trigger("objinfo_delete_node");}function saveNode(){    $(document).trigger("save_node");}function findNeighbors(){    $(document).trigger("find_neighbors",$("#neighbor_number").val());}function deleteRel(){    $(document).trigger("objinfo_delete_rel");}function saveRel(){    $(document).trigger("save_rel");}function checkDefaultPair(pair){    if($("input[name='"+pair+"_default'").is(":checked")){        $("input[name='"+pair+"']").attr("disabled",true);        $(document).trigger("set_default_value",pair);    }    else{        $("input[name='"+pair+"']").attr("disabled",false);    }}