from django.shortcuts import render
from django.contrib.auth.decorators import login_required   
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from random import sample, shuffle
from models import Question, QuestionPaper
from django.core.urlresolvers import reverse
from django.conf import settings
from json import dumps

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the ncqs index.")

# this handles the registration part of the user
def register_view(request):
    if request.method=="POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            username = request.POST.get('username')
            password = request.POST.get('password')
            print "username:",username,"password",password
            return login_user(request, username, password)
    else:
        form = UserRegistrationForm()
    return render(request, 'ncqs/register.html', {'form':form})

@csrf_exempt
def login_view(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print "username:",username,"password",password
        return login_user(request, username, password)
    return render(request, 'ncqs/login.html')


'''
helper function to log the user in for
    newly registered users
    existing users
'''
def login_user(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/ncqs/start")
        else:
            return HttpResponse("Your account is disabled!")
    else:
        return HttpResponse('invalid login!')

def logout_view(request):
    logout_string = "You are already logged out!"
    if request.user.is_authenticated(): #check if user is authenticated here
        logout(request)
        logout_string = "Successfully logged out!"
        #return HttpResponse("You were logged out!")
    return HttpResponse(logout_string+' <a href = "'+reverse("login")+'">Login again</a>')

@login_required()
def start_view(request):
    if request.user.is_authenticated():
        return render(request, "ncqs/start.html")

    else:   
        return HttpResponseRedirect(request, "/ncqs/login")

def get_question_list(index, qtype, user):
    question_objects = Question.objects.all().filter(question_type=qtype)
    question_list = []
    for i in index:
        question_object = question_objects[i]
        QuestionPaper.objects.get_or_create(user = user, question = question_object)
        question_dict = {}
        choices = [question_object.choice_correct, question_object.choice1, question_object.choice2, question_object.choice3]
        shuffle(choices)
        question_dict['question'] = question_object.question
        question_dict['choices'] = choices
        question_list.append(question_dict)
    return question_list;

def make_question_paper(user):
    easy_question_index = sample(range(settings.NCQS_TOTAL_EASY_QUESTIONS),settings.NCQS_SOLVABLE_EASY_QUESTIONS)
    hard_question_index = sample(range(settings.NCQS_TOTAL_HARD_QUESTIONS), settings.NCQS_SOLVABLE_HARD_QUESTIONS)
    easy_question = get_question_list(easy_question_index, 'EASY', user)
    print "easy questions:\n"+str(easy_question);
    hard_question = get_question_list(hard_question_index, 'HARD', user)
    print "hard questions:\n"+str(hard_question)
    final_question_list = easy_question + hard_question
    return final_question_list
 
@login_required   
def fetch_questions_ajax(request):
    current_user = request.user
    question_list = make_question_paper(current_user)
    # add a session variable here that keeps track whether we are making
    # the paper for the first time or not, otherwise every page refresh
    # will result in making of new question paper for this particular user
    data = {"data":question_list}
    return JsonResponse(data);

def delete_record_view(request, username='murtraja'):
    try:
        entries = QuestionPaper.objects.all().filter(user = User.objects.get(username=username)).delete()
    except Exception as e:
        return HttpResponse("error deleting records for username "+username+". "+str(e))
    return HttpResponse("Successfully deleted records for "+username);

@csrf_exempt
def record_answer_view(request):
    index = int(request.POST.get("question_no"));
    answer = request.POST.get("answer");
    qp_object = QuestionPaper.objects.all().filter(user = request.user)[index]
    print qp_object
    qp_object.user_answer = answer
    qp_object.save();
    return HttpResponse(dumps({"success":True}));
