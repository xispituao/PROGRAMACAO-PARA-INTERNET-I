from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.generic.base import View
from perfis.models import Perfil
from usuarios.forms import RegistrarUsuarioForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class RegistrarUsuarioView(View):
    template_name = 'registrar.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            dados_form = form.cleaned_data
            usuario = User.objects.create_user(username=dados_form['nome'],
                                               email=dados_form['email'],
                                               password=dados_form['senha'])
            perfil = Perfil(nome=dados_form['nome'], telefone=dados_form['telefone'],
                            nome_empresa=dados_form['nome_empresa'],
                            usuario_id=usuario)
            perfil.save()
            messages.add_message(request, messages.INFO, 'Cadastro realizado!')
            return redirect('index')

        return render(request, self.template_name, {'form': form})


class AlterarSenhaView(View):
    template_name = 'alterar_senha.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        senha_antiga = request.POST.get('senha_antiga')
        nova_senha = request.POST.get('nova_senha')
        confirmacao_senha = request.POST.get('confirmacao_senha')

        if self.validacoes_senha(request, senha_antiga, nova_senha, confirmacao_senha):
            user = request.user
            user.set_password(nova_senha)
            user.save()
            return redirect('index')

        return redirect('alterar_senha')


    def validacoes_senha(self, request, senha_antiga, nova_senha, confirmacao_senha):
        valido = True
        username = request.user.username
        user = authenticate(request, username=username, password=senha_antiga)

        if user is None:
            messages.add_message(request, messages.INFO, 'senha não confere com a cadastrada')
            valido = False
        if nova_senha != confirmacao_senha:
            messages.add_message(request, messages.INFO, 'senha repetida não confere')
            valido = False
        return valido   


def bloquear_usuario(request, id_perfil):
    if request.user.is_superuser:
        user = Perfil.objects.get(id=id_perfil).usuario
        user.is_active = False
        user.save()
    return redirect('/perfil/{}/'.format(id_perfil))

def bloquear_meu_usuario(request):
    user = request.user
    user.is_active = False
    user.save()
    return redirect('deslogar')


def desbloquear_usuario(request, id_perfil):
    if request.user.is_superuser:
        user = Perfil.objects.get(id=id_perfil).usuario
        user.is_active = True
        user.save()
    return redirect('/perfil/{}/'.format(id_perfil))

def superuser_on(request, id_perfil):
    if request.user.is_superuser:
        user = Perfil.objects.get(id=id_perfil).usuario_id
        user.is_superuser = True
        user.save()
    return redirect('/perfil/{}/'.format(id_perfil))


def superuser_off(request, id_perfil):
    if request.user.is_superuser:
        user = Perfil.objects.get(id=id_perfil).usuario_id
        user.is_superuser = False
        user.save()
    return redirect('/perfil/{}/'.format(id_perfil))