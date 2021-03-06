/**
 * Created by 1ka on 3/28/14.
 */
var ZOOMPYCDB = ZOOMPYCDB||{};
//создание пространства имен
ZOOMPYCDB.namespace = function (ns_string) {
    var parts = ns_string.split('.'),
        parent = ZOOMPYCDB,
        i;
    if (parts[0] === "ZOOMPYCDB") {
        parts = parts.slice(1);
    }
    for (i = 0; i < parts.length; i += 1) {
        if (typeof parent[parts[i]] === "undefined") {
            parent[parts[i]] = {};
        }
        parent = parent[parts[i]];
    }
    return parent;
};
ZOOMPYCDB.test;
ZOOMPYCDB.serveradr = function(){
	return "http://0.0.0.0:8082/";
};
$(document).ready(function(){
    var storage = ZOOMPYCDB.Storage(),
        cookies = ZOOMPYCDB.Cookies(),
        temp_data = ZOOMPYCDB.TempData(cookies),
        graph_view = ZOOMPYCDB.NavigationGraph(storage,{
            "canvas": d3.select("#graph_map"),
            "body": d3.select("body")
        }),
        logger = ZOOMPYCDB.Logger({},{
            "message": $("#error_message")
        }),
        keyboard = ZOOMPYCDB.Keyboard({},{}),
        graph_controller = ZOOMPYCDB.NGController({
            "storage": storage,
            "temp": temp_data
        },{
            "graph":graph_view,
            "keyboard": keyboard
        });
});
