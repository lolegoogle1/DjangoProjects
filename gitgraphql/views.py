from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .github_response import *
from .forms import CustomerForm


def index(request):
    form = CustomerForm
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        form.login = request.POST['github_login']
        if form.is_valid():
            form.save()
            name, repositories = get_repositories(form.login)
            if "Credentials" in name:
                return HttpResponse(name)
            elif "Connection" in name:
                return HttpResponse(name)
            elif "NOUSER" in name:
                return HttpResponse(name)

            return JsonResponse({name: repositories})

    context = {'form': form}
    return render(request, 'gitgraphql/index.html', context)
