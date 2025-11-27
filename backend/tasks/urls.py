from django.urls import path
from .views import AnalyzeTasks, SuggestTasks
from . import views

urlpatterns = [
    path('analyze/', AnalyzeTasks.as_view(), name='tasks-analyze'),
    path('suggest/', SuggestTasks.as_view(), name='tasks-suggest'),
    path('cycles/', views.check_cycles, name='check_cycles'), 
]
