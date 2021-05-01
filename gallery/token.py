from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.contrib.auth.models import User
from django.http import HttpResponse

VERIFICATION_SECRET_KEY = "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ3ODI1Njk3NiwiaWF0IjoxNDc4MjU2OTU2fQ.InllcmVtaWEuYWlAZ21haWwuY29tIg.2HdNgoR_z-0Jf2A8aD3HUKsscbKueyOboz8oWbH2Pek"

auth_signer = Serializer(VERIFICATION_SECRET_KEY, expires_in=600)

def token_is_valid(token):
   email = auth_signer.loads(token)
   user = User.objects.get(email=email)
   return user

def generate_token(email):
   return auth_signer.dumps(email)

def token_login_required(function):
    def wrapper(request, *args, **kw):
        auth_token = request.META['HTTP_AUTHORIZATION']
        if not(auth_token is None):
          try:
            request.user = token_is_valid(auth_token)
            if request.user == None:
              raise Exception('Token Invalid')
          except SignatureExpired:
            return HttpResponse('Token is expired')
          else:
            return function(request, *args, **kw)
        #else:
        #  view_func = login_required(request)
        #  if not view_func.user.is_authenticated():
        #    return view_func(request)
        #  else:
        #    return function(request, *args, **kw)
    return wrapper
