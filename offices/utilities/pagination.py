from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination

class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param = "limit" #upto data
    offset_query_param = "offset" #which page
    max_limit = 5000

class MyPageNumberPagination(PageNumberPagination):
    page_size = 20  # Set your desired page size
    page_size_query_param = 'size'
    max_page_size = 5000  # Set the maximum page size