import uuid
from django.db import models
from user.models import User

PARTS = ( 
    ("1", "1"), 
    ("2", "2"), 
    ("3", "3"),
    ("4", "all parts"),
) 


class Topic(models.Model):
    name = models.CharField('name', max_length=30, unique=True, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False, auto_created=True)
    title = models.CharField('title', max_length=200, unique=True)
    topic = models.ForeignKey(Topic, null=True, on_delete=models.SET_NULL)
    part = models.CharField(max_length=20, choices=PARTS, default='1', null=False)

    class Meta:
        ordering = ['topic']

    def __str__(self):
        return self.title
    

class Attempt(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    finished_at = models.DateTimeField(auto_created=True, auto_now=True, editable=False)
    part = models.CharField(max_length=20, choices=PARTS, default='1', null=False)
    score = models.PositiveIntegerField(null=True, blank=True)
    is_marked = models.BooleanField(null=False, default=False)

    class Meta:
        ordering = ['-finished_at']
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.finished_at}'
    

class QAPair(models.Model):
    id=models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    answer_id = models.UUIDField(null=False)
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE)
    attempt = models.ForeignKey(Attempt, null=False, on_delete=models.CASCADE)


class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    attempt = models.ForeignKey(Attempt, null=False, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    is_read = models.BooleanField(null=False, default=False)



