from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from survivor.models import Survivor
from survivor.serializers import SurvivorSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'survivor': reverse('survivor-list', request=request, format=format),
        'reports': reverse('reports-list', request=request, format=format)
    })

@api_view(['GET', 'POST'])
def survivor_list(request):
    """
    List all survivors, or create a new survivor
    """
    if request.method == 'GET':
        survivor = Survivor.objects.all()
        serializer = SurvivorSerializer(survivor, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = SurvivorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def survivor_detail(request, pk):
    """
    Retrieve or delete a survivor.
    """
    try:
        survivor = Survivor.objects.get(pk=pk)
    except Survivor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SurvivorSerializer(survivor)
        return Response(serializer.data)

@api_view(['GET'])
def survivor_reports(request):

    if request.method == 'GET':
        data = {}
        total = infected = non_infected = water = food = medication = ammunition = pointslost = 0
        for i in Survivor.objects.all():
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
        data['Percentage of infected survivors'] = str(round((infected/total), 2) * 100) + '%'
        data['Percentage of non-infected survivors'] = str(round((non_infected/total), 2) * 100) + '%'
        data['Average amount of water by survivor'] = round(water/total,2)
        data['Average amount of food by survivor'] = round(food/total,2)
        data['Average amount of medication by survivor'] = round(medication/total,2)
        data['Average amount of ammunition by survivor'] = round(ammunition/total,2)
        data['Points lost because of infected survivor'] = pointslost
        return Response(data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def survivor_update_location(request, pk):
    """
    Update the location of survivor
    """
    try:
        survivor = Survivor.objects.get(pk=pk)
    except Survivor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        data = request.data
        for item in data.keys():
            if len(data) > 2:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            elif item != "last_location_longitude" and item != "last_location_latitude":
                return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = SurvivorSerializer(survivor, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
def survivor_flag_as_infected(request, pk):
    """
    Flag one survivor as infected, starting from his id
    If gets a 3 flags, the boolean infected turns True
    Model of json:
    {
        reportx : <int:id>
    }
    where "x" is the number of report and <int:id> is the id of the other survivor
    """

    try:
        survivor = Survivor.objects.get(pk=pk)
    except Survivor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        if survivor.infected is True or survivor.reports >= 3:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        for item in data.keys():
            try:
                survivor_reporter = Survivor.objects.get(pk=data[item])
            except Survivor.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if survivor_reporter.infected is True:
                return Response(status=status.HTTP_404_NOT_FOUND)
        survivor.reports += len(data)
        serializer = SurvivorSerializer(survivor, data=survivor.__dict__)
        if survivor.reports >= 3:
            survivor.infected = True
            serializer = SurvivorSerializer(survivor, data=survivor.__dict__)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
