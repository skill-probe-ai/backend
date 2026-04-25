from django.urls import path
from .views import ResumeView,StartInterviewView, SubmitAnswerView

urlpatterns = [
    path('resume/', ResumeView.as_view()),
    path('interview/start/', StartInterviewView.as_view()),
    path('answer/submit/', SubmitAnswerView.as_view()),
]