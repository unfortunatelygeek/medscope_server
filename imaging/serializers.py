from rest_framework import serializers
from .models import DermatoImage

class DermatoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DermatoImage
        fields = '__all__'
