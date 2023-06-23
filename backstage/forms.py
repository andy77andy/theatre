from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from backstage.models import Actor


def validate_fee(
    average_fee: int, min_fee: int, max_fee: int
):  # regex validation is also possible here

    if not (min_fee <= average_fee <= max_fee):
        raise ValidationError(f"Average_fee  should exist in range {min_fee} and {max_fee}")
    return average_fee


def validate_year_of_joining(
    year_of_joining: int, first_year: int
):  # regex validation is also possible here

    if year_of_joining < first_year:

        raise ValidationError(f"Year_of_joining should be not earlier {first_year}")
    return year_of_joining


class ActorCreationForm(UserCreationForm):
    MIN_FEE = 700
    MAX_FEE = 3000
    FIRST_YEAR = 2000

    class Meta(UserCreationForm.Meta):
        model = Actor
        fields = UserCreationForm.Meta.fields + (
            "average_fee",
            "awards",
            "year_of_joining",
            "first_name",
            "last_name",
        )

    def clean_fee(self):
        return validate_fee(self.cleaned_data["average_fee"], min_fee=self.MIN_FEE, max_fee=self.MAX_FEE)

    def clean_year_number(self):
        return validate_year_of_joining(self.cleaned_data["year_of_joining"], first_year=self.FIRST_YEAR)

    # def validate_fee(self, average_fee: int
    # ):  # regex validation is also possible here
    #
    #     if not (self.MIN_FEE <= average_fee <= self.MAX_FEE):
    #         self.add_error("average_fee", f"Average_fee should exist in range {self.MIN_FEE} and {self.MAX_FEE}")
    #     return average_fee
    #


class ActorValidateUpdateDataForm(forms.ModelForm):
    MIN_FEE = 700
    MAX_FEE = 3000
    FIRST_YEAR = 1900

    class Meta:
        model = Actor
        fields = "__all__"

    def clean_fee(self):
        return validate_fee(self.cleaned_data["average_fee"], min_fee=self.MIN_FEE, max_fee=self.MAX_FEE)

    def clean_year_number(self):
        return validate_year_of_joining(self.cleaned_data["year_of_joining"], first_year=self.FIRST_YEAR)
