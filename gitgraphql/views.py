from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'gitgraphql/index.html', context)