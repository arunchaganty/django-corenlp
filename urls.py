from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'view/(?P<doc_id>.*)', views.view),
]
