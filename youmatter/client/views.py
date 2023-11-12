from django.shortcuts import render
from django.views import View

# Create your views here.

class Index(View):
    def get(self, request, *arg, **kwargs):
        return render(request, 'client/index.html')

class community(View):
    def get(self, request, *arg, **kwargs):
        return render(request, 'client/community.html')

class Shop(View):
    def get(self, request, *arg, **kwargs):
        return render(request, 'client/shop.html', context)