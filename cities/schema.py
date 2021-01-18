import graphene
from graphene_django import DjangoObjectType 
from .models import City, CityResponse 
from graphql import GraphQLError
from itertools import permutations

class CityType(DjangoObjectType): 
    class Meta: 
        model = City 

class CityResponseType(DjangoObjectType): 
    class Meta: 
        model = CityResponse 

DEFAULT_CITIES = ['Нур-Султан',  'Алматы',  'Шымкент',  'Актобе',  'Атырау', 'Усть-Каменогорск']

class Query(graphene.ObjectType): 
    cities = graphene.List(CityType)
    travel_paths = graphene.List(CityResponseType, startAt=graphene.String(), requestedCities=graphene.List(graphene.String)) 

    def resolve_cities(self, info, **kwargs): 
        return City.objects.all() 

    def resolve_travel_paths(self, info, startAt=None, requestedCities=DEFAULT_CITIES, **kwargs): 
        startCity = City.objects.filter(name=startAt).first() 
        if not startCity: 
            raise GraphQLError('You must provide correct starting city name')

        graph = []
        graph.append([int(d) for d in startCity.distances.split(',')])

        for city in City.objects.all():
            if city.name == startCity.name: 
                continue 
            graph.append([int(d) for d in city.distances.split(',')])

        paths = travelPaths(graph, City.objects, requestedCities)

        response = []
        for key in sorted(paths.keys(), reverse=True): 
            response.append( 
                CityResponse( 
                    startCity = startCity.name, 
                    pathWeight = key, 
                    path = paths[key]
                ) 
            )

        return response

class CreateCity(graphene.Mutation):
    city = graphene.Field(CityType)

    class Arguments:
        name = graphene.String()
        order = graphene.Int() 
        distances = graphene.String() 

    def mutate(self, info, name, order, distances): 
        city = City(
            name=name, 
            order=order, 
            distances=distances
        )
        city.save()

        return CreateCity(city=city)

class DeleteCities(graphene.Mutation):
    cities = graphene.List(CityType)

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

def travelPaths(graph, cities, requestedCities, s=0): 
    vertices = [] 
    for requestedCity in requestedCities: 
        city = cities.filter(name=requestedCity).first()
        if not city: 
            raise GraphQLError('Requested city not present in database')

        if city.order != s: 
            vertices.append(city.order) 
 
    paths = {}
    for combination in permutations(vertices):
        curr_weight = 0
        curr_path = []
        k = s 
        for j in combination: 
            curr_weight += graph[k][j] 
            curr_path.append(cities.filter(order=k).first().name)
            k = j 
        curr_weight += graph[k][s] 
        curr_path.append(cities.filter(order=k).first().name)
        paths[curr_weight]=curr_path
         
    return paths 
