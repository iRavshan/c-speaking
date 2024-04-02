from django.contrib import admin
from .models import Topic, Question, Feedback, Attempt, QAPair

admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Feedback)
admin.site.register(Attempt)
admin.site.register(QAPair)
