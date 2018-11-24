from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from .models import Question, Tag, User, Answer
from .forms import AuthForm, SignUpFrom


def get_tags_and_users():
    return Tag.objects.best_tags(), User.objects.best_users()


def paginate(objects_list, request):
    paginator = Paginator(objects_list, 10)
    page = request.GET.get('page')

    contacts = paginator.get_page(page)

    return contacts


def index(request):
    if request.method == 'POST':
        logout(request)

    question = paginate(Question.objects.get_question_by_date(), request)
    tags, users = get_tags_and_users()
    return render(request, "questions/index.html", {'questions': question, 'tags': tags, 'users': users})


def question(request, id):
    try:
        questions = Question.objects.get_question_by_id(id)
    except Question.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
    answers = Answer.objects.get_answers_by_id(questions.id)
    tags, users = get_tags_and_users()
    return render(request, "questions/oneQuestion.html", {'question': questions, 'tags': tags, 'users': users,
                                                          'answers': answers})


def tag(request, tagname):
    try:
        questions = paginate(Question.objects.get_questions_by_tag(tagname), request)
    except:
        raise Http404("No MyModel matches the given query.")
    tags, users = get_tags_and_users()
    return render(request, "questions/tagQuestions.html", {'questions': questions, 'tag': tagname,
                                                           'tags': tags, 'users': users})


def hot(request):
    question = paginate(Question.objects.get_question_by_popular(), request)
    tags, users = get_tags_and_users()
    return render(request, "questions/index.html", {'questions': question, 'tags': tags, 'users': users})


def signIn(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            print(user)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, "questions/auth.html", {'form': form})
    else:
        form = AuthForm()

    return render(request, "questions/auth.html", {'form': form})


def signUp(request):
    if request.method == 'POST':
        form = SignUpFrom(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            print(form)
    else:
        form = SignUpFrom()

    return render(request, "questions/registration.html", {'form': form})

def signOut(request):
    logout(request)
    return redirect('/')

def ask(request):
    return render(request, "questions/addQuiestion.html", {})
