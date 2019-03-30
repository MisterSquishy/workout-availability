from django.contrib.auth.models import User
from .models import Check
import rest_framework
from rest_framework import viewsets
from .serializers import UserSerializer, CheckSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.settings import api_settings
from graphene_django.views import GraphQLView

class UserViewSet(viewsets.ModelViewSet):
    """Here your users be."""
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class PrivateGraphQLView(GraphQLView):
    """Adds a login requirement to graphQL API access via main endpoint."""
    def parse_body(self, request):
        if isinstance(request, rest_framework.request.Request):
            return request.data
        return super(PrivateGraphQLView, self).parse_body(request)

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(PrivateGraphQLView, cls).as_view(*args, **kwargs)
        view = permission_classes((IsAuthenticated,))(view)
        view = authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)(view)
        view = api_view(["GET", "POST"])(view)
        return view

class ChecksView(viewsets.ModelViewSet):
    """These be the checks."""
    permission_classes = (IsAuthenticated,)
    queryset = Check.objects.all().order_by('-timestamp')
    serializer_class = CheckSerializer