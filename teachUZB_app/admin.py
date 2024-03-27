from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from teachUZB_app.models import *
from teachUZB_app.resources import ProfileResource


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0
    can_delete = False
    list_display = ['institution', 'degree', 'faculty', 'specialization', 'start_date', 'end_date', 'file']


class WorkInline(admin.TabularInline):
    model = WorkExperience
    extra = 0
    can_delete = False
    list_display = ['company', 'position', 'start_date', 'end_date']


class SocialInline(admin.TabularInline):
    model = SocialActivities
    extra = 0
    can_delete = False
    list_display = ['company', 'type_of_activity']


class PartProgramInline(admin.TabularInline):
    model = ParticipationInProgram
    extra = 0
    can_delete = False
    list_display = ['where_get_information', 'participate_in_summer', 'work_full_time', 'why_teach_uzb',
                    'value_to_the_children', 'benefit_from_your_experience_in_the_program']


class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['about', 'image']


class FeedbackAdmin(ImportExportModelAdmin):
    list_display = ['name', 'email', 'phone', 'date', 'approved']
    search_fields = ['name', 'email', 'phone']
    list_editable = ['approved']


class ContactAdmin(ImportExportModelAdmin):
    list_display = ['name', 'phone', 'email', 'message', 'received_date', 'replied_date', 'reply_subject',
                    'reply_message']
    search_fields = ['name', 'phone', 'email', 'message']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'rank', 'office', 'image']
    search_fields = ['title', 'name']
    list_editable = ['rank', 'office']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']
    search_fields = ['question']


class PersonalDataAdmin(ImportExportModelAdmin):
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_display = ['first_name', 'last_name', 'email', 'phone', 'which_city']
    inlines = [EducationInline, WorkInline, SocialInline, PartProgramInline]


class ProfilesAdmin(ImportExportModelAdmin):
    resource_class = ProfileResource
    search_fields = ['user__username']
    list_display = ['user', 'avatar', 'bio']


admin.site.site_header = "Teach for Uzbekistan"
admin.site.site_title = "Teach for Uzbekistan"
admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Profile, ProfilesAdmin)
admin.site.register(PersonalData, PersonalDataAdmin)
