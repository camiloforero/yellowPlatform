#coding=utf-8
from __future__ import unicode_literals
import math
from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse
from .models import Voto, Mocion, PlenoDerecho, Candidato, VotoCandidato
from django.forms import modelformset_factory
from django.views.generic.base import TemplateView
from .forms import VotoForm, VotoCandidatoForm

def votingView(request, Q):
    """
    Q: el Q o la asamblea extraordinaria donde corre la votación
    """
    if request.method == 'POST':
        #Se obtienen las mociones y los candidatos de la asamblea de la base de datos
        mociones = Mocion.objects.filter(asamblea=Q)
        candidatos = Candidato.objects.filter(asamblea=Q)
        #Se inicializan las listas que contendrán a las mociones y a los candidatos para TODO
        mocionList = []
        candidatoList = []
        #Se inicializan las listas que contendrán los votos para poder guardarlos en un ciclo al final, sólo si la totalidad del formulario es correcto.
        votos = []
        votosCandidatos = []
        
        for mocion in mociones:
            voteData = {}
            #Se obtienen los datos de la moción actual a partir del POST
            votoForm = VotoForm(request.POST, prefix=mocion.pk)
            #Se revisa si el código le pertenece a algún pleno derecho. Si no, se genera un mensaje de error inmediatamente
            try:
                votante = PlenoDerecho.objects.get(pk=request.POST.get('codigo'))
            except:
                return HttpResponse('código inválido')
            
            #Se asigna el votante al form para que se guarde bien
            votoForm.votante = votante
            voteData['mocion'] = mocion
            voteData['votoForm'] = votoForm
            #Se guardan los datos del voto para uso futuro, en caso que haya algún error
            mocionList.append(voteData)
            if votoForm.is_valid():
                #Como es válido, se guarda el voto, pero no se hace commit hasta el final, cuando es seguro que todos los votos sirven. Los votos se guardan en la lista que se inicializó para este fin.
                voto = votoForm.save(commit=False)
                voto.votante = votante
                votos.append(voto)
            else:
                return HttpResponse('Campo vacío')
        #Se recorren todos los candidatos
        for candidato in candidatos:
            voteData = {}
            #Se obtienen los datos de la moción actual a partir del POST
            votoCandidatoForm = VotoCandidatoForm(request.POST, prefix=candidato.pk)
            #Se revisa si el código le pertenece a algún pleno derecho. Si no, se genera un mensaje de error inmediatamente
            try:
                votante = PlenoDerecho.objects.get(pk=request.POST.get('codigo'))
            except:
                return HttpResponse('código inválido')
            
            #Se asigna el votante al form para que se guarde bien
            votoCandidatoForm.votante = votante
            voteData['candidato'] = candidato
            voteData['votoCandidatoForm'] = votoCandidatoForm
            #Se guardan los datos del voto para uso futuro, en caso que haya algún error
            candidatoList.append(voteData)
            if votoCandidatoForm.is_valid():
                #Como es válido, se guarda el voto, pero no se hace commit hasta el final, cuando es seguro que todos los votos sirven. Los votos se guardan en la lista que se inicializó para este fin.
                voto = votoCandidatoForm.save(commit=False)
                voto.votante = votante
                votosCandidatos.append(voto)
            else:
                return HttpResponse('Campo vacío')
        #Todos los campos son válidos, se procede a guardar los votos
        for voto in votos:
            voto.save()
        for voto in votosCandidatos:
            voto.save()
        return HttpResponse('success')
    else:
        mociones = Mocion.objects.filter(asamblea=Q)
        candidatos = Candidato.objects.filter(asamblea=Q)
        mocionList = []
        candidatoList = []
        for mocion in mociones:
            voteData = {}
            voto = Voto(mocion=mocion)
            votoForm = VotoForm(instance=voto, prefix=mocion.pk)
            voteData['mocion'] = mocion
            voteData['votoForm'] = votoForm
            mocionList.append(voteData)
        for candidato in candidatos:
            voteData = {}
            #Crea una nueva instancia de un voto con el candidato actual, agregándole un prefijo para obtenerla fácilmente en el futuro.
            votoCandidato = VotoCandidato(candidato=candidato)
            votoCandidatoForm = VotoCandidatoForm(instance=votoCandidato, prefix=candidato.pk)
            voteData['candidato'] = candidato
            voteData['votoCandidatoForm'] = votoCandidatoForm
            candidatoList.append(voteData)
    context = {'mocionList':mocionList, 'candidatoList':candidatoList}


    return render(request, 'voting/voting_form.html', context)

class GetVotingResults(TemplateView):
    template_name = "voting/voting_results.html"
    def get_context_data(self, **kwargs):
        context = super(GetVotingResults, self).get_context_data(**kwargs)
        mociones = Mocion.objects.filter(asamblea=self.kwargs['Q'])
        candidatos = Candidato.objects.filter(asamblea=self.kwargs['Q'])
        votaciones = []
        votacionesCandidatos = []
        for mocion in mociones:
            votos = 0
            resultados = {}
            resultados['A'] = mocion.votos.filter(votacion="A").count()
            resultados['B'] = mocion.votos.filter(votacion="B").count()
            votos += resultados['B']
            resultados['C'] = mocion.votos.filter(votacion="C").count()
            votos += resultados['C']
            resultados['F'] = mocion.votos.filter(votacion="F").count()
            votos += resultados['F']
            resultados['Q'] = int(math.ceil(votos*2.0/3))
            if resultados['F'] >= resultados['Q']:
                resultados['Resultado'] = "Pasa"
            else:
                resultados['Resultado'] = "No pasa"
            votaciones.append((mocion.nombre, resultados))
        for candidato in candidatos:
            votos = 0
            resultados = {}
            resultados['N'] = candidato.votosCandidatos.filter(votacion="N").count()
            votos += resultados['N']
            resultados['C'] = candidato.votosCandidatos.filter(votacion="C").count()
            votos += resultados['C']
            resultados['Q'] = int(math.ceil(votos*2.0/3))
            if resultados['C'] >= resultados['Q']:
                resultados['Resultado'] = "Confianza"
            else:
                resultados['Resultado'] = "No confianza"
            votacionesCandidatos.append((candidato.nombre, resultados))
        context['votaciones'] = votaciones
        context['votacionesCandidatos'] = votacionesCandidatos
        return context

class GetVoterVotes(TemplateView):
    template_name = "voting/voter_votes.html"
    def get_context_data(self, **kwargs):
        context = super(GetVoterVotes, self).get_context_data(**kwargs)
        votantes = PlenoDerecho.objects.annotate(num_votos=Count('votos'), num_votos_candidatos=Count('votosCandidatos'))
        context['votantes'] = votantes
        return context

# Create your views here.
