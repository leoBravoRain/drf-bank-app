from rest_framework.pagination import PageNumberPagination


class TransactionsPaginator(PageNumberPagination):
    page_size = 3
