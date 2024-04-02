import boto3
from uuid import uuid4
from datetime import datetime
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from user.decorators import user_access
from .models import Topic, Question, Attempt, QAPair

@login_required
@user_access
def Mock(request):
    questions = Question.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'speaking/mock.html', context)


@login_required
def Part1(request):
    context = {}
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        if int(topic_id) == -1:
           random_topic = Topic.objects.filter(question__part='1').distinct().order_by('?').first()
           topic_id = random_topic.id 
        random_questions = Question.objects.filter(topic_id=topic_id, part='1').order_by('?')[:6]
        if random_questions is not None:
            context['questions'] = random_questions
            return render(request, 'speaking/part1/part1.html', context)
    
    context['topics'] = Topic.objects.filter(question__part='1').distinct()
    return render(request, 'speaking/part1/topics.html', context)


@login_required
@user_access
def Part2(request):
    question = Question.objects.get(id=9)
    context = {
        'question': question,
    }
    return render(request, 'speaking/part2/part2.html', context)


@login_required
@user_access
def Part3(request):
    context = {}

    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        if int(topic_id) == -1:
           random_topic = Topic.objects.filter(question__part='3').distinct().order_by('?').first()
           topic_id = random_topic.id
        random_questions = Question.objects.filter(topic_id=topic_id, part='3').order_by('?')[:6]
        if random_questions is not None:
            context['questions'] = random_questions
            return render(request, 'speaking/part3/part3.html', context)            
    
    context['topics'] = Topic.objects.filter(question__part='3').distinct()
    return render(request, 'speaking/part3/topics.html', context)


@login_required
def save_answers(request):
    if request.method == 'POST':

        part = request.POST.get('part')
        question_ids = request.POST.getlist('questions')
        answers = request.FILES.getlist('answers')
        
        print(part)
        print(question_ids)
        
        attempt = Attempt(user=request.user, part=part, finished_at=datetime.now())
        attempt.save()

        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_S3_REGION_NAME)

        for i, question_id in enumerate(question_ids):
            question = Question.objects.get(id=question_id)

            new_id = uuid4()
            file_name = f"{new_id}.wav"
            s3_key = f"media/attempts/{attempt.id}/{file_name}"

            s3.upload_fileobj(answers[i], settings.AWS_STORAGE_BUCKET_NAME, s3_key)

            qa_pair = QAPair(answer_id=new_id, question=question, attempt=attempt)
            qa_pair.save()

    return redirect('user/practices')
    
def submitted(request):
    return render(request, 'speaking/submitted.html')