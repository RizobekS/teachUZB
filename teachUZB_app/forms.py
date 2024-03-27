from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _

from .models import Contact, Feedback, Profile, Education, WorkExperience, PersonalData, SocialActivities, \
    ParticipationInProgram

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female')
]

WHERE_GET_INFO = [
    ('Website', 'Website'),
    ('social_media', 'Social Media'),
    ('other', 'Other'),
]

PARTICIPATE_IN_THE_SUMMER = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]

WORK_FULLTIME_FROM_SEPTEMBER = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name', 'phone', 'email', 'message'
        ]


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'name', 'email', 'phone', 'text'
        ]


class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class PersonalDataForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = PersonalData
        fields = ['gender', 'birthday', 'phone', 'citizenship', 'which_city', 'registered_address']
        labels = {
            'birthday': 'Date of Birth',
            'phone': 'Mobile No.',
            'citizenship': 'Citezenship',
            'which_city': 'In which city do you live currently?',
            'registered_address': 'Registered Address',
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'class': 'form-control',
                                               'id': 'datepicker',
                                               'type': 'date'}),
            'citizenship': forms.TextInput(attrs={'class': 'form-control'}),
            'which_city': forms.TextInput(attrs={'class': 'form-control'}),
            'registered_address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'faculty', 'specialization', 'start_date', 'end_date']


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company', 'position', 'start_date', 'end_date']


class SocialActivitiesForm(forms.ModelForm):
    class Meta:
        model = SocialActivities
        fields = ['company', 'type_of_activity']


class ParticipationInProgramForm(forms.ModelForm):
    where_get_information = forms.ChoiceField(
        choices=WHERE_GET_INFO, widget=forms.Select(attrs={'class': 'form-control'}))
    work_full_time = forms.ChoiceField(
        choices=WORK_FULLTIME_FROM_SEPTEMBER, widget=forms.Select(attrs={'class': 'form-control'}))
    participate_in_summer = forms.ChoiceField(
        choices=PARTICIPATE_IN_THE_SUMMER, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = ParticipationInProgram
        fields = ['where_get_information', 'work_full_time', 'participate_in_summer', 'why_teach_uzb']
        labels = {
            'where_get_information': 'Where did you get information about the program?',
            'why_teach_uzb': 'Why do you want to become a fellow of the Teacher for Uzbekistan program? ? What do you think is your value for children and for the school? How can the experience of fellowship in the program benefit you? Please give a detailed answer in the form of an essay. *',
            'work_full_time': 'Are you ready to work full-time from September 1, 2024, without combining participation in the program with other activities?*',
            'participate_in_summer': 'Will you be able to participate in the Summer Institute in the summer of 2024 (participation in it is mandatory to participate in the program)? *',
        }
        widgets = {
            'why_teach_uzb': forms.Textarea(attrs={'class': 'form-control'}),
        }
