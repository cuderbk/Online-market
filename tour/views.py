from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Category, Tour, Info, NgaykhoihanhTourdai
from .forms import NewTourForm, EditTourForm, NewTourInfoForm, NgayKhoiHanhTourForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Category, Info, MultiStepFormModel
from formtools.wizard.views import SessionWizardView
from django.db.models import Case, When, IntegerField

from django.db import transaction

def tours(request):
    query = request.GET.get('query', '')
    # category_id = request.GET.get('category')

    tours = Info.objects.all()

    if query:
        tours = tours.filter(tour__tentour__icontains=query)

    # if category_id:
    #     tours = tours.filter(category_id=category_id)

    # categories = Category.objects.all()

    context = {
        'tours': tours,
        'query': query,
        # 'category_id': int(category_id) if category_id else None,
        # # 'categories': categories,
    }

    return render(request, 'tour/tours.html', context=context)

def detail(request, pk):
    
    tour = get_object_or_404(Tour, pk=pk)
    tour_detail =get_object_or_404(Info, tour=tour)
    # related_items = Info.objects.filter(category=tour_detail.category).exclude(pk=pk)[0:3]

    return render(request, 'tour/detail.html', {
        'tour': tour,
        # 'related_items': related_items
    })

# @login_required

# def show_business_form(wizard):
#     cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
#     return cleaned_data("is_business_guest")
# FORMS = [
#     ("tour", NewTourForm),
#     ("ngaykhoihanh", NgayKhoiHanhTourForm),
# ]

# TEMPLATES = {
#     "tour": "'tour/form.html'",
#     "ngaykhoihanh": "your_app/ngaykhoihanh_form.html",
# }
def get_generated_ma_tour():
    latest_tour = Tour.objects.order_by('ma_tour').last()
    if latest_tour:
        return latest_tour.ma_tour
    return None
class NewTourView(SessionWizardView):
    # ... (other code remains the same)
    form_list = [NewTourForm, NgayKhoiHanhTourForm]
    template_name = 'tour/form.html'
    def done(self, form_list, **kwargs):
        form_data = self.get_all_cleaned_data()

        with transaction.atomic():
            tour_instance = form_list[0].save()  # Save the Tour instance
            
            ngaykhoihanh_tourdai_data_list = []
            
            selected_dates = form_data['ngay']
            for ngay in int(selected_dates):

                ngaykhoihanh_tourdai_data = {
                    'ma_tour': tour_instance,
                    'ngay': int(ngay),
                    # ... populate other fields for NgayKhoiHanhTourdai model
                }
                ngaykhoihanh_tourdai_data_list.append(ngaykhoihanh_tourdai_data)
            
            NgaykhoihanhTourdai.objects.bulk_create([
                NgaykhoihanhTourdai(**data) for data in ngaykhoihanh_tourdai_data_list
            ])
        
        return HttpResponse('Form submitted')



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