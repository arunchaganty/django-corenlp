"""
Utilities to annotate documents with Stanza
"""

from stanza.nlp.corenlp import CoreNLPClient, AnnotationException
from . import settings

CORENLP_CLIENT = CoreNLPClient(settings.ANNOTATOR_ENDPOINT)

def annotate_document(doc_gloss):
    """
    Annotate a document using the CoreNLPClient
    :param doc_gloss Gloss of the document to parse.
    :returns A list of Sentences and Mentions
    """
    document = CORENLP_CLIENT.annotate(doc_gloss, settings.DEFAULT_ANNOTATORS)

    return [], []

