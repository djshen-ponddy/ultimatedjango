from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/$', views.account_cru, name='new'),
    url(r'^list/$', views.AccountList.as_view(), name='list'),
    url(r'^(?P<uuid>[\w-]+)/$', views.account_detail, name='detail'),
    url(r'^edit/(?P<uuid>[\w-]+)/$', views.account_cru, name='update'),
]
