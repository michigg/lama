import logging

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from account_manager.forms import EmailTemplateForm
from account_manager.utils.mail_utils import WelcomeMailTemplateController, DeletionMailTemplateController

logger = logging.getLogger(__name__)

# DONE
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    return render(request, 'admin/list_user.jinja2', {'users': _get_django_users()})

# DONE
def _get_django_users():
    users = User.objects.all().order_by('username')
    return users

# DONE
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

# DONE
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

# DONE
@user_passes_test(lambda u: u.is_superuser)
def configuration_screen(request):
    return render(request, 'admin/configuration.jinja2', {})


@user_passes_test(lambda u: u.is_superuser)
def configuration_screen_welcome_mail(request):
    welcome_mail = WelcomeMailTemplateController()
    template = welcome_mail.get_template()
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST)
        if form.is_valid():
            welcome_mail.save_template(form.cleaned_data["template"])
            return render(request, 'admin/configuration.jinja2',
                          {"success_headline": "Aufgabe Erfolgreich beendet",
                           "success_text": "Das Template wurde erfolgreich gespeichert", })
        else:
            return render(request, 'admin/configuration.jinja2',
                          {"welcome_mail_form": form, "error_headline": "Aufgabe abgebrochen",
                           "error_text": "Formular ungültig. Das Template konnte nicht gespeichert werden.", })
    else:
        form_data = {'template': template}
        form = EmailTemplateForm(initial=form_data)
    return render(request, 'admin/configuration.jinja2', {"welcome_mail_form": form})


@user_passes_test(lambda u: u.is_superuser)
def configuration_screen_deletion_mail(request):
    welcome_mail = DeletionMailTemplateController()
    template = welcome_mail.get_template()
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST)
        if form.is_valid():
            welcome_mail.save_template(form.cleaned_data["template"])
            return render(request, 'admin/configuration.jinja2',
                          {"success_headline": "Aufgabe Erfolgreich beendet",
                           "success_text": "Das Template wurde erfolgreich gespeichert", })
        else:
            return render(request, 'admin/configuration.jinja2',
                          {"deletion_mail_form": form, "error_headline": "Aufgabe abgebrochen",
                           "error_text": "Formular ungültig. Das Template konnte nicht gespeichert werden.", })
    else:
        form_data = {'template': template}
        form = EmailTemplateForm(initial=form_data)
    return render(request, 'admin/configuration.jinja2', {"deletion_mail_form": form})
