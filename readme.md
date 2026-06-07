# DRF Serializers

A **Serializer** in Django REST Framework (DRF) acts as a bridge between Python objects and JSON data. It is responsible for converting complex data types into JSON and validating incoming data before creating or updating objects.

## Main Uses of Serializers

### 1. Serialization (Python → JSON)

Converts model instances or querysets into JSON format for API responses.
```bash
book = Book.objects.first()
serializer = BookSerializer(book)

serializer.data
```
### 2. Deserialization (JSON → Python)

Converts incoming JSON data into Python objects.
```bash
serializer = BookSerializer(data=request.data)
```
### 3. Data Validation

Validates incoming request data before creating or updating it.
```bash
if serializer.is_valid():
    serializer.save()
```

### 4. Object Creation

Creates new database records using validated data.
```bash 
serializer.save() 
```

### 5. Object Update

Updates existing database records using validated data.
```bash
serializer = BookSerializer(book, data=request.data)

if serializer.is_valid():
    serializer.save()
```

## Useful Serializer Attributes

* `serializer.data` – Serialized output data
* `serializer.errors` – Validation errors
* `serializer.validated_data` – Clean validated input data
* `serializer.save()` – Creates or updates an object

---

# Nested Serializers

Nested serializers are used to include related model data inside the serialized output.
* Example model
```bash
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )
```

## Without Nested Serializer

```json
{
    "id": 1,
    "title": "Django",
    "author": 5
}
```

Only the related object's ID is returned.

## With Nested Serializer
```bash
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = "__all__"
```

```json
{
    "id": 1,
    "title": "Django",
    "author": {
        "id": 5,
        "name": "John"
    }
}
```

The complete related object details are included in the response.

## Benefits of Nested Serializers

* Include related object details in a single API response.
* Reduce additional API calls from the frontend.
* Improve API readability and usability.

# Function-Based Views (FBV) vs Class-Based Views (CBV) in DRF

Views handle incoming HTTP requests and return responses. DRF provides two main ways to build API views:

## Function-Based Views (FBV)

Function-Based Views are regular Python functions that handle requests.

### Example

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def book_list(request):
    return Response({"message": "List of books"})
```

### Advantages

* Easy to understand and write.
* Good for simple APIs.
* Suitable for beginners.

### Disadvantages

* Repetitive code for CRUD operations.
* Difficult to maintain as the project grows.
* Less reusable.

---

## Class-Based Views (CBV)

Class-Based Views organize request handling inside classes.

### Example

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class BookListView(APIView):

    def get(self, request):
        return Response({"message": "List of books"})
```

### Advantages

* Better code organization.
* Reusable through inheritance.
* Easier to extend and maintain.
* Preferred for larger projects.

### Disadvantages

* Slightly more complex than FBVs.
* Requires understanding of OOP concepts.

---

# DRF Class-Based View Hierarchy

## 1. APIView

The base class for all DRF class-based views.

```python
class BookView(APIView):

    def get(self, request):
        pass

    def post(self, request):
        pass
```

Provides:

* Request parsing
* Authentication
* Permissions
* Throttling
* Content negotiation

---

## 2. GenericAPIView

Extends APIView and adds common functionality.

Provides:

* `queryset`
* `serializer_class`
* `get_queryset()`
* `get_serializer()`

Example:

```python
class BookView(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

---

## 3. Mixins

Mixins provide reusable CRUD functionality.

### Available Mixins

* `ListModelMixin` → List objects
* `RetrieveModelMixin` → Retrieve single object
* `CreateModelMixin` → Create object
* `UpdateModelMixin` → Update object
* `DestroyModelMixin` → Delete object

Example:

```python
class BookListView(
    GenericAPIView,
    ListModelMixin
):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request):
        return self.list(request)
```

---

## 4. Generic Views

DRF combines GenericAPIView and Mixins into ready-made views.

### Common Generic Views

* `ListAPIView`
* `CreateAPIView`
* `RetrieveAPIView`
* `UpdateAPIView`
* `DestroyAPIView`
* `ListCreateAPIView`
* `RetrieveUpdateAPIView`
* `RetrieveDestroyAPIView`
* `RetrieveUpdateDestroyAPIView`

Example:

```python
class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

---

## 5. ViewSets

A ViewSet groups related actions into a single class.

```python
from rest_framework.viewsets import ModelViewSet

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

Provides all CRUD operations automatically:

* list()
* retrieve()
* create()
* update()
* partial_update()
* destroy()

---

# View Progression in DRF

```text
Function-Based View
        ↓
APIView
        ↓
GenericAPIView
        ↓
Mixins
        ↓
Generic Views
        ↓
ViewSets
```

As you move downward, DRF provides more built-in functionality and reduces boilerplate code.

---

# When to Use What?

| View Type               | Use Case                         |
| ----------------------- | -------------------------------- |
| Function-Based View     | Small or simple APIs             |
| APIView                 | Custom request handling          |
| GenericAPIView + Mixins | Custom CRUD behavior             |
| Generic Views           | Standard CRUD operations         |
| ViewSet / ModelViewSet  | Full REST APIs with minimal code |


Most real-world DRF projects use **Generic Views** and **ViewSets** because they reduce boilerplate code and improve maintainability.

# Pagination 
### Global
when you configure pagination globally in settings.py, it automatically works for GenericAPIView-based views and ViewSets (including ModelViewSet, ListAPIView, etc)
### Custom Pagination

A custom pagination class is implemented using `PageNumberPagination`.

```python
class CustomPagination(PageNumberPagination):
    page_size = 3  # Default page size
    page_size_query_param = 'page_size'
```

* `page_size` defines the default number of records returned per page.
* `page_size_query_param` allows clients to override the default page size through the URL.

Example:

```http
/api/books/?page=1&page_size=5
```

The above request returns 5 records instead of the default 3.

The paginated response can be customized by overriding `get_paginated_response()`:

```python
def get_paginated_response(self, data):
    return Response({
        "page_size": self.page_size,
        "count": self.page.paginator.count,
        "results": data
    })
```

* `self.page_size` returns the default page size configured in the pagination class.
* `self.page.paginator.count` returns the total number of records in the queryset.
* `results` contains the records for the current page.

# Filters
### Global Filter
### Custom Filter
- lookup_expr='icontains', 'iexact'
- RangeFilter only works integer field