import graphene
from graphene_django import DjangoObjectType 
from graphene_django.filter import DjangoFilterConnectionField 
from .models import City 
import django_filters 

class CityFilter(django_filters.FilterSet): 
    class Meta: 
        model = City 
        fields = ['name', 'distances'] 

class CityNode(DjangoObjectType): 
    class Meta: 
        model = City 
        interfaces = {graphene.relay.Node, } 

class Query(graphene.ObjectType): 
    city = graphene.relay.Node.Field(CityNode) 
    cities = DjangoFilterConnectionField(CityNode, filterset_class=CityFilter) 

class CreateCity(graphene.relay.ClientIDMutation):
    city = graphene.Field(CityNode)

    class Input:
        name = graphene.String()
        distances = graphene.String() 

    def mutate_and_get_payload(root, info, **input): 
        city = City(
            name=input.get('name'), 
            distances=input.get('distances')
        )
        city.save()

        return CreateCity(city=city)

class DeleteCities(graphene.Mutation):
    cities = graphene.List(CityNode)

    class Arguments:
        name = graphene.String()

    def mutate(root, info, **kwargs):
        deleted_cities = []
        for city in City.objects.filter(name=kwargs['name']): 
            city.delete()
            deleted_cities.append(city)
        return deleted_cities

class Mutation(graphene.AbstractType): 
    create_city=CreateCity.Field()
    delete_cities=DeleteCities.Field() 
