from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/$', views.contact_cru, name='new'),
    url(r'^(?P<uuid>[\w-]+)/$', views.contact_detail, name='detail'),
    url(r'^(?P<uuid>[\w-]+)/edit/$', views.contact_cru, name='update'),
    url(r'^(?P<uuid>[\w-]+)/delete/$', views.ContactDelete.as_view(), name='delete'),
]
