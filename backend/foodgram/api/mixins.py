from rest_framework import mixins, viewsets


class RetrieveListViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """Вьюсет для получения либо списка, либо одного эл-та."""

    pass
