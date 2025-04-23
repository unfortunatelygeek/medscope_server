from rest_framework import serializers
from .models import DermatoImage, OtoImage, PharyngoImage

class DermatoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DermatoImage
        fields = '__all__'

class OtoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtoImage
        fields = '__all__'

class DermatoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharyngoImage
        fields = '__all__'
