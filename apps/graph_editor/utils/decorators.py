from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.db.models import signals as signalmodule
from django.http import HttpResponse
import json as simplejson


class JsonResponse(HttpResponse):

    def __init__(self, data):
        super(JsonResponse, self).__init__(content=simplejson.dumps(data), content_type='application/json')

