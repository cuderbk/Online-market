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
FORMS = [
    ("tour", NewTourForm),
    ("ngaykhoihanh", NgayKhoiHanhTourForm),
]

TEMPLATES = {
    "tour": "'tour/form.html'",
    "ngaykhoihanh": "your_app/ngaykhoihanh_form.html",
}
def get_generated_ma_tour():
    latest_tour = Tour.objects.order_by('ma_tour').last()
    if latest_tour:
        return latest_tour.ma_tour
    return None
class NewTourView(SessionWizardView):
    form_list = [NewTourForm, NgayKhoiHanhTourForm]
    template_name = 'tour/form.html'

    def done(self, form_list, **kwargs):
        form_data = self.get_all_cleaned_data()

        # tour_data = {
        #     'ten_tour': form_data['ten_tour'],
        #     'anh': form_data['anh'],
        #     'ngay_batdau': form_data['ngay_batdau'],
        #     'sokhach_toida': form_data['sokhach_toida'],
        #     'giave_kl_nguoilon': form_data['giave_kl_nguoilon'],
        #     'giave_kl_treem': form_data['giave_kl_treem'],
        #     'giave_kd_nguoilon': form_data['giave_kd_nguoilon'],
        #     'giave_kd_treem': form_data['giave_kd_treem'],
        #     'sokhach_toithieu': form_data['sokhach_toithieu'],
        #     'sokhachdoan_toithieu': form_data['sokhachdoan_toithieu'],
        #     'so_dem': form_data['so_dem'],
        #     'so_ngay': form_data['so_ngay'],
        #     'ma_cn': form_data['ma_cn'],
        # }


        tour_instance = form_list[0].cleaned_data
        tour = tour_instance.save(commit=False)
        tour.save()

        ngaykhoihanh_data = {
            'ma_tour':Tour.objects.order_by('ma_tour').last(),
            'ngay': form_data['ngay'],
            # ... populate other fields for NgaykhoihanhTourdai model
        }

        ngaykhoihanh_instance = NgaykhoihanhTourdai(**ngaykhoihanh_data)
        ngaykhoihanh_instance.save()


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