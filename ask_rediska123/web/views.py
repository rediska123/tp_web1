
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import copy

from django.urls import reverse
from web.models import *
from django.db.models import *
from .forms import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required

import json
from django.http import JsonResponse

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = int(request.GET.get("page", 1))
    if page_number < 1:
        page_number = 1
    elif page_number > paginator.num_pages:
        page_number = paginator.num_pages
    current_page = paginator.get_page(page_number)
    return {
        'objects_list': current_page.object_list, 
        'current_page': current_page,
        'next_pages': page_number + 2,
        'last_pages': page_number - 2
    }

def question_search(request):
    search_text = request.POST.get('search_text', '')
    questions_list = question.objects.search(search_text)
    current_page = paginate(questions_list, request)
    current_page_questions_list = current_page["objects_list"]
    return render(request, 'search.html', {
        'questions_list': current_page_questions_list,
        'page': current_page,
        'search_text': search_text
    })

def new_questions_view(request):
    questions_list = question.objects.new_questions()
    current_page = paginate(questions_list, request)
    current_page_questions_list = current_page["objects_list"]
    return render(request, 'questions.html', {
        'questions_list': current_page_questions_list,
        'page': current_page,
        'login': True
    })

def hot_questions_view(request):
    questions_list = question.objects.hot_questions()
    current_page = paginate(questions_list, request)
    current_page_questions_list = current_page["objects_list"]
    print(len(current_page_questions_list))
    return render(request, 'hot.html', {
        'questions_list': current_page_questions_list,
        'page': current_page,
        'login': True
    })

def tagged_questions_view(request, tag_name):
    questions_list = question.objects.tagged_questions(tag_name)
    current_page = paginate(questions_list, request)
    current_page_questions_list = current_page["objects_list"]
    return render(request, 'tag.html', {
        'tag': tag_name,
        'questions_list': current_page_questions_list,
        'page': current_page,
        'login': True
    })

def question_view(request, id):
    answers_list = answer.objects.question_answers(id)
    answered_question = question.objects.get(id=id)
    form = AnswerForm()
    # Если нажали кнопку ответа
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        # Проверяем корректность формы
        if form.is_valid():
            author = profile.objects.get(user=request.user) # автор ответа
            form.save(author=author, answered_question=answered_question)
            form = AnswerForm() # очищаем для следующего ответа
    return render(request, 'question.html', {
        'question': answered_question,
        'answers_list': answers_list,
        'form': form
    })

def login_view(request):
    # Получаем на какую страницу перебросить после логина (параметр "next" в GET запросе), reverse - по умолчанию
    next_url = request.GET.get('next', reverse('new_questions'))
    form = LoginForm()
    # Если нажали кнопку логина
    if request.method == 'POST':
        form = LoginForm(request.POST) # Заполняем форму введенными данными
        # Проеверяем корректность формы
        if form.is_valid(): 
            user = auth.authenticate(request, **form.cleaned_data)
            # Если такой пользователь есть в системе, то авторизируемся и переходим на следующую страницу
            if user:
                auth.login(request, user)
                return redirect(next_url)
            else: # Если такого пользователя нет в системе
                form.add_error(None, 'Sorry, wrong login or password!')
    return render(request, 'login.html', {
        'form': form,
        'next_url': next_url
    })

# Добавили декоратор логина, если на страницу пытается зайти гость, то его перенаправит на страницу логина "login_url"
@login_required(login_url='login')
def settings_view(request):
    form = ProfileForm(instance=request.user) # Передаём параметр пользователя для заполнения полей
    # Если нажади на кнопку сохранения
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        # Если заполнено правильно, то сохраняем
        if form.is_valid():
            form.save()  
    return render(request, 'settings.html', {
        'form': form
    })

def registration_view(request):
    form = RegistrationForm()
    # Если нажади на кнопку регистрации
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        # Если заполнено правильно, то сохраняем
        if form.is_valid():
            user = form.save()
            user = auth.authenticate(request, **form.cleaned_data) 
            auth.login(request, user)
            return redirect(reverse('new_questions'))
    return render(request, 'registration.html', {
        'form': form
    })

# Добавили декоратор логина, если на страницу пытается зайти гость, то его перенаправит на страницу логина "login_url"
@login_required(login_url='login')
def new_question_view(request):
    form = QuestionForm()
    # Если нажали кнопку нового вопроса
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        # Проверяем корректность формы
        if form.is_valid():
            author = profile.objects.get(user=request.user) # авто вопроса
            new_question = form.save(author=author)
            return redirect('question', new_question.id) # перенаправляем на страницу нового вопроса
    return render(request, 'ask.html', {
        'form': form
    })

def logout(request):
    auth.logout(request)
    current_url = request.META.get('HTTP_REFERER', '/')
    return redirect(current_url)

def question_like_dislike(request, id):
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    if request.user == None: # Если пользватель не авторизован, то не может ставить лайки
        return JsonResponse({"error": "No auth"}, status=400)
    rating = questionlike.objects.like_dislike(id, request.user, data["like_dislike"])
    return JsonResponse({"rating" : rating})


def answer_like_dislike(request, id):
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    if request.user == None: # Если пользватель не авторизован, то не может ставить лайки
        return JsonResponse({"error": "No auth"}, status=400)
    rating = answerlike.objects.like_dislike(id, request.user, data["like_dislike"])
    return JsonResponse({"rating" : rating})

def correct_answer(request, id):
    user = request.user
    answer.objects.correct(user, id)
    return JsonResponse({"status": "OK"}, status=200)