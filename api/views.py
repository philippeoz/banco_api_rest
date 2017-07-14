from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import ContaSerializer
from api.serializers import ExtratoSerializer
from api.auth import CsrfExemptSessionAuthentication
from core.models import Conta
from core.models import Caixa
from core.utils import caixa_check
from core.utils import cedulas_check
from decimal import Decimal


class BaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet que abrange as principais funcionalidades
    para a api como listagem, criação, atualização, etc..
    Para servir como base na criação de outras Views da API
    """
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = None
    model = None

    def get_queryset(self):
        return self.model.objects.all()

    def retrieve(self, request, pk=None):
        queryset = self.model.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = self.model.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.update(obj, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400) 


class ContaViewSet(BaseViewSet):
    """
    ViewSet do Model Conta, herdando da BaseViewSet,
    contem os métodos que realizam as principais tarefas 
    do banco de tangamandápio
    """
    model = Conta
    serializer_class = ContaSerializer

    def saque(self, request, pk=None):
        """
        Método para realização de saque a partir da api

        :param request: Requisição
        :param pk: Id da conta que será realizado o saque 
        :return: Response
        """
        data = {}
        try:
            conta = self.model.objects.get(pk=pk)
            valor = Decimal(request.data['valor'])
            caixa = caixa_check()
            saque_dict = cedulas_check(valor, caixa.cedulas_disponiveis())
            conta.saque(valor)
            caixa.saque(saque_dict)
            return Response(saque_dict)
        except Exception as err:
            data['detail'] = str(err)
            return Response(data, status=400)

    def transferencia(self, request, pk=None):
        """
        Método para realização de transferência a partir da api

        :param request: Requisição
        :param pk: Id da conta que será realizada a transferência 
        :return: Response
        """
        data = {}
        try:
            conta = self.model.objects.get(pk=pk)
            conta_favorecida = self.model.objects.get(pk=request.data['conta'])
            valor = Decimal(request.data['valor'])
            conta.transferencia(valor, conta_favorecida)
            serialize = self.serializer_class(conta)
            return Response(serialize.data)
        except Exception as err:
            data['detail'] = str(err)
            return Response(data, status=400)

    def extrato(self, request, pk=None):
        """
        Método para visualização de extrato contendo todas as
        transações efetuadas em uma conta

        :param request: Requisição
        :param pk: Id da conta que será emitido o extrato
        :return: Response
        """
        queryset = self.model.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = ExtratoSerializer(obj.transacoes.all().order_by('data_hora'), 
                                        many=True)
        return Response(serializer.data)


class CaixaView(APIView):
    """
    APIView para visualizar e atualizar informações do model Caixa
    """
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, format=None):
        caixa = caixa_check()
        return Response(caixa.serialize())

    def post(self, request, format=None):
        caixa = caixa_check()
        caixa.update(request.data)
        return Response(caixa.serialize())