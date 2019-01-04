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
        #List all the survivors
        survivor = Survivor.objects.all()
        serializer = SurvivorSerializer(survivor, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        #Create a survivor
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
    """
    Return the reports about the survivors
    """
    if Survivor.objects.all() is None:
        return HttpResponse(status=404)
        #if doesn't exist any survivor, return error
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
                #Verify the number of fields
                return HttpResponse(status=400)
            elif item != "last_location_longitude" and item != "last_location_latitude":
                return HttpResponse(status=400)
        serializer = SurvivorSerializer(survivor, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return HttpResponse(status=404)

@csrf_exempt
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
        return HttpResponse(status=404)

    if request.method == 'PATCH':
        if survivor.infected is True or survivor.reports >= 3:
            return HttpResponse(status=401)
            #because he is alredy infected, doesn't make sense flag him again
        data = JSONParser().parse(request)
        #Date is a dict that contains the id of the survivors reporting
        for item in data.keys():
            #Verify if id's are valid
            try:
                survivor_reporter = Survivor.objects.get(pk=data[item])
            except Survivor.DoesNotExist:
                return HttpResponse(status=404)
            if survivor_reporter.infected is True:
                #In case of infected survivor
                return HttpResponse(status=404)
        reports = len(data)
        print(reports)
        data1 = {'reports' : reports}
        print(survivor.name)
        print(data1)
        serializer = SurvivorSerializer(survivor, data=data, partial=True)
        if (survivor.reports >= 3):
            data1 = {infected : False}
            serializer = SurvivorSerializer(survivor, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return HttpResponse(status=404)
