__author__ = '1ka'
import random,sys
from django.http import HttpResponse
from graph_constructor.utils.decorators import JsonResponse
from portal.utils.array_helpers import getFirstOrNone
from annoying.decorators import render_to
from string import maketrans
from django.db.models import Q
import json
import sys

@render_to("graph_constructor/index.html")
def index(request):
    conf = request.configuration
    return {}


def configData(request):
    classes_list = []
    relations_list = []

    entities = []
    entities = request.configuration.getAllEntities("template")
    for entity in entities:
        display_attrs = entity.getNeighbours("attributes",isInThisView)[0]
        classes_list += [{
                "id": "object",
                "title": entity["name"],
                "shape": display_attrs["shape"],
                "color": display_attrs["color"],
                "size": display_attrs["size"],
                "image": display_attrs["image"],
                "scale": display_attrs["scale"],
            }]
    entities = request.configuration.getAllEntities("socket_type")
    for entity in entities:
        display_attrs = entity.getNeighbours("attributes",isInThisView)[0] #getNeighboursTo("instanceof")[0]
        classes_list += [{
                "id": "socket",
                "title": entity["name"],
                "shape": display_attrs["shape"],
                "color": display_attrs["color"],
                "size": display_attrs["size"],
                "image": display_attrs["image"],
                "scale": display_attrs["scale"],
            }]
    entities = request.configuration.getAllEntities("pin_type")
    for entity in entities:
        classes_list += [{
                "id": "pin",
                "title": entity["name"],
                "shape": "cross",
                "color": "white",
                "size": "4",
                "image": "",
                "scale": 9
            }]
    """entities = request.configuration.getAllEntities("pin_type")
    for entity in entities:
        classes_list += [{
                "id": entity["id"],
                "title": entity["name"],
                "shape": "square",
                "color": "black",
                "size": "2",
                "image": "",
                "scale": 0
            }]"""
        
    relations = request.configuration.getAllEntities("link_type")
    for relation in relations:
        allowed_from = []
        allowed_to = []
        sockets = relation.getNeighbours("to_link")
        for obj in sockets:
            allowed_to.append(obj["id"])
        sockets = relation.getNeighbours("from_link")
        for obj in sockets:
            allowed_from.append(obj["id"])
        relations_list += [{
            "id": "link",
            "title": relation["name"],
            "shape": "stroke",
            #"x": cls_model_info.x,
            #"y": cls_model_info.y,
            "color": "black",
            "size": 1,
            "allowed_relations": {"to":allowed_to,"from":allowed_from}
        }]
    return JsonResponse({"nodes":classes_list,"rels":relations_list})

def templateData(request):
    templatedata = []
    
    obj_types = []
    obj_types = request.configuration.getAllEntities("object_type")
    for ot in obj_types:
        template_list = []
        templates = ot.getNeighboursFrom("instanceof")
        for temp in templates:
            template_list += [{
                "name": temp["readable_name"],
                #socket and pin data
            }]
        templatedata += [{
            "name": ot["readable_name"],
            "children": template_list
        }]
    return JsonResponse({"name": "Templates", "children": templatedata})

def isInThisView(obj):
    try:
        view_id = obj.getNeighboursTo("logical")[0]["name"]
        if(view_id == "basic"):
            return True
        else:
            return False
    except Exception:
        return False

