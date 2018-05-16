from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment, Category
import pdb
from .forms import CommentForm
from social_django.models import UserSocialAuth
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST


def home(request):
    user = request.user
    categories = Category.objects.all()
    content = {
        'articles': Article.objects.all(),
        'user': user,
        'categories': categories,         
    }
    return render(request, 'home.html', content)


def article(request, article_id):    
    user = request.user
    article = get_object_or_404(Article, id=article_id)
    comments = Comment.objects.filter(article=article)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = user
            form.article = article
            form.save()
            return redirect('post', article_id)
    else:
        form = CommentForm()

    #pdb.set_trace()
    content = {
        'article': article,
        'user': user,
        'comments': comments,
        'categories': categories,  
        'form': form,      
    }
    return render(request, 'article.html', content)


@login_required
def settings(request):
    user = request.user
    categories = Category.objects.all()
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
        'can_disconnect': can_disconnect,
        'categories': categories, 
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


@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        article_id = request.POST.get('id', None)
        article = get_object_or_404(Article, id=article_id)

        if article.likes.filter(id=user.id).exists():
            article.likes.remove(user)
            
        else:
            article.likes.add(user)
            

    ctx = {'likes_count': article.total_likes,}
    print(ctx)
    
    return HttpResponse(json.dumps(ctx), content_type='application/json')
