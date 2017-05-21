# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.views import login


urlpatterns = [
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login'),
]
