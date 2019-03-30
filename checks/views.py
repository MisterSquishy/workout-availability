from django.contrib.auth.models import User
from .models import Check
from rest_framework import viewsets
from .serializers import UserSerializer, CheckSerializer
from rest_framework.permissions import IsAuthenticated
from graphene_django.views import GraphQLView

class UserViewSet(viewsets.ModelViewSet):
    """Here your users be."""
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PrivateGraphQLView(GraphQLView):
    """Adds a login requirement to graphQL API access via main endpoint."""
    permission_classes = (IsAuthenticated,)
    pass

class ChecksView(viewsets.ModelViewSet):
    """These be the checks."""
    permission_classes = (IsAuthenticated,)
    queryset = Check.objects.all().order_by('-timestamp')
    serializer_class = CheckSerializer