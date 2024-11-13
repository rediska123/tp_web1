
from django.shortcuts import render
from django.core.paginator import Paginator
import copy
from web.models import *
from django.db.models import *

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
        'current_page': current_page
    }


def new_questions_view(request):
    questions_list = question.objects.new_questions()
    current_page = paginate(questions_list, request)
    current_page_questions_list = current_page["objects_list"]
    return render(request, 'questions.html', {
        'questions_list': current_page_questions_list,
        'page': current_page["current_page"],
        'login': True
    })

def hot_questions_view(request):
    questions_list = question.objects.hot_questions()
    current_page = paginate(questions_list, request)
    current_page_questions_list = current_page["objects_list"]
    print(len(current_page_questions_list))
    return render(request, 'hot.html', {
        'questions_list': current_page_questions_list,
        'page': current_page["current_page"],
        'login': True
    })

def tagged_questions_view(request, tag_name):
    questions_list = question.objects.tagged_questions(tag_name)
    current_page = paginate(questions_list, request)
    current_page_questions_list = current_page["objects_list"]
    return render(request, 'tag.html', {
        'tag': tag_name,
        'questions_list': current_page_questions_list,
        'page': current_page["current_page"],
        'login': True
    })

def question_view(request, id):
    answers_list = answer.objects.question_answers(id)
    answered_question = question.objects.get(id=id)
    return render(request, 'question.html', {
        'question': answered_question,
        'answers_list': answers_list,
        'login': True
    })

def login_view(request):
    return render(request, 'login.html', {
        'login': False
    })

def settings_view(request):
    return render(request, 'settings.html', {
        'login': True
    })

def registration_view(request):
    return render(request, 'registration.html', {
        'login': False
    })

def new_question_view(request):
    return render(request, 'new_question.html', {
        'login': True
    })
