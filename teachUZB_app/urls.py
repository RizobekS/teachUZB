from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", views.home, name="home"),
    # path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('full-registration/', full_registration, name='full_registration'),
    path('registration-success/', registration_success, name='registration_success'),
    path("team/", views.team, name="team"),
    path("faq/", views.faq, name="faq"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("feedback/", views.feedback, name="feedback"),

    path('success/<int:id>/', views.success_page, name='success-page'),
]
