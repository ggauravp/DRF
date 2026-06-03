# Serializer, Nested Serializer
# Function Based View
# Class Based View
# ApiView
# Mixins
# Generic View
# Viewsets
# Model Viewsets
# Pagination 
- Global when you configure pagination globally in settings.py, it automatically works for GenericAPIView-based views and ViewSets (including ModelViewSet, ListAPIView, etc)
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
