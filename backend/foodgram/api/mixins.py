from rest_framework import mixins, viewsets


class RetrieveListViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """Viewset to retrieve either a list or a single item."""

    pass
