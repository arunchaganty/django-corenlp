#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings specific to django-corenlp
"""

# Should django-corenlp create new tables or use existing ones?
MANAGE_TABLES = True
# Should django-corenlp use the 'corenlp_' prefix on tables?
USE_TABLENAME_PREFIX = True

# This flag determines the Stanford CoreNLP server endpoint to use.
# For now, we assume that you are hosting your own annotation server on
# your machine, but you might prefer using http://corenlp.ai as a hosted
# service.
ANNOTATOR_ENDPOINT = "localhost:8001"
API_USER = ""
API_KEY = ""

# TODO: include "mentions" when the server supports them.
DEFAULT_ANNOTATORS = ["tokenize", "ssplit", "lemma", "pos", "ner", "dep"]

