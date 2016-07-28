"""
Utilities to annotate documents with Stanza
"""

from stanza.nlp.corenlp import CoreNLPClient, AnnotationException
from . import settings

CORENLP_CLIENT = CoreNLPClient(settings.ANNOTATOR_ENDPOINT)

def annotate_document(doc_gloss):
    """
    Annotate a document using the CoreNLPClient
    """
    return CORENLP_CLIENT.annotate(doc_gloss, settings.DEFAULT_ANNOTATORS)

