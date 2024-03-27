import random
import string

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from .models import *
from site_setting.models import *
from django.contrib.auth.models import User

from teachUZB_app.forms import ContactForm, FeedbackForm, LoginForm, RegisterForm, UpdateUserForm, UpdateProfileForm, \
    PersonalDataForm, EducationForm, WorkExperienceForm, SocialActivitiesForm, \
    ParticipationInProgramForm
from teachUZB_app.models import AboutPage, Team, FAQ, Feedback, Education, WorkExperience, SocialActivities


def home(request):
    approved_feedback = Feedback.objects.filter(approved=True).order_by('-date')

    about1 = HomePageAbout1.objects.last()
    about2 = HomePageAbout2.objects.last()
    about1_sections = Section1.objects.filter(parent=about1).order_by('id')
    about2_sections = Section2.objects.filter(parent=about2).order_by('id')

    context = {
        "approved_feedbacks": approved_feedback,
        "about1": about1,
        "about2": about2,

        "about1_sections": about1_sections,
        "about2_sections": about2_sections
    }
    return render(request, "home.html", context)


def about(request):
    info_about = AboutPage.objects.first()
    return render(request, 'about_us.html', {'info_about': info_about})


def faq(request):
    questions_and_answers = FAQ.objects.all().order_by('id')
    return render(request, 'faq.html', {'questions_and_answers': questions_and_answers})


def team(request):
    context = {
        'staff_team': Team.objects.filter(office=0).order_by('rank'),
        'staff_tashkent': Team.objects.filter(office=1).order_by('rank'),
        'staff_jizzakh': Team.objects.filter(office=2).order_by('rank'),
        'staff_namangan': Team.objects.filter(office=3).order_by('rank'),
        'staff_buxoro': Team.objects.filter(office=4).order_by('rank'),
        'staff_qqr': Team.objects.filter(office=5).order_by('rank')
    }
    return render(request, 'team.html', context)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid() and request.POST['address'] == "":
            form.save()
            name = request.POST['name']
            messages.success(request, 'Success!')
            return render(request, 'contact.html', {'name': name})
        else:
            name = _("Oops, something went wrong!")
            return render(request, 'contact.html', {'name': name})
    else:
        return render(request, 'contact.html', {})


def feedback(request):
    approved_feedback = Feedback.objects.filter(approved=True).order_by('-date')[:5]

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            name = request.POST['name']
            messages.success(request, 'Success!')
            return render(request, 'feedback.html',
                          {'name': name, 'approved_feedback': approved_feedback})
        else:
            name = _("Oops something went wrong!")
            return render(request, 'feedback.html',
                          {'name': name, 'approved_feedback': approved_feedback})
    else:
        return render(request, "feedback.html",
                      {'approved_feedback': approved_feedback})


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    user = User.objects.get(id=request.user.id)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    except Exception as e:
        print("Xatolik yuz berdi:", e)
        profile = None

    if request.method == "POST":
        user.username = request.POST.get("username") or None
        user.email = request.POST.get("email") or None
        user.save()

        profile.avatar = request.FILES.get("avatar") or None
        profile.bio = request.POST.get("profile_bio") or None
        profile.save()
        messages.success(request, "Muvoffaqiyatli o'zgartirildi!")
    context = {
        "profile": profile,
        "user": user
    }
    return render(request, 'users/profile.html', context)


def full_registration(request):
    if request.method == "POST":
        personal_data = PersonalData()
        personal_data.first_name = request.POST.get("user_first_name")
        personal_data.last_name = request.POST.get("user_last_name")
        personal_data.email = request.POST.get("user_email")
        personal_data.user = request.user
        personal_data.gender = request.POST.get("personal_gender")
        personal_data.birthday = request.POST.get("personal_dateofbirth")
        personal_data.phone = request.POST.get("personal_mobileno")
        personal_data.citizenship = request.POST.get("personal_citezenship")
        personal_data.which_city = request.POST.get("personal_which_city")
        personal_data.registered_address = request.POST.get("personal_registered_address")
        personal_data.save()

        participationinprogram = ParticipationInProgram()
        participationinprogram.personal_data = personal_data
        participationinprogram.where_get_information = request.POST.get("where_get_information")
        participationinprogram.work_full_time = request.POST.get("work_full_time")
        participationinprogram.participate_in_summer = request.POST.get("participate_in_summer")
        participationinprogram.why_teach_uzb = request.POST.get("why_teach_uzb")
        participationinprogram.value_to_the_children = request.POST.get("value_to_the_children")
        participationinprogram.benefit_from_your_experience_in_the_program = request.POST.get("benefit_from_your_experience_in_the_program")
        participationinprogram.save()

        for num in range(1, 11):
            institution = request.POST.get(f"education_{num}_institution")
            degree = request.POST.get(f"education_{num}_degree")
            faculty = request.POST.get(f"education_{num}_faculty")
            specialization = request.POST.get(f"education_{num}_specialization")
            start_date = request.POST.get(f"education_{num}_start_date")
            end_date = request.POST.get(f"education_{num}_end_date")
            file = request.FILES.get(f"education_{num}_file")

            if institution and degree and start_date and end_date and file:
                education = Education.objects.create(
                    personal_data=personal_data,
                    institution=institution,
                    degree=degree,
                    faculty=faculty,
                    specialization=specialization,
                    start_date=start_date,
                    end_date=end_date,
                    file=file
                )
                education.save()

        for num in range(1, 11):
            company = request.POST.get(f"experience_{num}_company")
            position = request.POST.get(f"experience_{num}_position")
            start_date = request.POST.get(f"experience_{num}_start_date")
            end_date = request.POST.get(f"experience_{num}_end_date")

            if company and position and start_date and end_date:
                work_experience = WorkExperience.objects.create(
                    personal_data=personal_data,
                    company=company,
                    position=position,
                    start_date=start_date,
                    end_date=end_date
                )
                work_experience.save()

        for num in range(1, 11):
            social_company = request.POST.get(f"social_{num}_company")
            social_activity = request.POST.get(f"social_{num}_activity")

            if social_company and social_activity:
                socials = SocialActivities.objects.create(
                    personal_data=personal_data,
                    company=social_company,
                    type_of_activity=social_activity
                )
                socials.save()

        numbers = string.digits
        random_id = ''.join(random.choices(numbers, k=6))
        return redirect('success-page', random_id)

    return render(request, 'full_registration.html')


@login_required
def registration_success(request):
    return render(request, 'registration_success.html')


def success_page(request, id):
    return render(request, 'sucess_page.html')
