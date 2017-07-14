from core.models import Caixa


def caixa_check():
    """
    Função que checa a existencia de um caixa
    se existir retorna o caixa, caso contrário,
    cria um caixa e o retorna

    :return: Caixa
    """
    caixa = Caixa.objects.first()
    if caixa is None:
        caixa = Caixa.objects.create()
    return caixa


def cedulas_check(valor, cedulas_disp):
    """
    Função que realiza o procedimento de separação das
    cédulas para saque de acordo como solicitado pelo 
    banco de tangamandápio

    :param valor: Valor a ser sacado
    :param cedulas_disp: Dicionário com as cédulas disponíveis para saque
    :return: Dicionário com a quantidade e valor das cédulas que serão sacadas
    """
    data = {}
    for ced, ced_quant in sorted(cedulas_disp.items())[::-1]:
        temp_value = valor // ced
        if not temp_value:
            data[ced] = temp_value
        if ced_quant >= temp_value:
            data[ced] = temp_value
            valor = valor % ced
        else:
            data[ced] = ced_quant
            valor -= (ced_quant*ced)
    if valor:
        raise Exception('Cédulas Insuficientes')
    return data