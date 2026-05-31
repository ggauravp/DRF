from asyncio import mixins

from django.shortcuts import render
from django.http import Http404, JsonResponse
from students.models import Student
from .serializers import StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .serializers import EmployeeSerializer
from employees.models import Employee
from rest_framework import generics
from rest_framework import mixins

@api_view(['GET', 'POST'])
def studentsview(request):
    #students = Student.objects.all()
    #print(students)
   
   # return JsonResponse(students) --> In order to allow non-dict objects to be serialized set the safe parameter to False.
   # return JsonResponse(students, safe=False) --> Object of type QuerySet is not JSON serializable

   # Now we can either manually serialize the data using list comprehension OR
   # we can use Django's built-in serializers to convert the QuerySet into a JSON format.
   
    # Manual serialization using list comprehension
    #students_list = list(students.values())  # Convert QuerySet to a list of dictionaries
    #return JsonResponse(students_list, safe=False)

    # Using Django's built-in serializers

    if request.method == 'GET':
        students = Student.objects.all()
        students_json = StudentSerializer(students, many=True)
        return Response(students_json.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
      data = StudentSerializer(data=request.data)
      if data.is_valid():
          data.save()
          return Response(data.data, status=status.HTTP_201_CREATED)
      return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def studentdetailview(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        student_json = StudentSerializer(student)
        return Response(student_json.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        student_json = StudentSerializer(student, data= request.data)
        if student_json.is_valid():
            student_json.save()
            return Response(student_json.data, status=status.HTTP_200_OK)
        else:
            return Response(student_json.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == "DELETE":
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# class EmployeesView(APIView):  # inherit from APIView to create a class-based view. APIView provides methods for handling HTTP requests and responses, making it easier to create RESTful APIs.
#     def get(self, request):
#         employees = Employee.objects.all()
#         employees_json = EmployeeSerializer(employees, many=True)
#         return Response(employees_json.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         data = EmployeeSerializer(data=request.data)
#         if data.is_valid():
#             data.save()
#             return Response(data.data, status=status.HTTP_201_CREATED)
#         return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class EmployeeDetailView(APIView):
#     def get_object(self, id):
#         try:
#             return Employee.objects.get(id=id)
#         except Employee.DoesNotExist:
#             raise Http404

#     def get(self, request, id):
#         employee = self.get_object(id) # self is used to call another method of the same class 
#         if employee is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         employee_json = EmployeeSerializer(employee)
#         return Response(employee_json.data, status=status.HTTP_200_OK)

#     def put(self, request, id):
#         employee = self.get_object(id) 
#         if employee is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         employee_json = EmployeeSerializer(employee, data=request.data)
#         if employee_json.is_valid():
#             employee_json.save()
#             return Response(employee_json.data, status=status.HTTP_200_OK)
#         else:
#             return Response(employee_json.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         employee = self.get_object(id)
#         if employee is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# MIXINS
"""
class EmployeesView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    
class EmployeeDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)
    
    def put(self, request, pk):
        return self.update(request, pk=pk)

    def delete(self, request, pk):
        return self.destroy(request, pk=pk)
"""

# GENERIC VIEWS

class EmployeesView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'  # Specify the field to use for lookup (default is 'pk')