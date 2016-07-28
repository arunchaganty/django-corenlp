from django.shortcuts import render
from .models import *

def view(request, doc_id=None):
    """
    View a particular document from the database.
    """
    # Get the document from the database.
    if doc_id is not None:
        try:
            doc = Document.objects.get(doc_id=doc_id)
            return render('index.html', {'doc':doc})

