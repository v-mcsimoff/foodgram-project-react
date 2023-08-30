from rest_framework import pagination


class PageLimitPagination(pagination.PageNumberPagination):
    """Custom paginator to set the limit."""

    page_size_query_param = 'limit'
