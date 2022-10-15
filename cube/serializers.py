from rest_framework import serializers
from cube.models import cubeUser


class cubeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = cubeUser
        fields = '__all__'
