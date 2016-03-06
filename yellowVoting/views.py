#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from .models import Voto, Mocion, PlenoDerecho
from django.forms import modelformset_factory
from .forms import VotoForm

def votingView(request):
    if request.method == 'POST':
        mociones = Mocion.objects.filter(asamblea='Q1')
        mocionList = []
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
                voto.save()
                return HttpResponse('success')
    else:
        mociones = Mocion.objects.filter(asamblea='Q1')
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

# Create your views here.
