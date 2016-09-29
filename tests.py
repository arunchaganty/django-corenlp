from django.test import TestCase
import stanza.nlp.CoreNLP_pb2 as proto
from stanza.nlp.corenlp import AnnotatedDocument
from .util import annotate_document
from .models import Document
from datetime import datetime
import ipdb

import os

TEST_DATA = os.path.join(os.path.dirname(__file__), 'test-data')

class MockCoreNLPClient(object):
    def __init__(self, doc, return_value):
        self.doc = doc
        self.return_value = return_value

    def annotate(self, *args):
        return self.return_value

def is_unique(collection):
    elements = set([])
    for item in collection:
        if item in elements: return False
        else: elements.add(item)
    return True

class CoreNLPTestCase(TestCase):
    """
    doc:
    [Barack Hussein Obama] is an [American] politician who is the [44th] and
    [current] President of [the [United States]]. He is the [first] [African
    American] to hold the office and the [first] president born outside [the
    continental United States]. Born in [Honolulu], [Hawaii], [Obama] is a
    graduate of [Columbia University] and [Harvard Law School], where he was
    president of the [Harvard Law Review].
    """
    @classmethod
    def setUpClass(cls, *args):
        with open(os.path.join(TEST_DATA, "doc.txt"), "r") as f:
            doc_txt = f.read()
        with open(os.path.join(TEST_DATA, "doc.pb"), "rb") as f:
            pb = proto.Document()
            pb.ParseFromString(f.read())
            ann = AnnotatedDocument.from_pb(pb)

        cls._doc = Document(id="test",
                            corpus_id="test",
                            created=datetime.now(),
                            date=datetime.now(),
                            title="test",
                            gloss=doc_txt,
                            metadata="")
        cls._doc.save()
        cls._ann = ann
        cls._client = MockCoreNLPClient(cls._doc, cls._ann)
        super(CoreNLPTestCase, cls).setUpClass(*args)

    def test_annotate(self):
        """
        Verify that, after processing the annotated document,
            the mentions should correctly identify:
        """
        sentences, mentions = annotate_document(self._doc, self._client)
        # Just assert counts.
        self.assertEqual(3, len(sentences))
        self.assertEqual(21, len(mentions))

        m_he = mentions[0]
        m_barack = mentions[6]

        self.assertEqual(sentences[0], m_barack.sentence)
        self.assertEqual(sentences[1], m_he.sentence)

    def test_annotate_glosses(self):
        _, mentions = annotate_document(self._doc, self._client)
        m_he = mentions[0]
        m_barack = mentions[6]


        # gloss and character offsets
        self.assertEqual("He", m_he.gloss)
        self.assertEqual(self._doc.gloss.__getitem__(slice(*m_he.character_span)), m_he.gloss)
        self.assertEqual((107,109), m_he.character_span)

        self.assertEqual("Barack Hussein Obama", m_barack.gloss)
        self.assertEqual(self._doc.gloss.__getitem__(slice(*m_barack.character_span)), m_barack.gloss)
        self.assertEqual((0,20), m_barack.character_span)

    def test_annotate_canonical_mentions(self):
        _, mentions = annotate_document(self._doc, self._client)
        m_he = mentions[0]
        m_barack = mentions[6]

        # Verify that canonical_mentions functions correctly.
        self.assertEqual(m_barack, m_he.canonical_mention)
        self.assertEqual(m_barack, m_barack.canonical_mention)

    def test_annotate_parent_mentions(self):
        _, mentions = annotate_document(self._doc, self._client)
        m_he = mentions[0]
        m_us1 = mentions[4] # the United States
        m_us2 = mentions[10] # United States

        # Verify that parent_mentions functions correctly.
        self.assertEqual(None, m_he.parent_mention)
        self.assertEqual(m_us1, m_us2.parent_mention)

    def test_annotate_nodup(self):
        sentences, mentions = annotate_document(self._doc, self._client)
        # Just assert counts.
        self.assertTrue(is_unique(s.gloss for s in sentences))
        self.assertTrue(is_unique(m.character_span for m in mentions))

    def test_annotate_filter(self):
        """
        Filter mentions that are 'O' mentions.
            the mentions should correctly identify:
            - character offsets
            - glosses
            - links to canonical_mentions
            - links to parent_mentions
        """
        sentences, mentions = annotate_document(self._doc, self._client,
                                                mention_filter=lambda mentions:[m for m in mentions if m.type != 'O'])

        ipdb.set_trace()

        # Just assert counts.
        self.assertEqual(3, len(sentences))
        self.assertEqual(19, len(mentions))

        for m in mentions:
            self.assertTrue(m.ner != 'O')
