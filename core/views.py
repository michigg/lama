import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)


def about(request):
    return render(request, 'about.jinja2', {})
