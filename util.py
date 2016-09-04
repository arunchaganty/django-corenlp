"""
Utilities to annotate documents with Stanza
"""

from stanza.nlp.corenlp import CoreNLPClient, AnnotationException
from . import settings

def annotate_document(doc_gloss):
    """
    Annotate a document using the CoreNLPClient
    :param doc_gloss Gloss of the document to parse.
    :returns A list of Sentences and Mentions
    """
    client = CoreNLPClient(settings.ANNOTATOR_ENDPOINT)
    document = client.annotate(doc_gloss, settings.DEFAULT_ANNOTATORS)

    return [], []

