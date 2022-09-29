from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import render, redirect
from django.views import View

from .models import InputsValues


class MainView(View):

    def get(self, request):
        return render(request, 'main.html')

    def post(self, request):
        for key in request.POST:
            value = request.POST.get(key)
            if value != "" and key != 'csrfmiddlewaretoken':
                data = InputsValues(json={'name': key, 'value': value})
                data.save()
        return redirect('/read')


class ReadView(View):
    def get(self, request):
        data = InputsValues.objects.all()
        return render(request, 'read.html', context={'data': data})
