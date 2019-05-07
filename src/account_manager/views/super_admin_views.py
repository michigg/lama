from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)


@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    return render(request, 'admin/list_user.jinja2', {'users': _get_django_users()})


def _get_django_users():
    users = User.objects.all().order_by('username')
    return users


@user_passes_test(lambda u: u.is_superuser)
def add_superuser(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_superuser = True
        user.save()
        return redirect('django-additional-admin-list')
    except ObjectDoesNotExist as err:
        return render(request, 'admin/list_user.jinja2',
                      {'users': _get_django_users(), 'extra_errors': 'Nutzer ist uns nicht bekannt'})


@user_passes_test(lambda u: u.is_superuser)
def remove_superuser(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_superuser = False
        user.save()
        return redirect('django-additional-admin-list')
    except ObjectDoesNotExist as err:
        return render(request, 'admin/list_user.jinja2',
                      {'users': _get_django_users(), 'extra_errors': 'Nutzer ist uns nicht bekannt'})
