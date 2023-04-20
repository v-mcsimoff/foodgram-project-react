from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Кастомный пагинатор для установки лимита."""

    page_size_query_param = 'limit'
