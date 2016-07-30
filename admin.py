from django.contrib import admin
from corenlp.models import Document
from corenlp.util import annotate_document
from django.db import transaction

# Register your models here.
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        """
        If a document is being added (`change == False`), then
        call the annotator to annotate the doument.
        """
        if not change:
            sentences, mentions = annotate_document(obj.gloss)
            with transaction.atomic():
                obj.save()
                # TODO(chaganty): batch these saves.
                for sentence in sentences:
                    sentence.doc = obj
                    sentence.save()
                for mention in mentions:
                    mention.save()
        else:
            raise NotImplementedError("Can't update a document")

