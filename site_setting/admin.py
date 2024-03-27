from django.contrib import admin
from .models import *


class Home1Inline(admin.TabularInline):
    model = Section1
    extra = 1
    list_display = ['title', 'subtitle']


class Home1Admin(admin.ModelAdmin):
    inlines = [Home1Inline]


class Home2Inline(admin.TabularInline):
    model = Section2
    extra = 1
    list_display = ['title', 'subtitle']


class Home2Admin(admin.ModelAdmin):
    inlines = [Home2Inline]


admin.site.site_header = "Home page"
admin.site.register(HomePageAbout1, Home1Admin)
admin.site.register(HomePageAbout2, Home2Admin)
