from django.contrib.auth.models import User
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from teachUZB_app.models import Profile


class ProfileResource(resources.ModelResource):
    user = fields.Field(attribute='user', column_name='user', widget=ForeignKeyWidget(User, 'username'))

    class Meta:
        model = Profile
