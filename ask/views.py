import json

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from ask.forms import LoginForm, RegisterForm, AvatarForm, AnswerForm, QuestionForm, PictureForm
from ask.models import Question, Answer, Tag, Profile


class N:
    def __init__(self, n=0, dots=False):
        self.n = n
        self.dots = dots


def paginate(url, entity, page, count, **kwargs):
    def l(st, e):
        return list(map(lambda n: N(n), range(st, e + 1)))

    pcount = 7
    paginator = Paginator(entity, count)

    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
        page = 1
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    start = 1
    end = paginator.num_pages
    page = int(page)

    if end - start < pcount + 2:
        numbers = l(start, end)
    elif page - start < (pcount + 3) // 2:
        numbers = l(start, pcount + 2) + [N(pcount + 3, dots=True), N(end)]
    elif page >= end - pcount // 2 - 1:
        numbers = [N(start), N(end - pcount - 2, dots=True)] + l(end - pcount - 1, end)
    else:
        numbers = [N(start), N(page - pcount // 2 - 1, dots=True)] + \
                  l(page - pcount // 2, page + pcount // 2) + [N(page + pcount // 2 + 1, dots=True), N(end)]
    kwargs.update({'url': url, 'list': qs, 'numbers': numbers, 'show': len(numbers) > 1, 'sel': page})
    return kwargs


def empty(request):
    return redirect('index', sort='new')


def index(request, sort):
    print("1231")
    if sort != 'new' and sort != 'hot': return redirect('index', sort='new')
    return render(request, 'ask/index.html',
                  paginate(reverse('index', kwargs={'sort': sort}),
                           Question.objects.new() if sort == 'new' else Question.objects.hot(),
                           request.GET.get('page', 1), 3, sort=sort,
                           title='Все вопросы', popular_tags=Tag.objects.popular_tags(),
                           url_new='' if sort == 'new' else reverse('index', kwargs={'sort': 'new'}),
                           url_hot='' if sort == 'hot' else reverse('index', kwargs={'sort': 'hot'})))


def tag(request, tag, sort):
    if sort != 'new' and sort != 'hot': return redirect('tag', tag=tag, sort='new')

    return render(request, 'ask/index.html',
                  paginate(reverse('tag', kwargs={'tag': tag, 'sort': sort}),
                           Question.objects.new_tag(tag) if sort == 'new' else Question.objects.hot_tag(tag),
                           request.GET.get('page', 1), 3, tag=tag, sort=sort,
                           title='Вопросы по тегу {}'.format(tag), popular_tags=Tag.objects.popular_tags(),
                           url_new='' if sort == 'new' else reverse('tag', kwargs={'tag': tag, 'sort': 'new'}),
                           url_hot='' if sort == 'hot' else reverse('tag', kwargs={'tag': tag, 'sort': 'hot'})))


def question(request, id=0):
    question = get_object_or_404(Question, pk=id)
    answers = Answer.objects.filter(question=question)
    if request.POST:
        form = AnswerForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            answer = form.save(question, request.user)
            return HttpResponseRedirect(
                request.path + "?page=" + str(list(answers).index(answer) % 5) + "#" + str(answer.id))
        else:
            return render(request, 'ask/question.html',
                          paginate(reverse('question', kwargs={'id': id}),
                                   answers, request.GET.get('page', 1),
                                   5, question=question,
                                   popular_tags=Tag.objects.popular_tags(), form=form))

    else:
        form = AnswerForm()
        return render(request, 'ask/question.html',
                      paginate(reverse('question', kwargs={'id': id}),
                               answers, request.GET.get('page', 1),
                               5, question=question,
                               popular_tags=Tag.objects.popular_tags(), form=form))


def ask(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    if request.POST:
        p = Profile.objects.get(user=request.user)
        form = QuestionForm(request.POST, author=p)
        picture_form = PictureForm(request.POST, request.FILES)
        if form.is_valid() and picture_form.is_valid():
            title = form.cleaned_data.get('title')
            text = form.cleaned_data.get('text')
            picture = picture_form.cleaned_data.get('picture')
            print(picture)
            question = Question(title=title, text=text, picture=picture, author=request.user)
            question.save()
            tags = form.cleaned_data.get('tags')
            for t in tags.split(" "):
                if not t:
                    continue
                try:
                    tag = Tag.objects.get(name=t)
                except Tag.DoesNotExist:
                    tag = Tag(name=t)
                    tag.save()
                question.tags.add(tag)
                question.save()
            return HttpResponseRedirect('/question/' + str(question.id))
        else:
            return render(request, 'ask/ask.html', {'form': form, 'picture_form': picture_form})
    else:
        form = QuestionForm()
        picture_form = PictureForm()
        return render(request, 'ask/ask.html', {'form': form, 'picture_form': picture_form})


def register(request):
    return render(request, 'ask/register.html', {'popular_tags': Tag.objects.popular_tags()})


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                redirect = form.cleaned_data.get('redirect', '/none?')
                if redirect == '/login/' or redirect == '/signup/':
                    redirect = '/'
                return HttpResponseRedirect(redirect)
            else:
                error = u'Неверная связка логин-пароль'
                return render(request, 'ask/login.html', {'form': form, 'error': error})
        else:
            return render(request, 'ask/login.html', {'form': form})

    else:
        form = LoginForm()
        return render(request, 'ask/login.html', {'form': form})


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.POST:
        form = RegisterForm(request.POST)
        avatar_form = AvatarForm(request.POST, request.FILES)
        if form.is_valid() and avatar_form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            avatar = avatar_form.cleaned_data.get('avatar')
            user = User.objects.create_user(username=username, email=email, password=password)
            profile = Profile(user=user, avatar=avatar)
            profile.save()
            us = authenticate(username=username, password=password)
            auth_login(request, us)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'ask/register.html', {'form': form, 'avatar_form': avatar_form})
    else:
        form = RegisterForm()
        avatar_form = AvatarForm()
        return render(request, 'ask/register.html', {'form': form, 'avatar_form': avatar_form})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


def rate(request):
    response_data = {}

    if request.POST and 'tp' in request.POST:
        id = int(request.POST['tp'][1:])
        q = Question.objects.get(pk=id)
        q.rating += 1 if request.POST['tp'][0] == 'p' else -1
        q.save()
        response_data['new'] = q.rating

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return HttpResponse(json.dumps(response_data), content_type="application/json")
