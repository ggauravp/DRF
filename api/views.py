from django.shortcuts import render
from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
# Create your views here.


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