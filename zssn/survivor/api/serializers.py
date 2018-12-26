from rest_framework.serializers import ModelSerializer
import survivor.models as model

class SurvivorSerializer(ModelSerializer):
    class Meta:
        model = model.Survivor
        fields = ('id', 'name', 'age', 'gender', 'last_location_longitude',
                  'last_location_latitude', 'water', 'food',
                  'medication', 'ammunition', 'infected', 'reports')
        read_only_fields = ('infected', 'reports')
