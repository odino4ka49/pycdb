# -*- coding: UTF-8 -*-
__author__ = 'alexmak'
from settings_common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG



# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_SITE_ROOT_URL = "http://localhost:8082"
EMAIL_FROM = "pce.dev@gmail.com"

CONFIGURATIONS = {
    "tst_config": ConfigurationInfo("Test Configuration", "graph_dbs.configurations.test_config.TestConfig", BASE_DIR + "/graph_dbs/data/nxgraph.gpickle"),
    "tst_construct": ConfigurationInfo("Test Constructor", "graph_dbs.configurations.test_constructor.TestConstructor", BASE_DIR + "/graph_dbs/data/tst_construct.gpickle"),
    "nsls2_magnets": ConfigurationInfo("NSLS 2 - Magnets configuration", "graph_dbs.configurations.nsls2_magnets.NSLS2Magnets", BASE_DIR + "/graph_dbs/data/nsls2_magnets.gpickle"),
    "nsls2_magnets_test": ConfigurationInfo("Test NSLS 2 - Magnets configuration", "graph_dbs.configurations.nsls2_magnets.NSLS2Magnets", BASE_DIR + "/graph_dbs/data/nsls2_magnets_test.gpickle"),
    "vepp4_k500" : ConfigurationInfo("VEPP4 - K500", "graph_dbs.configurations.vepp4_k500.VEPP4K500", BASE_DIR + "/graph_dbs/data/k500.gpickle"),
    "cxv2_config": ConfigurationInfo("CXV2 ", "graph_dbs.configurations.cxv2_config.CXV2Config", BASE_DIR + "/graph_dbs/data/cxv2_config.gpickle"),
}

INSTALLED_APPS += [
    'std_editor',
    'cxv2_tools',
    'nsls_tools',
    'pasha_app',
]

MENU_SOURCES += ["nsls_tools.menu.MENU_ITEMS", "std_editor.menu.MENU_ITEMS",  "cxv2_tools.menu.MENU_ITEMS", "graph_editor.menu.MENU_ITEMS", "graph_constructor.menu.MENU_ITEMS"]
