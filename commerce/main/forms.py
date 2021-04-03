from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
# from main.validators import validator_age
from datetime import date


from main.models import Profile


class ProfileForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput())
    date_of_birth = forms.DateField(
        label='Возраст',
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ('user', 'date_of_birth')


class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилие', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


ProfileFormSet = inlineformset_factory(
    User,
    Profile,
    form=ProfileForm,
    extra=0,
    min_num=1,
    can_delete=False
)
