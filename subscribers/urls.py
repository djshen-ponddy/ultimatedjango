from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signup/$', views.subscriber_new, name='new'),
]
