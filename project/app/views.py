from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Article, Comment
import pdb

from social_django.models import UserSocialAuth


def home(request):
    user = request.user
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except:
        twitter_login = None

    try:
        vk_login = user.social_auth.get(provider='vk')
    except:
        vk_login = None
    content = {
        'articles': Article.objects.all(),
        
    }
    return render(request, 'home.html', content)


@login_required
def settings(request):
    user = request.user
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        vk_login = user.social_auth.get(provider='vk-oauth2')
    except UserSocialAuth.DoesNotExist:
        vk_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
    #pdb.set_trace()
    return render(request, 'settings.html', {        
        'twitter_login': twitter_login,  
        'vk_login': vk_login,      
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'password.html', {'form': form})