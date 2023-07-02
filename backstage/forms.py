import form as form
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelMultipleChoiceField

from backstage.models import Actor, Play, Award


def validate_fee(
    average_fee: int, min_fee: int, max_fee: int
):  # regex validation is also possible here
    if not (min_fee <= int(average_fee) <= max_fee):
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

    def clean_average_fee(self):
        return validate_fee(self.cleaned_data["average_fee"], min_fee=self.MIN_FEE, max_fee=self.MAX_FEE)

    def clean_year_of_joining(self):
        return validate_year_of_joining(self.cleaned_data["year_of_joining"], first_year=self.FIRST_YEAR)


class ActorValidateUpdateDataForm(forms.ModelForm):
    MIN_FEE = 700
    MAX_FEE = 3000
    FIRST_YEAR = 1900

    class Meta:
        model = Actor
        fields = "__all__"

    def clean_average_fee(self):
        return validate_fee(self.cleaned_data["average_fee"], min_fee=self.MIN_FEE, max_fee=self.MAX_FEE)

    def clean_year_of_joining(self):
        return validate_year_of_joining(self.cleaned_data["year_of_joining"], first_year=self.FIRST_YEAR)


class PlayForm(forms.ModelForm):
    troupe = ModelMultipleChoiceField(queryset=get_user_model().objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    widgets = {
        'day_of_premiere': forms.DateInput(attrs={'type': 'date'})
    }

    class Meta:
            model = Play
            fields = "__all__"
            widgets = {
                'day_of_premiere': forms.DateInput(attrs={'type': 'date'})
            }


class PlaySearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name..."})
    )


class ActorSearchForm(forms.Form):
    last_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by last name..."})
    )

class PlayPremiereForm(forms.ModelForm):
    class Meta:
        model = Play
        fields = ['day_of_premiere', ]
        widgets = {
            'day_of_premiere': forms.DateInput(attrs={'type': 'date'})
        }


class AwardForm(forms.ModelForm):
    YEAR_CHOICES = [(year, str(year)) for year in range(1990, 2023)]  # Adjust the upper bound for recent year

    NAME_CHOICES = [
        ('', '--- Select Award ---'),
        ('best_play', 'Best Play'),
        ('best_director', 'Best Director'),
        ('best_actor_actress', 'Best Actor/Actress'),
        ('best_supporting_actor_actress', 'Best Supporting Actor/Actress'),
        ('best_decoration', 'Best Decoration')
    ]

    NOMINATION_CHOICES = [
        ('best_play', 'Best Play'),
        ('best_director', 'Best Director'),
        ('best_actor_actress', 'Best Actor/Actress'),
        ('best_supporting_actor_actress', 'Best Supporting Actor/Actress'),
        ('best_decoration', 'Best Decoration')
    ]

    class Meta:
        model = Award
        fields = '__all__'
        widgets = {}

    Meta.widgets = {'name': forms.Select(choices=NAME_CHOICES),
            'nomination': forms.Select(choices=NOMINATION_CHOICES),
            'year': forms.Select(choices=YEAR_CHOICES)}

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Please select a valid name.')
        return name

    def clean_nomination(self):
        nomination = self.cleaned_data.get('nomination')
        if not nomination:
            raise forms.ValidationError('Please select a valid nomination.')
        return nomination
