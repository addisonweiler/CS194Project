from django.shortcuts import render
from django_facebook.decorators import canvas_only

@canvas_only
def home(request):
    return render(request, 'home.html')
