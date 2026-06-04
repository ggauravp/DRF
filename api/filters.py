import django_filters
from employees.models import Employee

class EmployeeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # Filter by name (case-insensitive)
    
    class Meta:
        model = Employee
        fields = ['name']  # Specify the fields to filter on