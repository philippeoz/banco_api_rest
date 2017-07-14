from rest_framework.authentication import SessionAuthentication 

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Classe de autenticação que remove a validação CSRF Token
    """
    def enforce_csrf(self, request):
        return