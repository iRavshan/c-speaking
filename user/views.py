from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm
from .decorators import teacher_access
from speaking.models import Attempt, Topic, Feedback, QAPair

@login_required
def practices(request):
    response_answers = []
    attempts = Attempt.objects.filter(user=request.user)
    for attempt in attempts:
        qa_pair = QAPair.objects.filter(attempt=attempt).first()
        topic = qa_pair.question.topic
        response_answers.append({
            'id': attempt.id,
            'finished_at': attempt.finished_at,
            'part': attempt.part,
            'score': attempt.score,
            'topic': topic.name,
        })
    context = {
        'answers': response_answers
    }
    return render(request, 'user/practices.html', context)


@login_required
def get_answer(request, answer_id):
    attempt = Attempt.objects.get(id=answer_id, user=request.user)
    if attempt is not None:
        qa_pairs = QAPair.objects.filter(attempt=attempt.id)
        context = {
            'answer': {
                'score': attempt.score,
                'questions': qa_pairs,
                'topic': qa_pairs.first().question.topic.name
            },
        }
        if attempt.is_marked:
            feedback = Feedback.objects.get(attempt=attempt)
            context['feedback'] = feedback
        return render(request, 'user/answer.html', context)


@login_required
@teacher_access
def attempts(request):
    status = request.GET.get('status', 'unchecked')
    if status == 'checked':
        attempts = Attempt.objects.filter(is_marked=True)
    else:
        attempts = Attempt.objects.filter(is_marked=False)
    context = {
        'attempts': attempts
    }
    return render(request, 'user/attempts.html', context)


@login_required
@teacher_access
def check_attempt(request, attempt_id):
    attempt = Attempt.objects.get(id=attempt_id)
    
    if request.method == 'POST':
        score = request.POST.get('score')
        feedback_text = request.POST.get('feedback')
        feedback = Feedback(attempt=attempt, text=feedback_text)
        feedback.save()
        attempt.score = score
        attempt.is_marked = True
        attempt.save()

        return redirect('attempts')

    else:
        if attempt is not None:
            qa_pairs = QAPair.objects.filter(attempt=attempt)
            context = {
                'attempt': {
                    'id': attempt.id,
                    'user': attempt.user,
                    'part': attempt.part,
                    'score': attempt.score,
                    'qa_pairs': qa_pairs,
                    'topic': qa_pairs.first().question.topic.name
                }
            }
        return render(request, 'user/check_attempt.html', context)
    

@login_required
@teacher_access
def get_attempt(request, attempt_id):
    attempt = Attempt.objects.get(id=attempt_id)

    if request.method == 'POST':
        score = request.POST.get('score')
        feedback_text = request.POST.get('feedback')

        Feedback.objects.filter(attempt=attempt).delete()

        attempt.score = score
        attempt.save()

        feedback = Feedback(attempt=attempt, text=feedback_text)
        feedback.save()

        return redirect('attempts')

    else:
        if attempt is not None:
            qa_pairs = QAPair.objects.filter(attempt=attempt)
            context = {
                'attempt': {
                    'id': attempt.id,
                    'user': attempt.user,
                    'part': attempt.part,
                    'score': attempt.score,
                    'qa_pairs': qa_pairs,
                    'topic': qa_pairs.first().question.topic.name
                }
            }
        return render(request, 'user/check_attempt.html', context)

    

def Register(request):
    context = {}
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            try:
                instance = form.save(commit=True)
                instance.save()
                user = authenticate(request, username=username, password=password)
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