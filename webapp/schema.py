import graphene

import checks.schema

class Query(checks.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
