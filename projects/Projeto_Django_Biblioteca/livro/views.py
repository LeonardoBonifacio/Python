from django.shortcuts import render,redirect
from django.http import HttpResponse
from usuarios.models import  Usuario
from .models import Livros,Categoria,Emprestimo
from .forms import CadastroLivro,CategoriaLivro
from datetime import datetime

from django.db.models import Q
# Create your views here.





def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session['usuario'])
        livros = Livros.objects.filter(usuario=usuario)
        total_livros = livros.count()
        form = CadastroLivro()
        form.fields['usuario'].initial = request.session['usuario']
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario)
        form_categoria = CategoriaLivro()
        status_categoria = request.GET.get('cadastro_categoria')
        usuarios = Usuario.objects.all()
        livros_emprestar = Livros.objects.filter(usuario=usuario).filter(emprestado=False)
        livros_emprestados = Livros.objects.filter(usuario=usuario).filter(emprestado=True)

        return render(request, 'home.html', {'livros':livros, 
                                             'usuario_logado': request.session.get('usuario'), 
                                             'form':form,
                                             'form_categoria':form_categoria,
                                             'status_categoria':status_categoria,
                                             'usuarios':usuarios,
                                             'livros_emprestar':livros_emprestar,
                                             'total_livros' : total_livros,
                                             'livros_emprestados' : livros_emprestados})
    else:
        return redirect('/auth/login/?status=2')


def ver_livros(request, id):
    if request.session.get('usuario'):
        livro = Livros.objects.get(id=id)
        if request.session.get('usuario') == livro.usuario.id:
            usuario = Usuario.objects.get(id = request.session['usuario'])
            categoria_livro = Categoria.objects.filter(usuario_id = request.session.get('usuario'))
            emprestimos = Emprestimo.objects.filter(livro=livro)
            form = CadastroLivro()
            form.fields['usuario'].initial = request.session['usuario']
            form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario)
            form_categoria = CategoriaLivro()
            usuarios = Usuario.objects.all()
            livros_emprestar = Livros.objects.filter(usuario=usuario).filter(emprestado=False)
            livros_emprestados = Livros.objects.filter(usuario=usuario).filter(emprestado=True)
            livros = Livros.objects.filter(usuario=usuario)
            total_livros = livros.count()

            return render(request, 'ver_livro.html', {'livro':livro, 
                                                      'categoria_livro':categoria_livro, 
                                                      'emprestimos':emprestimos,
                                                      'usuario_logado': request.session.get('usuario'),
                                                      'form':form,
                                                      'id_livro':id,
                                                      'form_categoria':form_categoria,
                                                      'usuarios': usuarios,
                                                      'livros_emprestar':livros_emprestar,
                                                      'total_livros' : total_livros,
                                                      'livros_emprestados' : livros_emprestados})
        else:
            return redirect('/auth/sair/')
    return redirect('/auth/login/?status=2')


def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivro(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/livro/home/')
        else:
            return HttpResponse('Dados inválidos')


def excluir_livro(request,id):
    livro = Livros.objects.get(id = id).delete()
    return redirect('/livro/home')


def cadastrar_categoria(request):
    form = CategoriaLivro(request.POST)
    nome = form.data['nome']
    descricao =  form.data['descricao']
    id_usuario = request.POST.get('usuario')
    if int(id_usuario) == int(request.session.get('usuario')):
        user = Usuario.objects.get(id = id_usuario)
        categoria = Categoria(
            nome=nome,
            descricao=descricao,
            usuario=user
        )
        categoria.save()
        return redirect('/livro/home?cadastro_categoria=1')
    else:
        return HttpResponse('Pare de querer trocar html das coisa ')


def cadastrar_emprestimo(request):
    if request.method == 'POST':
        nome_emprestado = request.POST.get('nome_emprestado')
        nome_emprestado_anonimo = request.POST.get('nome_emprestado_anonimo')
        livro_emprestado = request.POST.get('livro_emprestado')
        if nome_emprestado_anonimo:
             emprestimo = Emprestimo(
            nome_emprestado_anonimo=nome_emprestado_anonimo,
            livro_id=livro_emprestado
        )
        else:
            emprestimo = Emprestimo(
                nome_emprestado_id=nome_emprestado,
                livro_id=livro_emprestado
            )
        emprestimo.save()

        livro = Livros.objects.get(id = livro_emprestado)
        livro.emprestado = True
        livro.save()

        return redirect('/livro/home/')


def devolver_livro(request):
    id = request.POST.get('id_livro_devolver')
    livro_devolver = Livros.objects.get(id = id)
    livro_devolver.emprestado = False
    livro_devolver.save()

    emprestado_devolver = Emprestimo.objects.get(Q(livro = livro_devolver) & Q(data_devolucao = None))
    emprestado_devolver.data_devolucao = datetime.now()
    emprestado_devolver.save()
    return redirect('/livro/home/')



def alterar_livro(request):
    livro_id = request.POST.get('livro_id')
    nome_livro = request.POST.get('nome_livro')
    autor = request.POST.get('autor')
    co_autor = request.POST.get('co_autor')
    categoria_id = request.POST.get('categoria_id')
    categoria = Categoria.objects.get(id = categoria_id)

    livro = Livros.objects.get(id = livro_id)
    if livro.usuario.id == request.session['usuario']:
        livro.nome = nome_livro
        livro.autor = autor
        livro.co_autor = co_autor
        livro.categoria = categoria
        livro.save()
        return redirect(f'/livro/ver_livro/{livro_id}')
    else:
        return redirect('/auth/sair')


def seus_emprestimos(request):
    usuario = Usuario.objects.get(id = request.session.get('usuario'))
    emprestimos = Emprestimo.objects.filter(nome_emprestado=usuario)
    livros = Livros.objects.filter(usuario=usuario)
    total_livros = livros.count()
    livros_emprestar = Livros.objects.filter(usuario=usuario).filter(emprestado=False)
    livros_emprestados = Livros.objects.filter(usuario=usuario).filter(emprestado=True)
    form = CadastroLivro()
    form.fields['usuario'].initial = request.session['usuario']
    form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario)
    form_categoria = CategoriaLivro()

    return render(request, 'seus_emprestimos.html', {"usuario_logado":request.session['usuario'],
                                                    "emprestimos": emprestimos,
                                                    'total_livros' : total_livros,
                                                    'livros_emprestar':livros_emprestar,
                                                    'livros_emprestados' : livros_emprestados,
                                                    'form':form,
                                                    'form_categoria':form_categoria,})

def processa_avaliacao(request):
    id_emprestimo = request.POST.get('id_emprestimo')
    id_livro = request.POST.get('id_livro')
    opcoes = request.POST.get('opcoes')
    emprestimo = Emprestimo.objects.get(id = id_emprestimo)
    if emprestimo.livro.usuario.id == request.session['usuario']:
        emprestimo.avaliacao = opcoes
        emprestimo.save()
        return redirect(f'/livro/ver_livro/{id_livro}')
    else:
        return HttpResponse('Esse empréstimo não é seu')