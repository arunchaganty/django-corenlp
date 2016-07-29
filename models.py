from django.db import models
from django.contrib.postgres.fields import ArrayField
from . import settings


# TODO(chaganty): include a from_to stanza/dict methods.

class Document(models.Model):
    """
    Represents metadata about a document.
    """
    class Meta:
        if settings.USE_TABLENAME_PREFIX:
            db_table = "document"
        managed = settings.MANAGE_TABLES
    id = models.CharField(max_length=256, primary_key=True)
    corpus_id = models.TextField(help_text="Namespace of the document collection.")
    source = models.TextField(help_text="Tracks the document source.")
    date = models.DateField(null=True, help_text="Date of the document")
    title = models.TextField(help_text="Title for the document")
    gloss = models.TextField(help_text="The entire document")
    metadata = models.TextField(help_text="Miscellaneous metadata in json")

    def __str__(self):
        return self.gloss

    def __repr__(self):
        return "[Document {} ({})]".format(self.id, self.title)

class Sentence(models.Model):
    """
    Represents the consitutents of each sentence, with the basic
    annotations.
    """
    class Meta:
        if settings.USE_TABLENAME_PREFIX:
            db_table = "document"
        managed = settings.MANAGE_TABLES

    id = models.BigIntegerField(primary_key=True)
    # The corpus id is replicated here for the purpose of efficiency.
    corpus_id = models.TextField(help_text="Namespace of the document collection.")
    doc = models.ForeignKey(Document, help_text="Source document")
    sentence_index = models.IntegerField(help_text="Index of sentence in document (useful to order sentences)")
    words = ArrayField(models.TextField(), help_text="Array of tokens")   # Tokens
    lemmas = ArrayField(models.TextField(), help_text="Array of lemmas")  # Tokens
    pos_tags = ArrayField(models.TextField(), help_text="Array of POS tags")     # Field
    ner_tags = ArrayField(models.TextField(), help_text="Array of NER tags")     # Field.
    doc_char_begin = ArrayField(models.IntegerField(), help_text="Array of character begin positions for each token, relative to document start")
    doc_char_end = ArrayField(models.IntegerField(), help_text="Array of character end positions for each token, relative to document start")
    # NOTE: constituencies are ignored because they are usually very expensive to compute
    dependencies = models.TextField(null=True, db_column = 'dependencies_extra', help_text="Dependency tree in CONLL format")
    # NOTE: other dependency formats like dependencies_malt are ignored.
    gloss = models.TextField(help_text="Raw text representation of the sentence")

    def __str__(self):
        return self.gloss

    def __repr__(self):
        return "[Sentence {}]".format(self.gloss[:50])

class Entity(models.Model):
    """
    An entity is the target of entity linking.
    Usually, if linking works, these entities will be represented in
    "Wiki_Format".
    """
    class Meta:
        if settings.USE_TABLENAME_PREFIX:
            db_table = "entity"
        managed = settings.MANAGE_TABLES

    id = models.TextField(primary_key=True, help_text="The entity id is simply the canonical textual representation of the entity")
    ner = models.CharField(max_length=64, help_text="Type of entity, usually an NER tag")

    def __str__(self):
        return "{}".format(str(self.id).replace("_"," "))

    def __repr__(self):
        return "[Entity {}]".format(self.id)

class Mention(models.Model):
    """
    Represents occurrences of entity mentions in the document.
    """
    class Meta:
        if settings.USE_TABLENAME_PREFIX:
            db_table = "mention"
        managed = settings.MANAGE_TABLES

    id = models.BigIntegerField(primary_key = True)
    # The corpus id is replicated here for the purpose of efficiency.
    corpus_id = models.TextField(help_text="Namespace of the document collection.")
    doc = models.ForeignKey(Document, help_text="Source document")
    sentence = models.ForeignKey(Sentence, help_text="Sentence containing the mention")

    # provenance information
    token_begin = ArrayField(models.IntegerField(), help_text="Token offset within sentence where this entity mention starts")
    token_end = ArrayField(models.IntegerField(), help_text="Token offset within sentence where this entity mention ends")
    doc_char_begin = ArrayField(models.IntegerField(), help_text="Character offset within the document where this entity mention starts")
    doc_char_end = ArrayField(models.IntegerField(), help_text="Character offset within the document where this entity mention ends")
    doc_canonical_char_begin = ArrayField(models.IntegerField(), help_text="Character offset within the document where this entity's canonical mention (resolved through coref) starts")
    doc_canonical_char_end = ArrayField(models.IntegerField(), help_text="Character offset within the document where this entity's canonical mention (resolved through coref) ends")

    # linking information
    ner = models.CharField(max_length=64, help_text="Type of entity, usually an NER tag")
    best_entity = models.ForeignKey(Entity, related_name="mentions", db_column="best_entity", help_text="The best entity link for this mention")
    best_entity_score = models.FloatField(null=True, help_text="Linking score for the best entity match")
    unambiguous_link = models.BooleanField(help_text="Was the linking unambigiuous?")
    alt_entity = models.ForeignKey(Entity, null=True, related_name="mentions_alt", db_column="alt_entity", help_text="The 2nd best entity link for this mention")
    alt_entity_score = models.FloatField(null=True, help_text="Linking score for the 2nd best entity match")

    gloss = models.TextField(null=True, help_text="Raw text representation of the mention")

    def __str__(self):
        return self.gloss

    def __repr__(self):
        return "[Mention {}]".format(self.gloss[:50])

class Relation(models.Model):
    """
    Represents a relation between two entities in a document.
    If has_title('Obama', 'president') then:
        'Obama' is the entity
        'has_title' is the relation
        'president' is the slot value
    """
    class Meta:
        if settings.USE_TABLENAME_PREFIX:
            db_table = "kbp_slot_fill"
        managed = settings.MANAGE_TABLES

    id = models.BigIntegerField(primary_key = True)
    # Provenance
    corpus_id = models.TextField(help_text="Namespace of the document collection.")
    sentence = models.ForeignKey(Sentence, help_text="Sentence containing the mention")

    # Entity
    entity = models.ForeignKey(Mention, null = True, related_name='entity_relations', help_text="Link to the the entity mention")
    # Replicated here for efficiency
    entity_name = models.TextField(help_text="The link of the entity")
    entity_gloss = models.TextField(help_text="The textual gloss of the entity")
    # Slot
    slot_value = models.ForeignKey(Mention, null = True, related_name='slot_relations', help_text="Link to the the slot mention")
    # Replicated here for efficiency
    slot_value_name = models.TextField(help_text="The link of the slot value")
    slot_value_gloss = models.TextField(help_text="The textual gloss of the slot filler")

    # Relation
    relation = models.TextField(help_text="Relation between the entity and slot value")
    score = models.FloatField(help_text="Score predicted by the relation extractor")

    def __str__(self):
        return "{} {} {}".format(self.entity_gloss, self.relation, self.slot_value_gloss)

    def __repr__(self):
        return "[Relation {} {} {}]".format(self.entity_gloss, self.relation, self.slot_value_gloss)

