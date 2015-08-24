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
                "id": entity["id"],
                "title": entity["name"],
                "shape": display_attrs["shape"],
                "color": display_attrs["color"],
                "size": display_attrs["size"],
                "image": display_attrs["image"]
                #"scale": cls_model_info.scale
            }]
    entities = request.configuration.getAllEntities("template_socket")
    for entity in entities:
        display_attrs = entity.getNeighboursTo("instanceof")[0].getNeighbours("attributes",isInThisView)[0]
        classes_list += [{
                "id": entity["id"],
                "title": entity["name"],
                "shape": display_attrs["shape"],
                "color": display_attrs["color"],
                "size": display_attrs["size"],
                "image": display_attrs["image"]
                #"scale": cls_model_info.scale
            }]
    entities = request.configuration.getAllEntities("pin_type")
    for entity in entities:
        classes_list += [{
                "id": entity["id"],
                "title": entity["name"],
                "shape": "square",
                "color": "black",
                "size": "2",
                "image": "",
                #"scale": cls_model_info.scale
            }]
    entities = request.configuration.getAllEntities("pin_type")
    for entity in entities:
        classes_list += [{
                "id": entity["id"],
                "title": entity["name"],
                "shape": "square",
                "color": "black",
                "size": "2",
                "image": "",
                #"scale": cls_model_info.scale
            }]
    
    """        relations_list += [{
                "id": cls_id,
                "title": cls_info["name"],
                "description": cls_info["description"],
                "shape": cls_model_info.shape,
                "x": cls_model_info.x,
                "y": cls_model_info.y,
                "color": cls_model_info.color,
                "size": cls_model_info.size,
                "allowed_relations": filterTagRelations(cls_info["allowed_relations"])
            }]"""
    return JsonResponse({"nodes":classes_list,"rels":relations_list})

def isInThisView(obj):
    try:
        view_id = obj.getNeighboursTo("logical")[0]["name"]
        if(view_id == "basic"):
            return True
        else:
            return False
    except Exception:
        return False

def getEntityAttributes(entity):
    cid = int(cid)
    id = int(id)
    attr_list = []
    attr_data_list = []
    class_info = request.configuration.classes[cid]
    entity = request.configuration.loadEntity(cid, id)
    protos = {}
    protos_values = {}
    types = []

    for attr in class_info["attributes"]:
        key = attr["name"]
        attr_list.append(key)
        attr_data_list.append(entity[key])
        types.append(attr["data_type"])
        protos[key] = key not in entity
        protos_values[key] = entity.get_default_attribute_value(key)

    return JsonResponse({
        "fields": attr_list,
        "vals": attr_data_list,
        "types": types,
        "protos": protos,
        "proto_vals": protos_values
    })
