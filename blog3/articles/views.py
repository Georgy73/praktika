from django.http import Http404
from django.shortcuts import render, redirect
from .models import Article
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login


def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})


def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404


def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                # если поля заполнены без ошибок
                article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('get_article', article_id=article.id)
            # перейти на страницу поста
            else:
                # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    else:
        raise Http404


def create_user(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            form = {
                'username': request.POST["username"],
                'email': request.POST["email"],
                'password': request.POST["password"]
            }
            if form["username"] and form["email"] and form["password"]:
                try:
                    User.objects.get(username=form['username'])
                    form['errors'] = u"Пользователь уже существует"
                    return render(request, 'register.html', {'form': form})
                except User.DoesNotExist:
                    User.objects.create_user(username=form["username"], email=form["email"], password=form["password"])
                    return render(request, 'login.html', {})
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'register.html', {'form': form})
        else:
            return render(request, 'register.html', {})
    else:
        raise Http404


def login_user(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            form = {
                'username': request.POST["username"],
                'password': request.POST["password"]
            }
            if form["username"] and form["password"]:
                try:
                    user = authenticate(username=form['username'], password=form['password'])
                    login(request, user)
                    return render(request, 'archive.html', {"posts": Article.objects.all()})
                except (PermissionError, AttributeError):
                    form['errors'] = u"Не удалось зайти"
                    return render(request, 'login.html', {'form': form})
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {})
    else:
        raise Http404
    # Create your views here.
