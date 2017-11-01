# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.conf.urls import url
from .views import index, query, result, upload, upload_done

__author__ = 'lundberg'

urlpatterns = [
    # Index view
    url(r'^$', query),
    url(r'^query/$', query, name='query'),
    url(r'^result/$', result, name='result'),
    url(r'^upload/$', upload, name='upload'),
    url(r'^upload_done/$', upload_done, name='upload_done')
]