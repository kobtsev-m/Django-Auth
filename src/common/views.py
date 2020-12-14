from django.http.response import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db import transaction
from django.views.generic import TemplateView, DetailView, UpdateView
from django.contrib.auth.models import User

from common.forms import UserProfileForm

from allauth.account.forms import SignupForm
from allauth.account.views import SignupView as SignupViewDefault
from allauth.socialaccount.views import SignupView as SocialSignupViewDefault
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import complete_signup
from allauth.socialaccount import helpers
from allauth.exceptions import ImmediateHttpResponse

from django.core.files.images import ImageFile
from urllib.request import urlopen
from urllib.parse import urlparse
from io import BytesIO

from django.contrib import messages



class Home(TemplateView):

    template_name = 'common/base.html'


class Profile(DetailView):
    
    template_name = 'common/user_profile.html'
    model = User

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
           request.user.pk == kwargs.get('pk'):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('common:index'))


class Settings(UpdateView):
    
    template_name = 'common/user_settings.html'
    model = User
    fields = ['username', 'first_name', 'last_name']

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
           request.user.pk == kwargs.get('pk'):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('common:index'))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response({
            'form': self.get_form(),
            'profile_form': UserProfileForm(
                instance=self.object.userprofile
            )
        })
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        clear_avatar = request.POST.get('avatar_changed') == '1' and \
            not request.FILES.get('avatar')
            
        form = self.get_form()
        profile_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=self.object.userprofile
        )
        
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form, clear_avatar)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form, clear_avatar):
        self.object = form.save()
        userprofile_instance = profile_form.save(commit=False)
        if clear_avatar: 
            userprofile_instance.avatar = None
        self.object.userprofile = userprofile_instance.save()
        return self.get_success_url()

    def form_invalid(self, form, profile_form):
        return self.render_to_response({
            'form': form,
            'profile_form': profile_form
        })

    def get_success_url(self):
        messages.success(self.request, 'Data is saved!')
        return HttpResponseRedirect(
            reverse_lazy('common:user-settings', args=(self.request.user.pk,))
        )


class SignupView(SignupViewDefault):

    def get(self, request, *args, **kwargs):
        form = SignupForm()
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        
        if 'user_submit' in request.POST:
            form = SignupForm(request.POST)
            if not form.is_valid():
                return self.form_invalid(form=form)
            
            request.session['signup_user_data'] = request.POST
            profile_form = UserProfileForm()
            return self.render_to_response({'profile_form': profile_form})

        elif 'profile_submit' in request.POST:
            profile_form = UserProfileForm(request.POST, request.FILES)
            if profile_form.is_valid():
                form = SignupForm(
                    request.session.pop('signup_user_data', None)
                )
                if form.is_valid():
                    return self.form_valid(form, profile_form)
            
            return self.form_invalid(profile_form=profile_form)
        
        return HttpResponseNotFound()
    
    @transaction.atomic
    def form_valid(self, form, profile_form):
        self.user = form.save(self.request)
        profile_instance = profile_form.save(commit=False)
        profile_instance.user = self.user
        profile_instance.save()
        try:
            return complete_signup(
                self.request,
                self.user,
                app_settings.EMAIL_VERIFICATION,
                self.get_success_url(),
            )
        except ImmediateHttpResponse as e:
            return e.response
    
    def form_invalid(self, form=None, profile_form=None):
        if form:
            return self.render_to_response(self.get_context_data(form=form))

        return self.render_to_response({'profile_form': profile_form})


class SocialSignupView(SocialSignupViewDefault):

    def get(self, request, *args, **kwargs):
        
        social_form = self.get_form()
        profile_form = UserProfileForm(sociallogin=self.sociallogin)

        return self.render_to_response({
            'account': self.sociallogin.account,
            'form': social_form,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):

        form_class = self.get_form_class()
        social_form = self.get_form(form_class)

        use_provider_avatar = request.POST.get('avatar_changed') == '0'

        if use_provider_avatar:
            profile_form =  UserProfileForm(
                request.POST, request.FILES, sociallogin=self.sociallogin
            )
        else:
            profile_form =  UserProfileForm(
                request.POST, request.FILES
            )

        if social_form.is_valid() and profile_form.is_valid():
            return self.form_valid(
                social_form, profile_form, use_provider_avatar
            )

        return self.form_invalid(social_form, profile_form)
    
    @transaction.atomic
    def form_valid(self, social_form, profile_form, use_provider_avatar):
        
        self.request.session.pop('socialaccount_sociallogin', None)
        user = social_form.save(self.request)
        
        instance = profile_form.save(commit=False)
        if use_provider_avatar:
            if self.sociallogin.account.provider == 'google':
                img_url = self.sociallogin.account\
                    .extra_data.get('picture', '').split('=')[0] + '=s0'
            elif self.sociallogin.account.provider == 'github':
                img_url = self.sociallogin.account\
                    .extra_data.get('avatar_url', '')
            else:
                img_url = None
            img_name = urlparse(img_url).path.split('/')[-1] + '.jpg'
            img_obj = BytesIO(urlopen(img_url).read())
            instance.avatar.save(img_name, ImageFile(img_obj), save=False)

        name = self.sociallogin.account.extra_data.get('name', '')
        if len(name.split()) > 1:
            instance.first_name = name.split()[0]
            instance.second_name = name.split()[1]

        instance.user = user
        instance.save()

        return helpers.complete_social_signup(self.request, self.sociallogin)
    
    def form_invalid(self, social_form, profile_form):
        return self.render_to_response(self.get_context_data(
            account=self.sociallogin.account,
            form=social_form,
            profile_form=profile_form
        ))
