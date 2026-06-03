from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 3  # Default page size
    # page_size_query_param = 'page_size'  # Allow client to set page size
    max_page_size = 100  # Maximum page size allowed
    page_query_param = 'page_number'  # Query parameter for page number

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count, # Total objects in queryset
            'results': data,
            'page_size': self.page_size, # Number of objects per page
        })