def getGraphData(request):
    data = request.GET
    nodes_list = []
    relations_list = []
    backgrounds_list = []
    entities = []

    #loading objects    
    entities = request.configuration.getAllEntities("object")
    for en in entities:
        object_type = en.getNeighboursTo("instanceof")[0]
        display_attrs = object_type.getNeighbours("attributes",isInThisView)[0]
        obj_coords = en.getNeighbours("attributes",isInThisView)[0]
        socket_list = []
        pin_list = []
        #loading sockets
        sockets = en.getNeighboursTo("composition")
        for sc in sockets:
            template_socket = sc.getNeighboursTo("instanceof")[0]
            socket_type = template_socket.getNeighboursTo("instanceof")[0]
            sc_display_attrs = socket_type.getNeighbours("attributes",isInThisView)[0]
            sc_coords = template_socket.getNeighbours("attributes",isInThisView)[0]
            sc_x = int(obj_coords["x"])+int(sc_coords["x"])-int(display_attrs["size"])/2
            sc_y = int(obj_coords["y"])+int(sc_coords["y"])-int(display_attrs["size"])/2
            sc_size = int(sc_display_attrs["size"])
            #loading pins
            pins = sc.getNeighboursTo("instanceof")[0].getNeighboursTo("composition")
            pin_type = pins[0].getNeighboursTo("instanceof")[0]
            i = 0
            for pin in pins:
                pin_list += [{
                    "id": pin["id"],
                    "cid": "pin",
                    "title": pin["name"],
                    "x": sc_x,
                    "y": sc_y-sc_size/2+sc_size*i/(len(pins)-1),
                    "shape": "square",
                    "color": "white",
                    "size": 1,
                    "image": "",
                    "scale": 9
                }]
                i += 1
            socket_list += [{
                "id": sc["id"],
                "cid": "socket",
                "title": "",#sc["readable_name"],
                "x": sc_x,
                "y": sc_y,
                "shape": sc_display_attrs["shape"],
                "color": sc_display_attrs["color"],
                "size": sc_size,
                "image": sc_display_attrs["image"],
                "scale": sc_display_attrs["scale"],
                "children": pin_list
            }]
        nodes_list += [{
            "id": en["id"],
            "cid": "object",
            "title": en["readable_name"],
            "x": int(obj_coords["x"]),
            "y": int(obj_coords["y"]),
            "shape": display_attrs["shape"],
            "color": display_attrs["color"],
            "size": int(display_attrs["size"]),
            "image": display_attrs["image"],
            "scale": display_attrs["scale"],
            "children": socket_list
        }]
        
    #loading socket relations
    relations = request.configuration.getAllEntities("link")
    for rel in relations:
        from_ent = rel.getNeighbours("from_link")[0]["id"]
        to_ent = rel.getNeighbours("to_link")[0]["id"]
        relations_list += [{
            "id": rel["id"],
            "source": ["socket",from_ent],
            "target": ["socket",to_ent],
            "cid": "link",
            "name": "",
        }]
        """relations = request.configuration.getAllRelations(en,None,None,True,"to")
        for rel in relations:
            rel_name = ""
            if 'name' in rel: rel_name = rel["name"]
            for node in nodes_list:
                to_ent = rel.getToEntity().getId()
                if to_ent[0]==node["cid"] and to_ent[1]==node["id"]:
                    relations_list += [{
                        "id": rel.getId()[1],
                        "source": rel.getFromEntity().getId(),
                        "target": to_ent,
                        "cid": rel.getId()[0],
                        "name":rel_name,
                    }]
    backgrounds = Background.objects.filter(config=configuration,view=the_view)
    for bg in backgrounds:
        backgrounds_list += [{
            "id": bg.id,
            "x": bg.x,
            "y": bg.y,
            "width": bg.width,
            "height": bg.height,
            "image": bg.image,
            "z": bg.z
        }]"""
    return JsonResponse({'nodes':nodes_list,'rels':relations_list,'bgs':backgrounds_list})



def saveGraph(request):
    data = request.GET
    nodes = json.loads(data["nodes"])
#    the_view = None if (view_id=="") else View.objects.get(id=view_id)
#    entities = request.configuration.getAllEntities("object")
    for node in nodes:
        #work with object
        obj = request.configuration.loadEntity(str(node["cid"]),node["id"])
        obj_coords = obj.getNeighbours("attributes",isInThisView)[0]
        obj_coords["x"] = node["x"]
        obj_coords["y"] = node["y"]
        obj_coords.save()
        print >>sys.stdout, obj_coords
    return HttpResponse(0)
