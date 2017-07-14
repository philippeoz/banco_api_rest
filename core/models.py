from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class Conta(models.Model):
    """
    Model Conta do Banco de Tangamandápio
    """
    nome = models.CharField(max_length=100)
    saldo = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.nome

    def saque(self, valor):
        """
        Método que efetua um saque na conta

        :param valor: Valor que será sacado
        :return:
        """
        self.check_valor(valor)
        saldo_anterior = self.saldo
        self.saldo -= valor
        self.save()
        Transacao.objects.create(
            saldo_antes=saldo_anterior,
            saldo_depois=self.saldo,
            descricao='Saque no valor de {} patacas.'.format(valor),
            conta=self
        )

    def transferencia(self, valor, conta_favorecida):
        """
        Método que realiza trasferência de saldo de uma conta para outra

        :param valor: Valor que será transferido
        :param conta_favorecida: ID da conta que receberá o valor
        :return:
        """
        self.check_valor(valor)
        saldo_anterior = self.saldo
        self.saldo -= valor
        conta_favorecida.saldo += valor
        self.save()
        conta_favorecida.save()
        Transacao.objects.create(
            saldo_antes=saldo_anterior,
            saldo_depois=self.saldo,
            descricao='Transferencia de {} para {}, no valor de {} patacas.'.\
                format(
                        self.nome,
                        conta_favorecida.nome,
                        valor
                ),
            conta=self
        )

    def check_valor(self, valor):
        if not valor or valor < 0:
            raise Exception('Valor inválido.')
        elif valor > self.saldo:
            raise Exception('Saldo insuficiente.')


class Caixa(models.Model):
    """
    Model Caixa do Banco de Tangamandápio
    """

    def serialize(self):
        """
        Método para serializar o model Caixa
        
        :return: dict 
        """
        cedulas_cfg = settings.CEDULAS
        data = {}
        for ced in cedulas_cfg:
            data[str(ced)] = self.cedulas.get(valor=ced).quantidade
        return data

    def cedulas_disponiveis(self):
        """
        Método que retorna um dicionário com as cédulas disponíveis para saque

        :return: dict 
        """
        data = {}
        queryset = self.cedulas.filter(quantidade__gt=0)
        for ced in queryset:
            data[ced.valor] = ced.quantidade
        return data

    def saque(self, saque_dict):
        """
        Método de saque que remove as cédulas que serão sacadas pela Conta

        :param saque_dict: Dicionário com cédulas/quantidades que serão sacadas
        :return:
        """
        for ced, quant in saque_dict.items():
            cedula = self.cedulas.get(valor=ced)
            cedula.quantidade -= quant
            cedula.save()

    def update(self, update_dict):
        """
        Método para atualizar as cédulas do Caixa a partir da API

        :param update_dict: Dicionário com as cedulas/quantidades que 
                            serão adicionadas
        :return:
        """
        cedulas_cfg = settings.CEDULAS
        for ced in cedulas_cfg:
            try:
                value = int(update_dict[str(ced)])
                if value >= 0:
                    cedula = self.cedulas.get(valor=ced)
                    cedula.quantidade = value
                    cedula.save()
            except:
                continue


class Cedula(models.Model):
    """
    Model para Cédulas do banco de tangamandápio
    """
    valor = models.IntegerField()
    quantidade = models.IntegerField(default=0)
    caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE, related_name='cedulas')


class Transacao(models.Model):
    """
    Model Transação para geração do extrato
    """
    saldo_antes = models.IntegerField()
    saldo_depois = models.IntegerField()
    descricao = models.CharField(max_length=255)
    data_hora = models.DateTimeField(auto_now=True)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='transacoes')

        
@receiver(post_save, sender=Caixa)
def criar_cedulas(sender, **kwargs):
    """
    Função para criar a quantidade de cedulas configuradas no settings
    Será executada para todo caixa criado.
    """
    cedulas_cfg = settings.CEDULAS
    for ced in cedulas_cfg:
        Cedula.objects.create(valor=ced, caixa=kwargs['instance'])