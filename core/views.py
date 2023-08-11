from django.shortcuts import render, redirect

from tour.models import Category, Tour

from .forms import SignupForm

def index(request):
    tours = Tour.objects.all()[0:6]

    return render(request, 'core/index.html', {
        'tours': tours,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })