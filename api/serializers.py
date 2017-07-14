from core.models import *
from rest_framework import serializers


class ContaSerializer(serializers.ModelSerializer):
    """
    Serializer para o Model Conta
    """
    class Meta:
        model = Conta
        fields = "__all__"


class ExtratoSerializer(serializers.ModelSerializer):
    """
    Model para Transacao para geração de extrato
    """
    class Meta:
        model = Transacao
        fields = "__all__"