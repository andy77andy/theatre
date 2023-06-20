from django.contrib.auth.forms import UserCreationForm

from backstage.models import Actor


class ActorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Actor
        fields = UserCreationForm.Meta.fields + (
            "average_fee",
            "awards",
            "year_of_joining",
            "first_name",
            "last_name",
        )
#
#     # def clean_license_number(self):  # this logic is optional, but possible
#     #     return validate_license_number(self.cleaned_data["license_number"])