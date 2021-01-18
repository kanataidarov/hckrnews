import graphene
from graphene_django import DjangoObjectType
from .models import URL
from django.db.models import Q 

class URLType(DjangoObjectType): 
    class Meta: 
        model = URL 

class Query(graphene.ObjectType): 
    urls = graphene.List(URLType, url=graphene.String(), 
            first=graphene.Int(), skip=graphene.Int()) 

    def resolve_urls(self, info, url=None, first=None, skip=None, **kwargs): 
        querySet = URL.objects.all()

        if url: 
            _filter = Q(full_url__icontains=url) 
            querySet = querySet.filter(_filter) 

        if first: 
            querySet = querySet[:first]
        
        if skip: 
            querySet = querySet[skip:]

        return querySet 

class CreateURL(graphene.Mutation): 
    url = graphene.Field(URLType) 

    class Arguments: 
        full_url = graphene.String() 

    def mutate(self, info, full_url): 
        url = URL(full_url=full_url)
        url.save() 
        return CreateURL(url=url)

class Mutation(graphene.ObjectType): 
    create_url = CreateURL.Field() 
