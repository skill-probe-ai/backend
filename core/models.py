# Create your models here.

from django.contrib.auth.models import User
from django.db import models

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Resume"
    

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    verification_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class InterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    total_questions = models.IntegerField(default=5)
    current_question_index = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
class Question(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE)
    text = models.TextField()
    difficulty = models.CharField(
        max_length=20,
        choices=[("easy", "easy"), ("medium", "medium"), ("hard", "hard")],
        default="medium"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    improvement = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    