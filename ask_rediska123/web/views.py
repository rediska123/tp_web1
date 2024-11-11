
from django.shortcuts import render
from django.core.paginator import Paginator
import copy
import random

questions_list = []
for i in range(1,30):
  questions_list.append({
    'title': 'title' + str(i),
    'id': i,
    'text': 'text' + str(i),
    'tags': ['tag'+str(i), 'tag'+str(i+1), 'tag'+str(i+2)]
  })
answers_list = []
for i in range(30):
    answers_list.append([])
    for j in range(5):
        answers_list[i].append({
        'id': i*5 + j,
        'text': 'text' + str(i*5 + j),
        'flag': random.choice(["", "checked"])
        })

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, 10)
    page_number = int(request.GET.get("page", 1))
    if page_number < 1:
        page_number = 1
    elif page_number > paginator.num_pages:
        page_number = paginator.num_pages
    current_page = paginator.get_page(page_number)
    return {
        'questions_list': current_page.object_list, 
        'current_page': current_page
    }


def questions(request):
    current_page = paginate(questions_list, request)
    data = []
    current_page_questions_list = current_page["questions_list"]
    for i in range(len(current_page_questions_list)):
        data.append({
            "question": current_page_questions_list[i],
            "answers_amount": len(answers_list[current_page_questions_list[i]['id']])
        })
    print(data)
    return render(request, 'questions.html', {
        'data': data,
        'page': current_page["current_page"],
        'login': True
    })

def hot_questions(request):
    hot_questions_list = copy.deepcopy(questions_list)
    hot_questions_list.reverse()
    current_page = paginate(hot_questions_list, request)
    data = []
    current_page_questions_list = tuple(current_page["questions_list"])
    for i in range(len(current_page_questions_list)):
        data.append({
            "question": current_page_questions_list[i],
            "answers_amount": len(answers_list[current_page_questions_list[i]['id']])
        })
    return render(request, 'hot.html', {
        'data': data,
        'page': current_page["current_page"],
        'login': True
    })

def tagged_questions(request, tag):
    data = []
    for i in questions_list:
        if tag in i['tags']:
            data.append({
                "question": i,
                "answers_amount": len(answers_list[i['id']])
            })
    current_page = paginate(data, request)
    return render(request, 'questions.html', {
        'data': data,
        'page': current_page["current_page"],
        'login': True
    })

def question(request, id):
    print(answers_list)
    return render(request, 'question.html', {
        'title': questions_list[id-1]['title'],
        'question': questions_list[id-1],
        'answers_list': answers_list[id-1],
        'login': True
    })

def login(request):
    return render(request, 'login.html', {
        'login': False
    })

def settings(request):
    return render(request, 'settings.html', {
        'login': True
    })

def registration(request):
    return render(request, 'registration.html', {
        'login': False
    })

def new_question(request):
    return render(request, 'new_question.html', {
        'login': True
    })
