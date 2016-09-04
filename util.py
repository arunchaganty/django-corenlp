"""
Utilities to annotate documents with Stanza
"""

from django.db import transaction
from stanza.nlp.corenlp import CoreNLPClient, AnnotationException
from .models import Sentence, Mention
from . import settings

def annotate_document(doc):
    """
    Annotate a document using the CoreNLPClient
    :param doc Document to parse.
    :returns A list of Sentences and Mentions
    """
    client = CoreNLPClient(settings.ANNOTATOR_ENDPOINT)
    document = client.annotate(doc.gloss, settings.DEFAULT_ANNOTATORS)

    with transaction.atomic():
        # Create django objects
        sentences = [Sentence.from_stanza(doc, i, s) for i, s in enumerate(document)]
        Sentence.objects.bulk_create(sentences)
        mentions = [Mention.from_stanza(doc, sentences[m.sentence.sentenceIndex], m) for m in document.mentions]
        Mention.objects.bulk_create(mentions)

    return sentences, mentions

