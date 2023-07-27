from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewTourForm, EditTourForm
from .models import Category, Tour

def tours(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    tours = Tour.objects.filter(is_sold=False)

    if category_id:
        tours = tours.filter(category_id=category_id)

    if query:
        tours = tours.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'tour/tours.html', {
        'tours': tours,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

def detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    related_tours = Tour.objects.filter(category=tour.category, is_sold=False).exclude(pk=pk)[0:6]

    return render(request, 'tour/detail.html', {
        'tour': tour,
        'related_tours': related_tours
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewTourForm(request.POST, request.FILES)

        if form.is_valid():
            tour = form.save(commit=False)
            tour.created_by = request.user
            tour.save()

            return redirect('tour:detail', pk=tour.MaTour)
    else:
        form = NewTourForm()

    return render(request, 'tour/form.html', {
        'form': form,
        'title': 'New tour',
    })

@login_required
def edit(request, pk):
    tour = get_object_or_404(Tour, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditTourForm(request.POST, request.FILES, instance=tour)

        if form.is_valid():
            form.save()

            return redirect('tour:detail', pk=tour.MaTour)
    else:
        form = EditTourForm(instance=tour)

    return render(request, 'tour/form.html', {
        'form': form,
        'title': 'Edit tour',
    })

@login_required
def delete(request, pk):
    tour = get_object_or_404(Tour, pk=pk, created_by=request.user)
    tour.delete()

    return redirect('dashboard:index')