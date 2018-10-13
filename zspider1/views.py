from django.shortcuts import render
from zspider1.models import Website
# Create your views here.

def home(request):
    queryset = Website.objects.all()
    return render(request, 'home.html', {'QuerySet': queryset})

def search(request):
    q = request.GET.get('q')
    post_list = Website.objects.filter(head__icontains=q)
    return render(request, 'result.html', {'post_list': post_list})