from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User

from main.models import Profile, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'title', 'seller', 'short_desc', 'description', 'image', 'price',
            'quantity', 'discount', 'category', 'tags'
        )
        widgets = {
            'seller': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProfileForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput())
    date_of_birth = forms.DateField(
        label='Возраст',
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ('user', 'date_of_birth', 'avatar')


class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилие', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


ProfileFormSet = inlineformset_factory(
    User,
    Profile,
    fields='__all__',
    extra=0,
    min_num=1,
    can_delete=False
)
