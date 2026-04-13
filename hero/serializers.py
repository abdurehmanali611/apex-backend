from rest_framework import serializers
from .models import HeroStat


class HeroStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroStat
        fields = "__all__"
