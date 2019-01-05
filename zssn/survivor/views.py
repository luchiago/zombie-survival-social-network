from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from survivor.models import Survivor
from survivor.serializers import SurvivorSerializer

@csrf_exempt
def survivor_list(request):
    """
    List all survivors, or create a new survivor
    """
    if request.method == 'GET':
        survivor = Survivor.objects.all()
        serializer = SurvivorSerializer(survivor, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SurvivorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def survivor_detail(request, pk):
    """
    Retrieve or delete a survivor.
    """
    try:
        survivor = Survivor.objects.get(pk=pk)
    except Survivor.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SurvivorSerializer(survivor)
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        survivor.delete()
        return HttpResponse(status=204)

@csrf_exempt
def survivor_reports(request):
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
    return JsonResponse(data)


@csrf_exempt
def survivor_update_location(request, pk):
    """
    Update the location of survivor
    """
    try:
        survivor = Survivor.objects.get(pk=pk)
    except Survivor.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PATCH':
        data = JSONParser().parse(request)
        for item in data.keys():
            if len(data) > 2:
                return HttpResponse(status=400)
            elif item != "last_location_longitude" and item != "last_location_latitude":
                return HttpResponse(status=400)
        serializer = SurvivorSerializer(survivor, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return HttpResponse(status=404)

@csrf_exempt
def survivor_trade(request):
    """
    The exchange of items between survivors happening in the following model:
    {
        "survirvor1_id" : id,
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
                points = survivor_items[item] * 4
            if item.lower() == "food":
                points = survivor_items[item] * 3
            if item.lower() == "medication":
                points = survivor_items[item] * 2
            if item.lower() == "ammunition":
                points = survivor_items[item] * 1
        return points

    if request.method == 'PATCH':
        data = JSONParser().parse(request)
        try:
            survivor = Survivor.objects.get(pk=data["survivor1_id"])
            survivor = Survivor.objects.get(pk=data["survivor2_id"])
        except Survivor.DoesNotExist:
            return HttpResponse(status=404)
        survivor1_items = data["items1_trade"]
        survivor1_points = get_points(survivor1_items)
        survivor2_items = data["items2_trade"]
        survivor2_points = get_points(survivor2_items)
