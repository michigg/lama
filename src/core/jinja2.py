from django.templatetags.static import static
from django.utils.translation import gettext, ngettext
from django.urls import reverse
from django.utils import translation

from jinja2 import Environment


def environment(**options):
    options['extensions'] = ['jinja2.ext.i18n']
    env = Environment(**options)
    # env.install_gettext_translations(translation)
    env.install_gettext_callables(gettext=gettext, ngettext=ngettext, newstyle=True)
    env.globals.update({
        'static': static,
        'url': reverse,
    })
    return env
