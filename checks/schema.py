import graphene
from graphene_django import DjangoObjectType

from .models import Check


class CheckType(DjangoObjectType):
    class Meta:
        model = Check


class Query(graphene.ObjectType):
    checks = graphene.List(CheckType)

    def resolve_checks(self, info, **kwargs):
        return Check.objects.all()