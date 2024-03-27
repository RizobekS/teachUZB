from django.utils.translation import gettext_lazy as _
from modeltranslation.translator import translator, TranslationOptions

from .models import (
    AboutPage, Team, FAQ,
)


class AboutPageOptions(TranslationOptions):
    fields = ['about']
    fallback_values = _('-- sorry, no translation provided')


class TeamOptions(TranslationOptions):
    fields = ['title', 'name']
    fallback_values = _('-- sorry, no translation provided')


class FAQOptions(TranslationOptions):
    fields = ['question', 'answer']
    fallback_values = _('-- sorry, no translation provided')


translator.register(AboutPage, AboutPageOptions)
translator.register(Team, TeamOptions)
translator.register(FAQ, FAQOptions)
