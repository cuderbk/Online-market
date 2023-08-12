from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Category, Tour, Info, NgaykhoihanhTourdai, DiadiemThamquan, Lichtrinhtour, DiemDulich
from .forms import NewTourForm, EditTourForm, NewTourInfoForm, NgayKhoiHanhTourForm, HanhdongLichtrinhtourForm, HdvChuyendiForm, LichtrinhChuyenForm, LichtrinhtourForm, DiadiemThamquanForm, ChuyenDiForm,DonviccdvChuyenForm, DonviccdvLienquan
from django.http import HttpResponse, JsonResponse
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

    tours = Tour.objects.all()

    if query:
        tours = tours.filter(ten_tour__icontains=query)

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
    
    try:
        lttour = Lichtrinhtour.objects.filter(ma_tour=tour)
    except Lichtrinhtour.DoesNotExist:
        return JsonResponse({'message': 'Lichtrinhtour not found'})
    
    diadiem_list = []
    for lttour in lttour:
        diadiem_thamquan = DiadiemThamquan.objects.filter(ma_tour=pk, stt_ngay=lttour.stt_ngay)
        
        if diadiem_thamquan.exists():
            diadiem_list.extend(diadiem_thamquan.values())

    return render(request, 'tour/detail.html', {
        'tour': tour,
        'diadiem_thamquan': diadiem_thamquan,
        # 'diem_dulich': diem_dulich,
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
#     "ngaykhoihanh": "your_app/ngaykhoihanh_form.html", ,DiadiemThamquanForm, NgayKhoiHanhTourForm,LichtrinhtourForm
# }
def get_generated_ma_tour():
    latest_tour = Tour.objects.order_by('ma_tour').last()
    if latest_tour:
        return latest_tour.ma_tour
    return None
class NewTourView(SessionWizardView):
    form_list = [NewTourForm, ChuyenDiForm, LichtrinhChuyenForm, DonviccdvChuyenForm]
    template_name = 'tour/form.html'
    
    def done(self, form_list, **kwargs):
        form_data = self.get_all_cleaned_data()

        with transaction.atomic():
            tour_instance = form_list[0].save()  # Save the Tour instance
            chuyendi_instance = form_list[1].save(commit=False)
            lichtrinhchuyen_instance = form_list[2].save(commit= False)
            donviccdvchuyen_instance = form_list[3].save(commit = False)
            # ngaykhoihanh_tourdai_data_list = []
            
            # selected_dates = form_list[1].cleaned_data['selected_dates']
            TourInstance=Tour.objects.annotate(
                    sort_order=Case(
                        When(ma_cn=form_data['ma_cn'], then=1), default=0, output_field=IntegerField()
                    )                
                ).order_by('ma_tour').last()
            
            chuyendi_instance.ma_tour = TourInstance
            chuyendi_instance.save()
            
            lichtrinhchuyen_instance.chuyendi= chuyendi_instance
            lichtrinhchuyen_instance.save()
            
            donviccdvchuyen_instance.lichtrinhchuyen = lichtrinhchuyen_instance
            donviccdvchuyen_instance.save()
            # lichtrinhtour_instance = form_list[2].save(commit=False)
            # lichtrinhtour_instance.ma_tour = TourInstance
            # lichtrinhtour_instance.save()
            
            # lichtrinhchuyen_instance = form_list[3].save(commit=False)
            # lichtrinhchuyen_instance.ma_tour = TourInstance.ma_tour
            # lichtrinhchuyen_instance.ngay_khoihanh = chuyendi_instance.ngay_khoihanh
            # lichtrinhchuyen_instance.save()
            # lichtrinhchuyen_instance.id = chuyendi_instance

            
        return HttpResponse('Success')



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