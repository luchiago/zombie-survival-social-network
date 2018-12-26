from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import survivor.models as model
from .serializers import SurvivorSerializer


class SurvivorViewSet(ModelViewSet):
    serializer_class = SurvivorSerializer
    queryset = model.Survivor.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'age', 'last_location_longitude', 'last_location_latitude', 'infected')
    lookup_field = 'id' #for acess by endpoint survirvor/id

    @action(methods=['get'], detail=False)
    def reports(self, request):
        '''
        This method implements the reports
        Percentage of infected survivors.
        Percentage of non-infected survivors.
        Average amount of each kind of resource by survivor (e.g. 5 waters per survivor)
        Points lost because of infected survivor.
        '''
        d = {}
        total = infected = non_infected = water = food = medication = ammunition = pointslost = 0
        for i in model.Survivor.objects.all():
            total += 1
            if i.infected is False:
                non_infected += 1
            if i.infected is True:
                infected += 1
                pointslost += (4 * i.water)
                pointslost += (3 * i.food)
                pointslost += (2 * i.medication)
                pointslost += (1 * i.ammunition)
            water += i.water
            food += i.food
            medication += i.medication
            ammunition += i.ammunition
        d['Percentage of infected survivors'] = str((infected/total) * 100) + '%'
        d['Percentage of non-infected survivors'] = str((non_infected/total) * 100) + '%'
        d['Average amount of water by survivor'] = round(water/total,2)
        d['Average amount of food by survivor'] = round(food/total,2)
        d['Average amount of medication by survivor'] = round(medication/total,2)
        d['Average amount of ammunition by survivor'] = round(ammunition/total,2)
        d['Points lost because of infected survivor'] = pointslost
        return Response(d)