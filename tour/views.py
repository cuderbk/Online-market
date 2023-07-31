from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import render, redirect
from .models import Category, Tour, Info
from .forms import NewTourForm, EditTourForm, NewTourInfoForm

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Category, Info

def tours(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category')

    tours = Info.objects.all()

    if query:
        tours = tours.filter(tour__tentour__icontains=query)

    if category_id:
        tours = tours.filter(category_id=category_id)

    categories = Category.objects.all()

    context = {
        'tours': tours,
        'query': query,
        'category_id': int(category_id) if category_id else None,
        'categories': categories,
    }

    return render(request, 'tour/tours.html', context=context)

def detail(request, pk):
    
    tour = get_object_or_404(Tour, pk=pk)
    tour_detail =get_object_or_404(Info, tour=tour)
    related_items = Info.objects.filter(category=tour_detail.category).exclude(pk=pk)[0:3]

    return render(request, 'tour/detail.html', {
        'tour': tour,
        'related_items': related_items
    })

@login_required
def new(request):
    if request.method == 'POST':
        tour_form = NewTourForm(request.POST, prefix='tourform')
        print('check1')
        tour_info_form = NewTourInfoForm(request.POST, request.FILES, prefix='tourinfo')
        print('check2')
        if tour_form.is_valid() and tour_info_form.is_valid():
            # Save the tour form without committing to the database yet
            tour_instance = tour_form.save(commit=False)

            # Add the user (assuming the tour is associated with the logged-in user)
            tour_instance.user = request.user

            # Save the tour to the database
            tour_instance.save()

            # Save the tour info form with the newly created tour object
            tour_info_instance = tour_info_form.save(commit=False)
            tour_info_instance.tour = tour_instance
            tour_info_instance.created_by = request.user
            # tour_info_instance.tour = tour_instance
            tour_info_instance.save()

            return render(request, 'tour/form.html')  # Assuming you have a success URL name defined in urls.py
    else:
        tour_form = NewTourForm(prefix='tourform')
        tour_info_form = NewTourInfoForm(prefix='tourinfo')

    context = {
        'tour_form': tour_form, 
        'tour_info_form': tour_info_form,
    }
    return render(request, 'tour/form.html', context=context)


@login_required
def edit(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    info = get_object_or_404(Info, tour=tour)

    if request.method == 'POST':
        tour_form = EditTourForm(request.POST, instance=tour, prefix='tourform')
        tour_info_form = NewTourInfoForm(request.POST, request.FILES, instance=info, prefix='tourinfo')

        if tour_form.is_valid() and tour_info_form.is_valid():
            tour_instance = tour_form.save()

            # Assuming you want to update the 'created_by' field with the current user
            info_instance = tour_info_form.save(commit=False)
            info_instance.created_by = request.user
            info_instance.save()

            return render(request, 'tour/form.html')  # Assuming you have a success URL name defined in urls.py
    else:
        tour_form = EditTourForm(instance=tour, prefix='tourform')
        tour_info_form = NewTourInfoForm(instance=info, prefix='tourinfo')

    context = {
        'tour_form': tour_form,
        'tour_info_form': tour_info_form,
    }
    return render(request, 'tour/form.html', context=context)

@login_required
def delete(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    info = get_object_or_404(Info, matour=tour, created_by = request.user)
    tour.delete()

    return redirect('dashboard:index')