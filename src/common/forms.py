from django import forms
from django.core.exceptions import ValidationError
from datetime import date as datetime_date
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from common.models import UserProfile

from allauth.account.forms import LoginForm as _LoginForm
from allauth.account.forms import SignupForm as _SignupForm
from allauth.socialaccount.forms import SignupForm as _SocialSignupForm


class DatePicker(forms.DateInput):
    template_name = 'forms/date-field.html'


class JasnyFileInput(forms.FileInput):
    template_name = 'forms/image-field.html'

    def build_attrs(self, base_attrs, extra_attrs=None):
        self.field_image = base_attrs.pop('field_image', None)
        return super().build_attrs(base_attrs, extra_attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['field_image'] = self.field_image
        return context


class SocialSignupForm(_SocialSignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.sociallogin and \
           self.sociallogin.account.provider in ('google', 'facebook'):
            name = self.sociallogin.account.extra_data['email'].split('@')[0]
            self.fields['username'].widget.attrs.update({'value': name})


class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        sociallogin = kwargs.pop('sociallogin', None)
        
        super().__init__(*args, **kwargs)

        self.fields['birth_date'].input_formats = ['%d.%m.%Y']
        self.fields['birth_date'].widget.format = '%d.%m.%Y'

        if sociallogin:
            if sociallogin.account.provider == 'google':
                field_image = sociallogin.account\
                    .extra_data['picture'].split('=')[0] + '=s140'
                self.fields['avatar'].widget.attrs.update(
                    field_image=field_image
                )
            elif sociallogin.account.provider == 'github':
                field_image = sociallogin.account\
                    .extra_data['avatar_url'].split('?')[0] + '?s=140&v=4'
                self.fields['avatar'].widget.attrs.update(
                    field_image=field_image
                )
                self.fields['about'].initial = \
                    sociallogin.account.extra_data['bio']
        
        if self.instance.avatar:
            self.fields['avatar'].widget.attrs.update(
                field_image=self.instance.avatar.url,
                value=self.instance.avatar
            )

    class Meta:
        model = UserProfile
        fields = ['birth_date', 'avatar', 'about']
        labels = {
            'birth_date': _('Date of Birth'),
            'avatar': _('Profile picture'),
            'about': _('Bio')
        }
        widgets = {
            'avatar': JasnyFileInput(),
            'birth_date': DatePicker(),
            'about': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': _('Some words about you')
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data