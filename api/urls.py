from django.urls import path, include
from . import views

urlpatterns = [
    path('students/', views.studentsview),
    path('students/<int:id>/', views.studentdetailview)
]