import graphene
import graphql_jwt
import cities.schema
import shortener.schema

class Query(cities.schema.Query, 
            shortener.schema.Query, 
            graphene.ObjectType, 
):
    pass 

class Mutation(cities.schema.Mutation, 
            shortener.schema.Mutation, 
            graphene.ObjectType, 
): 
    token_auth = graphql_jwt.ObtainJSONWebToken.Field() 
    verify_token = graphql_jwt.Verify.Field() 
    refresh_token = graphql_jwt.Refresh.Field() 

schema = graphene.Schema(query=Query, mutation=Mutation)
