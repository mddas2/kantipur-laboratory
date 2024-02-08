from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination

class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 5000

class MyPageNumberPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 5000
    page_size_query_param = 'size'