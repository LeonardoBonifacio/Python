from django.shortcuts import render,redirect
from .models import Especialidades,DadosMedico,is_medico,DatasAbertas
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
# Create your views here.


def cadastro_medico(request):

    if is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Você já é médico')
        return redirect('/medicos/abrir_horario')

    if request.method == 'GET':
        especialidades = Especialidades.objects.all()   
        return render(request,'cadastro_medico.html', {'especialidades': especialidades})

    elif request.method == 'POST':
        crm = request.POST.get('crm')
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')        
        especialidade = request.POST.get('especialidade')
        descricao = request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')
        cim = request.FILES.get('cim')
        rg = request.FILES.get('rg')
        foto = request.FILES.get('foto')

        dados_medico = DadosMedico(
            crm=crm,
            nome=nome,
            cep=cep,
            rua=rua,
            bairro=bairro,
            numero=numero,
            especialiade_id=especialidade,
            descricao=descricao,
            valor_consulta=valor_consulta,
            cedula_identidade_medica=cim,
            rg=rg,
            foto=foto,
            user=request.user
        )

        dados_medico.save()

        messages.add_message(request, constants.SUCCESS, 'Cadastro médico realizado com Sucesso!')
        return redirect('/medicos/abrir_horario')


def abrir_horario(request):

    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, "Somente médicos podem abrir horários")
        return redirect('/usuarios/sair')
    
    if request.method == 'GET':
        datas_abertas = DatasAbertas.objects.filter(User=request.user)
        dados_medico = DadosMedico.objects.get(user=request.user)
        return render(request, 'abrir_horario.html', {'dados_medico': dados_medico, 'datas_abertas' : datas_abertas})
    elif request.method == 'POST':
        data = request.POST.get('data')
        data_formatada = datetime.strptime(data,'%Y-%m-%dT%H:%M')
        if data_formatada < datetime.now():
            messages.add_message(request, constants.WARNING, 'A data não pode ser anterior a data atual')
            return redirect('/medicos/abrir_horario')
        
        horario_abrir = DatasAbertas(
            data=data,
            User=request.user
        )
        horario_abrir.save()

        messages.add_message(request, constants.SUCCESS, 'Horário cadastrado com sucesso!')
        return redirect('/medicos/abrir_horario')



