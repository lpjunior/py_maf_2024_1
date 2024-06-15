from django.shortcuts import render


def index(request):
    return render(request, 'bemvindo/index.html', {})


def saudacao(request):
    nome = request.POST.get('nome')
    return render(request, 'bemvindo/saudacao.html', {'nome': nome})
