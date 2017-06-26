# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

import logging

import os

import re


from privateviews.decorators import login_not_required

logger = logging.getLogger(__name__)


def index(request):
	return render(request, 'core/index.html')


