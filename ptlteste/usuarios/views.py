
from rest_framework import viewsets, permissions, authentication, filters
from .models import Usuario
from .serializers import UsuarioSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import requests

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# MANIPULAÇÃO DOS USUARIOS
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


#PARA CRIAÇÃO DE USUÁRIO
class CadastrarUserView(APIView):
    parser_class = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        retorno = json.loads(self.request.body.decode("utf-8"))

        username = retorno.get('username')
        first_name = retorno.get('first_name')
        last_name = retorno.get('last_name')
        email = retorno.get('email')
        cep = retorno.get('cep')
        rua = retorno.get('rua')
        numero = retorno.get('numero')
        complemento = retorno.get('complemento')
        municipio = retorno.get('municipio')
        estado = retorno.get('estado')
        pais = retorno.get('pais')
        cpf = retorno.get('cpf')
        pis = retorno.get('pis')
        password = retorno.get('password')
        is_superuser = retorno.get('is_superuser')
        is_active = retorno.get('is_active')

        user = Usuario.objects.create_user(username, email, password)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.cep = cep
        user.rua = rua
        user.numero = numero
        user.complemento = complemento
        user.municipio = municipio
        user.estado = estado
        user.pais = pais
        user.cpf = cpf
        user.pis = pis
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.save()

        msg = 'Cadastro realizado!'

        return Response({'status': msg})


@csrf_exempt
def gerar_token(request):
    msg =''
    dicToken={}
    usuario=  Usuario.objects.all()
    if request.method == 'POST':
        email_cpf_pis = request.POST.get('email')
        password = request.POST.get('password')
        payload = jwt_payload_handler(usuario)
        token = jwt_encode_handler(payload)


        dicToken.update({'Token':token})

    return   HttpResponse(json.dumps(dicToken), content_type='application/json')



def do_login(request):
    msg=''
    dicToken={}
    if request.method == 'POST':
        email = request.POST.get('email')
        password =request.POST.get('password')
        user = Usuario.authenticate(username=email, password=password)
        if user is not None:
            usuario = Usuario.objects.get(id=user.id)
            login(request, user,  backend='django.contrib.auth.backends.ModelBackend')
            payload = jwt_payload_handler(usuario)
            token = jwt_encode_handler(payload)
            dicToken.update({'token':token})
            return render(request,'usuarios/index.html',{'token': dicToken } )
        else:
            msg = 'Usuário ou senha inválidos!'

    return render(request,'registration/login.html',{'msg': msg} )

def do_logout(request):
    logout(request)
    return redirect('/login/auth0')


def index(request):

    return render(request, 'usuarios/index.html')

def editar(request,pk):

    return render(request, 'usuarios/editar.html',{'id':pk})


def cadastrar(request):

    return render(request, 'usuarios/cadastrar.html')



@csrf_exempt
def search_by_cep(request):
    cep = request.POST.get('cep')
    #print('vai printar')
    #print(cep.replace('"','').replace('.','').replace('-',''))
    #token = "ab56b218a8cdc76afda4c63286655086"
    #headers = {'Authorization': 'Token token=%s' % token}
    url = "https://viacep.com.br/ws/"+format(cep.replace('"','').replace('.','').replace('-',''))+"/json/"
    response = requests.get(url)
    #print(response.json())
    return  JsonResponse({"data":response.json()})
