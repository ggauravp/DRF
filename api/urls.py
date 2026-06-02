from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router =  DefaultRouter()
router.register("employees", views.Employeeviewset, basename='employee') # we need to specify the basename if we are not using queryset in the viewset, if we are using queryset then we don't need to specify the basename

urlpatterns = [
    path('students/', views.studentsview), # this is for function based view
    path('students/<int:id>/', views.studentdetailview),

    # path('employees/', views.EmployeesView.as_view()), # this is for class based view, we need to call as_view() method to convert class based view into function based view
    # path('employees/<int:pk>/', views.EmployeeDetailView.as_view()),

    path('', include(router.urls)), # this is for viewsets, we need to include the router urls to the urlpatterns

    path('blogs/', views.BlogsViewset.as_view()), # this is for blogs viewset
    path('comments/', views.CommentViewset.as_view()), # this is for comments viewset

    path('blogs/<int:pk>/', views.BlogDetailView.as_view()), # this is for blog detail view
]