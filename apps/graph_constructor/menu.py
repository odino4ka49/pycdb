__author__ = '1ka'
from django.core.urlresolvers import reverse

MENU_ITEMS = [
              {
                    "title" : "Graph Constructor",
                    "url" : reverse("constructor-index")
              },
]