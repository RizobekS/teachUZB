from django.utils.translation import gettext_lazy as _
from modeltranslation.translator import translator, TranslationOptions

from .models import (
    HomePageAbout1,
    Section1,
    HomePageAbout2,
    Section2
)


class HomePageAbout1Options(TranslationOptions):
    fields = ['subtitle']
    fallback_values = _('-- sorry, no translation provided')


class Section1Options(TranslationOptions):
    fields = ['title', 'subtitle']
    fallback_values = _('-- sorry, no translation provided')


class HomePageAbout2Options(TranslationOptions):
    fields = ['subtitle']
    fallback_values = _('-- sorry, no translation provided')


class Section2Options(TranslationOptions):
    fields = ['title', 'subtitle']
    fallback_values = _('-- sorry, no translation provided')


translator.register(HomePageAbout1, HomePageAbout1Options)
translator.register(Section1, Section1Options)
translator.register(HomePageAbout2, HomePageAbout2Options)
translator.register(Section2, Section2Options)
