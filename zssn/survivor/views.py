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
        'survivor detail' : reverse('survivor-detail', request=request, format=format),
        'reports': reverse('reports-list', request=request, format=format),
        'update location' : reverse('update-location', request=request, format=format),
        'flag as infected' : reverse('infected',request=request, format=format),
        'trades' : reverse('trade', request=request, format=format)
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
        total_survivors = infected = non_infected = water = food = medication = ammunition = pointslost = 0
        for i in Survivor.objects.all():
            total_survivors += 1
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
        if total_survivors != 0:
            data['Percentage of infected survivors'] = str(round((infected/total_survivors), 2) * 100) + '%'
            data['Percentage of non-infected survivors'] = str(round((non_infected/total_survivors), 2) * 100) + '%'
            data['Average amount of water by survivor'] = round(water/total_survivors,2)
            data['Average amount of food by survivor'] = round(food/total_survivors,2)
            data['Average amount of medication by survivor'] = round(medication/total_survivors,2)
            data['Average amount of ammunition by survivor'] = round(ammunition/total_survivors,2)
            data['Points lost because of infected survivor'] = pointslost
        return Response(data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def survivor_update_location(request, pk):

    """
    Update the location of survivor
    Model of json:
    {
        "last_location_longitude" : "172º23'23''E'"
        "last_location_latitude" : "80º21'25''N"
    }
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
        "reportx" : <int:id>
    }
    where "x" is the number of report and <int:id> is the id of the other survivor
    """

    try:
        survivor = Survivor.objects.get(pk=pk)
    except Survivor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    def repeated_id_verify(list_id, id_to_verify):
        if len(list_id) == 0:
            list_id.append(id_to_verify)
            return list_id
        else:
            for id in list_id:
                if id == id_to_verify:
                    return list_id
            list_id.append(id_to_verify)
            return list_id

    if request.method == 'PATCH':

        if survivor.infected is True or survivor.reports >= 3:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        list_id = []

        for item in data.keys():
            try:
                survivor_reporter = Survivor.objects.get(pk=data[item])
            except Survivor.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if survivor_reporter.infected is True:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            list_id = repeated_id_verify(list_id, data[item])

        survivor.reports += len(list_id)
        serializer = SurvivorSerializer(survivor, data=survivor.__dict__)
        if survivor.reports >= 3:
            survivor.infected = True
            serializer = SurvivorSerializer(survivor, data=survivor.__dict__)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
def survivor_trade(request):
    """
    The exchange of items between survivors happening in the following model:
    {
        "survivor1_id" : id,
        "items1_trade": {"type" : amount},
        "survivor2_id": id,
        "items2_trade": {"type" : amount},
    }
    where "x" is the amount of the item (e.g "water" : 5)
    """
    def get_points(survivor_items):
        points = 0
        for item in survivor_items.keys():
            if item.lower() == "water":
                points += survivor_items[item] * 4
            if item.lower() == "food":
                points += survivor_items[item] * 3
            if item.lower() == "medication":
                points += survivor_items[item] * 2
            if item.lower() == "ammunition":
                points += survivor_items[item] * 1
        return points

    def verify_items(survivor, survivor_items):
        flag = True
        for item in survivor_items.keys():
            if item.lower() == "water":
                if survivor_items[item] > survivor.water:
                    flag = False
            if item.lower() == "food":
                if survivor_items[item] > survivor.food:
                    flag = False
            if item.lower() == "medication":
                if survivor_items[item] > survivor.medication:
                    flag = False
            if item.lower() == "ammunition":
                if survivor_items[item] > survivor.ammunition:
                    flag = False
        return flag

    def trade_accepted(survivor, survivor_gives, survivor_receive):
        for item in survivor_gives.keys():
            if item.lower() == "water":
                survivor.water -= survivor_gives[item]
            if item.lower() == "food":
                survivor.food -= survivor_gives[item]
            if item.lower() == "medication":
                survivor.medication -= survivor_gives[item]
            if item.lower() == "ammunition":
                survivor.ammunition -= survivor_gives[item]
        for item in survivor_receive.keys():
            if item.lower() == "water":
                survivor.water += survivor_receive[item]
            if item.lower() == "food":
                survivor.food += survivor_receive[item]
            if item.lower() == "medication":
                survivor.medication += survivor_receive[item]
            if item.lower() == "ammunition":
                survivor.ammunition += survivor_receive[item]
        return survivor

    if request.method == 'PATCH':

        data = request.data

        try:
            survivor1 = Survivor.objects.get(pk=data["survivor1_id"])
            survivor2 = Survivor.objects.get(pk=data["survivor2_id"])
        except Survivor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if survivor1.infected is True or survivor2 is True:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        survivor1_items = data["items1_trade"]
        survivor1_points = get_points(survivor1_items)
        survivor2_items = data["items2_trade"]
        survivor2_points = get_points(survivor2_items)

        if not verify_items(survivor1, survivor1_items) or not verify_items(survivor2, survivor2_items):
                return Response(status=status.HTTP_400_BAD_REQUEST)

        if survivor1_points == survivor2_points:
            survivor1 = trade_accepted(survivor1, survivor1_items, survivor2_items)
            survivor2 = trade_accepted(survivor2, survivor2_items, survivor1_items)
            serializer1 = SurvivorSerializer(survivor1, data=survivor1.__dict__)
            serializer2 = SurvivorSerializer(survivor2, data=survivor2.__dict__)
            if serializer1.is_valid() and serializer2.is_valid():
                serializer1.save()
                serializer2.save()
                response = list((serializer1.data, serializer2.data))
                return Response(response)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
