from rest_framework.pagination import PageNumberPagination

class MyPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'records' #support & and client can decide  ?page=1&records=10 it shows per page 10 record
    max_page_size = 10
    last_page_strings = 'last'
