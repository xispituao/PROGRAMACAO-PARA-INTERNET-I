from django.shortcuts import render, redirect
from perfis.models import *
from django.contrib.auth.decorators import login_required
from perfis.form_post import PostForm
from django.views.generic.base import View
from django.core.files.storage import FileSystemStorage
from django.contrib import messages


@login_required
def index(request):
    form = PostForm()
    perfil_logado = get_perfil_logado(request)
    timeline = perfil_logado.timeline

    return render(request, 'index.html',
                  {'perfis': Perfil.objects.all(),
                   'perfil_logado': perfil_logado,
                   'form': form,
                   'timeline': timeline})


@login_required
def exibir(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    return render(request, 'perfil.html',
                  {'perfil': perfil,
                   'perfil_logado': get_perfil_logado(request),
                   'ja_eh_contato': ja_eh_contato})


@login_required
def convidar(request, perfil_id):
    perfil_logado = get_perfil_logado(request)
    perfil_a_convidar = Perfil.objects.get(id=perfil_id)
    if perfil_a_convidar != perfil_logado:
        perfil_logado.convidar(perfil_a_convidar)
    else:
        print('error')
    return redirect('index')


@login_required
def aceitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.aceitar()
    return redirect('index')


@login_required
def recusar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.recusar()
    return redirect('index')


@login_required
def desfazer_amizade(request, contato_id):
    perfil_logado = get_perfil_logado(request)
    perfil_logado.contatos.remove(contato_id)
    return redirect('index')


@login_required
def get_perfil_logado(request):
    return request.user.perfil


@login_required
def ser_super_usuario(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil.usuario.is_superuser = True
    perfil.usuario.save()
    perfil.save()

    return redirect('index')


@login_required
def deletar_postagem(request, postagem_id):
    postagem = Post.objects.get(id=postagem_id)
    postagem.excluir_postagem()

    return redirect('index')

@login_required
def buscar_usuario(request):
    encontrados = Perfil.objects.all()
    if request.method == 'GET':
        dados = {}
        dados['perfil_logado'] = request.user.perfil
        dados['encontrados'] = encontrados
        return render(request, 'busca.html', dados)
    if request.method == 'POST':
        query = request.POST.get('busca')

        if len(query) <= 0:
            messages.add_message(request, messages.INFO, 'Digite algo no campo de busca.')
            return redirect('index')

        encontrados = list(Perfil.objects.filter(nome__contains=query))
        if request.user.perfil in encontrados:
            encontrados.remove(request.user.perfil)

    dados = {}
    dados['encontrados'] = encontrados
    dados['perfil_logado'] = request.user.perfil
        
    return render(request, 'busca.html', dados)

# @login_required(login_url='login')
# def alterar_perfil(request):
#     try:
#         if request.method == 'POST':
#             imagem = request.FILES['imagemperfil']
#             file_system = FileSystemStorage()
#             file_name = file_system.save(imagem.name, imagem)

#             perfil_logado = request.user.perfil
#             perfil_logado.imagem_perfil = file_name
#             perfil_logado.save()
            
#             return redirect('index')
#     except:
#         return redirect('index')



class PostView(View):
    def post(self, request):
        form = PostForm(request.POST)
        imagem = request.FILES['imagem']
        if form.is_valid():
            file_system = FileSystemStorage()
            file_name = file_system.save(imagem.name, imagem)
            dados_form = form.cleaned_data
            post = Post()
            post.perfil = get_perfil_logado(request)
            post.postagem = dados_form['postagem']
            post.imagem = file_name
            post.save()
            return redirect('index')

        return redirect('index')


