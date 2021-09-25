from django.shortcuts import render, redirect
from django.http import HttpResponse

from .github_response import *
from .forms import CustomerForm


def index(request):
    form = CustomerForm
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        form.login = request.POST['github_login']
        if form.is_valid():
            form.save()
    name, response = get_repositories(form.login)
    context = {'form': form, 'response': response, "name": name}
    return render(request, 'gitgraphql/index.html', context)




