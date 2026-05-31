from django.urls import path, include
from . import views

urlpatterns = [
    path('students/', views.studentsview), # this is for function based view
    path('students/<int:id>/', views.studentdetailview),

    path('employees/', views.EmployeesView.as_view()), # this is for class based view, we need to call as_view() method to convert class based view into function based view
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view()),
]