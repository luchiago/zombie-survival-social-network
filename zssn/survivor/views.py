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

    '''elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        serializer = SurvivorSerializer(survivor, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(data="Wrong Parameters", status=400)'''

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
    data['Percentage of infected survivors'] = str((infected/total) * 100) + '%'
    data['Percentage of non-infected survivors'] = str((non_infected/total) * 100) + '%'
    data['Average amount of water by survivor'] = round(water/total,2)
    data['Average amount of food by survivor'] = round(food/total,2)
    data['Average amount of medication by survivor'] = round(medication/total,2)
    data['Average amount of ammunition by survivor'] = round(ammunition/total,2)
    data['Points lost because of infected survivor'] = pointslost
    return JsonResponse(data)
