#coding=utf-8
from __future__ import unicode_literals
from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse
from .models import Voto, Mocion, PlenoDerecho
from django.forms import modelformset_factory
from django.views.generic.base import TemplateView
from .forms import VotoForm

def votingView(request, Q):
    if request.method == 'POST':
        mociones = Mocion.objects.filter(asamblea=Q)
        mocionList = []
        votos = []
        for mocion in mociones:
            voteData = {}
            votoForm = VotoForm(request.POST, prefix=mocion.pk)
            try:
                votante = PlenoDerecho.objects.get(pk=request.POST.get('codigo'))
            except:
                return HttpResponse('código inválido')
                
            votoForm.votante = request.POST.get('codigo')
            voteData['mocion'] = mocion
            voteData['votoForm'] = votoForm
            mocionList.append(voteData)
            if votoForm.is_valid():
                voto = votoForm.save(commit=False)
                voto.votante = votante
                votos.append(voto)
            else:
                return HttpResponse('Campo vacío')
        for voto in votos:
            voto.save()
        return HttpResponse('success')
    else:
        mociones = Mocion.objects.filter(asamblea=Q)
        mocionList = []
        for mocion in mociones:
            voteData = {}
            voto = Voto(mocion=mocion)
            votoForm = VotoForm(instance=voto, prefix=mocion.pk)
            voteData['mocion'] = mocion
            voteData['votoForm'] = votoForm
            mocionList.append(voteData)
    context = {'mocionList':mocionList}


    return render(request, 'voting/voting_form.html', context)

class GetVotingResults(TemplateView):
    template_name = "voting/voting_results.html"
    def get_context_data(self, **kwargs):
        context = super(GetVotingResults, self).get_context_data(**kwargs)
        mociones = Mocion.objects.filter(asamblea=self.kwargs['Q'])
        votaciones = {}
        for mocion in mociones:
            resultados = {}
            resultados['A'] = mocion.votos.filter(votacion="A").count()
            resultados['B'] = mocion.votos.filter(votacion="B").count()
            resultados['C'] = mocion.votos.filter(votacion="C").count()
            resultados['F'] = mocion.votos.filter(votacion="F").count()
            votaciones[mocion.nombre] = resultados
        context['votaciones'] = votaciones
        return context

class GetVoterVotes(TemplateView):
    template_name = "voting/voter_votes.html"
    def get_context_data(self, **kwargs):
        context = super(GetVoterVotes, self).get_context_data(**kwargs)
        votantes = PlenoDerecho.objects.annotate(num_votos=Count('voto'))
        context['votantes'] = votantes
        return context

# Create your views here.
