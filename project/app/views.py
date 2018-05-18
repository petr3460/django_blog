from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment, Tag
import pdb
from .forms import CommentForm
from social_django.models import UserSocialAuth
from django.http import HttpResponse
import json
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q


def home(request, page_number=1, tag=''):
    if tag:
        tag = get_object_or_404(Tag, title=tag)
        articles = Article.objects.filter(tags=tag)
    else:
        articles = Article.objects.all()
    query = request.GET.get('q')
    if query:
        articles = articles.filter(
            Q(title__icontains=query)|
            Q(author__first_name__icontains=query)|
            Q(author__last_name__icontains=query)|
            Q(text__icontains=query)
            ).distinct()
    current_page = Paginator(articles, 2)
    user = request.user
    tags = Tag.objects.all()
    #pdb.set_trace()
    content = {
        'articles': current_page.get_page(page_number),
        'user': user,
        'tags': tags,         
    }
    return render(request, 'home.html', content)


def article(request, article_id):    
    user = request.user
    article = get_object_or_404(Article, id=article_id)
    comments = Comment.objects.filter(article=article)
    tags = Tag.objects.all()
    
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
        'tags': tags,  
        'form': form,      
    }
    return render(request, 'article.html', content)


@login_required
def settings(request):
    user = request.user
    tags = Tag.objects.all()
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        vk_login = user.social_auth.get(provider='vk-oauth2')
    except UserSocialAuth.DoesNotExist:
        vk_login = None
    #pdb.set_trace()
    return render(request, 'settings.html', {        
        'twitter_login': twitter_login,  
        'vk_login': vk_login,      
        'tags': tags, 
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
