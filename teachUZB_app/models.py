import os
import uuid

from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField

from teachUZB.settings import EMAIL_HOST_USER


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 100 or img.width > 100:
                new_img = (100, 100)
                img.thumbnail(new_img)
                img.save(self.avatar.path)


class AboutPage(models.Model):
    class Meta:
        verbose_name = _('About Us')
        verbose_name_plural = _('About Us')

    about = RichTextUploadingField(blank=True, null=True)

    image = ResizedImageField(upload_to='images/about_page/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg', 'webp'])],
                              null=True, blank=True, quality=65, force_format='JPEG')

    def __str__(self):
        return self.about


class Feedback(models.Model):
    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')

    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True)
    text = models.CharField(max_length=1000, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # for moderator
    approved = models.BooleanField(blank=True, default=False)
    reply_subject = models.CharField(max_length=255, blank=True, null=True)
    reply_message = RichTextUploadingField(max_length=1000, blank=True, null=True)
    replied_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.reply_subject and self.reply_message:
            self.replied_date = timezone.now()
            send_mail(self.reply_subject, self.reply_message, EMAIL_HOST_USER, [self.email], fail_silently=False)
            super(Feedback, self).save()
        else:
            super(Feedback, self).save()

    def __str__(self):
        return self.name


class PersonalData(models.Model):
    class Meta:
        verbose_name = _('Full registration')
        verbose_name_plural = _('Full Registration')

    first_name = models.CharField(max_length=600, null=True)
    last_name = models.CharField(max_length=600, null=True)
    email = models.CharField(max_length=600, null=True)

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=100, null=True)
    birthday = models.DateField(null=True, auto_now=False, auto_now_add=False)
    phone = models.CharField(max_length=20, null=True)
    citizenship = models.CharField(max_length=100, null=True, blank=True)
    which_city = models.CharField(max_length=100, null=True)
    registered_address = models.CharField(max_length=255, null=True)
    entry_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # for moderator
    reply_subject = models.CharField(max_length=255, blank=True, null=True)
    reply_message = RichTextUploadingField(max_length=1000, blank=True, null=True)
    replied_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        if self.reply_subject and self.reply_message:
            self.replied_date = timezone.now()
            send_mail(self.reply_subject, self.reply_message, EMAIL_HOST_USER, [self.email], fail_silently=False)
            super(PersonalData, self).save()
        else:
            super(PersonalData, self).save()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Education(models.Model):
    class Meta:
        verbose_name = _('Education')
        verbose_name_plural = _('Education')

    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('full_registrations/files', filename)

    personal_data = models.ForeignKey(PersonalData, on_delete=models.CASCADE)
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to=get_file_path,
                            validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True, blank=True)


class WorkExperience(models.Model):
    class Meta:
        verbose_name = _('Work Experience')
        verbose_name_plural = _('Work Experience')

    personal_data = models.ForeignKey(PersonalData, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


class SocialActivities(models.Model):
    class Meta:
        verbose_name = _('Social Activities')
        verbose_name_plural = _('Social Activities')

    personal_data = models.ForeignKey(PersonalData, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    type_of_activity = models.CharField(max_length=100)


class ParticipationInProgram(models.Model):
    class Meta:
        verbose_name = _('Participation In Program')
        verbose_name_plural = _('Participation In Program')

    personal_data = models.ForeignKey(PersonalData, on_delete=models.CASCADE)
    where_get_information = models.CharField(max_length=100)
    participate_in_summer = models.CharField(max_length=100, null=True)
    work_full_time = models.CharField(max_length=100, null=True)
    why_teach_uzb = models.TextField(max_length=500, null=True)
    value_to_the_children = models.TextField(max_length=500, null=True)
    benefit_from_your_experience_in_the_program = models.TextField(max_length=500, null=True)


class Contact(models.Model):
    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    phone = models.CharField(max_length=13, null=True)
    message = RichTextUploadingField(max_length=1000, blank=True)
    received_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    # for moderator
    reply_subject = RichTextUploadingField(max_length=255, blank=True, null=True)
    reply_message = RichTextUploadingField(max_length=1000, blank=True, null=True)
    replied_date = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.reply_subject and self.reply_message:
            self.replied_date = timezone.now()
            send_mail(self.reply_subject, self.reply_message, EMAIL_HOST_USER, [self.email], fail_silently=False)
            super(Contact, self).save()
        else:
            super(Contact, self).save()

    def __str__(self):
        return self.name


class Team(models.Model):
    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')

    title = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)

    rank = models.IntegerField(blank=True, default=100, null=True)

    office = models.IntegerField(default=0, blank=False, )  # 0-JPIU, 1-Toshkent, 2-Djizzak, 3-Namangan, 4-Buxoro, 5-QQR

    image = ResizedImageField(upload_to='images/piu/staff',
                              validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])], null=True,
                              blank=True, unique=True, quality=65)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'

    question = RichTextUploadingField(blank=True, null=True)

    answer = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return self.question

