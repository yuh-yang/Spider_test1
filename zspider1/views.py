from django.http import HttpResponse
from django.shortcuts import render
from zspider1.models import Website
from zspider1.models import parse
# Create your views here.

def home(request):
    queryset = Website.objects.all()
    return render(request, 'home.html', {'QuerySet': queryset})

def search(request):
    q = request.GET.get('q')
    post_list = Website.objects.filter(head__icontains=q)
    return render(request, 'result.html', {'post_list': post_list})

def choose_form(request):
    return render(request, 'choose.html')

def choose(request):
    start_page = request.GET.get('choice1')
    end_page = request.GET.get('choice2')
    start_page = int(start_page)
    end_page = int(end_page)
    parse(start_page, end_page)
    return HttpResponse('爬取成功，请进入主页查看 http://127.0.0.1:8000/home')
