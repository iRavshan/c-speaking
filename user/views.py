from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm
from speaking.models import Answer, Topic, Feedback

@login_required
def practices(request):
    response_answers = []
    answers = Answer.objects.filter(user=request.user)
    for answer in answers:
        topic = (answer.questions.all()[0]).topic
        response_answers.append({
            'id': answer.id,
            'finished_at': answer.finished_at,
            'part': answer.part,
            'score': answer.score,
            'topic': topic.name,
        })
    context = {
        'answers': response_answers
    }
    return render(request, 'user/practices.html', context)


@login_required
def get_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id, user=request.user)
    if answer is not None:
        feedback = Feedback.objects.get(answer=answer)
        context = {
            'answer': {
                'score': answer.score,
                'questions': answer.questions.all(),
                'topic': (answer.questions.all()[0]).topic.name
            },
            'feedback': feedback
        }
        return render(request, 'user/answer.html', context)


def Register(request):
    context = {}
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password1']
            try:
                instance = form.save(commit=True)
                instance.save()
                user = authenticate(request, username=phone, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
            except:
                context['form'] = form
                return render(request, 'user/register.html', context)
        else:
            context['form'] = form
            return render(request, 'user/register.html', context)
    context['form'] = UserRegistrationForm()
    return render(request, 'user/register.html', context)


def Login(request):
    if request.method == "POST":
        username = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        messages.error(request, 'Foydalanuvchi nomi yoki parol xato')
        return redirect('login')
    return render(request, 'user/login.html')


@login_required
def Logout(request):
    logout(request)
    return render(request, 'user/login.html')