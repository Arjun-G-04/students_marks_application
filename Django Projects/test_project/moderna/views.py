from django.shortcuts import render
from .models import Card

# Create your views here.

def index(request):
    c1 = Card()
    c2 = Card()
    c3 = Card()
    c1.title, c2.title, c3.title = 'Hey There!', 'This is A', 'Big Test'
    c1.desc, c2.desc, c3.desc = 'This is D1', 'This is D2', 'This is D3'

    return render(request, 'Moderna/index.html', {'c1':c1, 'c2':c2, 'c3':c3})