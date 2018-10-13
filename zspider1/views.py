from django.shortcuts import render
from zspider1.models import Website
# Create your views here.

def home(request):
    queryset = Website.objects.all()
    return render(request, 'home.html', {'QuerySet': queryset})

