"""
Utilities to annotate documents with Stanza
"""

from django.db import transaction
from .models import Sentence, Mention
from . import settings

def span_overlap(span1, span2):
    return not ((span1[1] < span2[0]) or (span2[1] < span1[0]))

def span_match(span1, span2):
    return span1 == span2

def span_contains(span1, span2):
    return (span2[0] >= span1[0]) and (span2[1] <= span1[1])

def annotate_document(doc,
                      client,
                      sentence_filter=lambda xs:xs,
                      mention_filter=lambda xs:xs):
    """
    Annotate a document using the CoreNLPClient
    :param doc Document to parse.
    :param sentence_filter -- a post-processor that filters sentences returned by the annotator
    :param mention_filter -- a post-processor that filters mentions returned by the annotator
    :returns A list of Sentences and Mentions
    """
    ann = client.annotate(doc.gloss, settings.DEFAULT_ANNOTATORS)

    with transaction.atomic():
        # Create django objects
        sentences = sentence_filter(ann.sentences)
        mentions = mention_filter([m for m in ann.mentions if m.sentence in sentences])

        sentences = [Sentence.from_stanza(doc, i, s) for i, s in enumerate(sentences)]
        sentences = Sentence.objects.bulk_create(sentences)
        # Note: setting ids is only supported with django 1.10 and with
        # postgres
        assert sentences[0].id is not None, "Ids have not been created. Are you using Django 1.10 with postgres?"

        # First, insert all mentions to get ids.
        mentions = {m: Mention.from_stanza(doc, sentences[m.sentence.sentenceIndex], m) for m in mentions}
        Mention.objects.bulk_create(mentions.values())

        # Set the canonical mention and parent mention ids
        for mention, db_mention in mentions.items():
            db_mention.canonical_mention = mentions[mention.canonical_entity]

            for parent_mention in (db_mention_ for _, db_mention_ in mentions.items() if not db_mention_.character_span == db_mention.character_span and span_contains(db_mention_.character_span, db_mention.character_span)):
                mention.parent_mention = parent_mention
                break
            db_mention.save()

    return sentences, mentions

