from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Category, Tour, Info, DiadiemThamquan, DiadiemThamquan, Lichtrinhtour, DiemDulich, LichtrinhChuyen
from .forms import NewTourForm, EditTourForm, NewTourInfoForm, NgayKhoiHanhTourForm, HanhdongLichtrinhtourForm, HdvChuyendiForm, LichtrinhChuyenForm, LichtrinhtourForm, DiadiemThamquanForm, ChuyenDiForm,DonviccdvChuyenForm, DonviccdvLienquan
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Category, Info, MultiStepFormModel
from formtools.wizard.views import SessionWizardView
from django.db.models import Case, When, IntegerField

from datetime import timedelta
from collections import OrderedDict
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
    tour_detail =get_object_or_404(Info, tour=tour)
    # related_items = Info.objects.filter(category=tour_detail.category).exclude(pk=pk)[0:3]

    return render(request, 'tour/detail.html', {
        'tour': tour,
        # 'related_items': related_items
    })

# @login_required

# def get_tour_instace():
#     return Tour.objects.all().last()
# def tour_view(request):
#     if request.method == 'POST':
#         form = NewTourForm(request.POST)
#         if form.is_valid():
#             tour = form.save()
#             tour_instance = get_tour_instace()
#             if tour.so_ngay:
#                 return redirect(reverse('tour:ngaykhoihanh_tour'))
#             else:
#                 return redirect(reverse('tour:diadiem_thamquan'))
#     else:
#         form = NewTourForm()
#     return render(request, 'tour/tour.html', {'form': form})

# def ngaykhoihanh_tour_view(request):
#     if request.method == 'POST':
#         form = NgayKhoiHanhTourForm(request.POST)
#         if form.is_valid():
#             ngaykhoihanh_tour = form.save(commit=False)
#             tour_instance = get_tour_instace
#             ngaykhoihanh_tour.ma_tour = ma_tour
#             ngaykhoihanh_tour.save()
#             return redirect('tours/diadiem_thamquan', ma_tour = tour_instance)
#     else:
#         form = NgayKhoiHanhTourForm()
#     return render(request, 'tours/ngaykhoihanh_tour.html', {'form': form})

# def diadiem_thamquan_view(request, ma_tour):
#     if request.method == 'POST':
#         form = DiadiemThamquanForm(request.POST)
#         if form.is_valid():
#             diadiem_thamquan = form.save(commit=False)
#             diadiem_thamquan.ma_tour = ma_tour
#             diadiem_thamquan.save()
#             if 'save_and_add_another' in request.POST:
#                 return redirect('tours/diadiem_thamquan', ma_tour=ma_tour)
#             else:
#                 return redirect('tours/lichtrinh_tour', ma_tour=ma_tour)
#     else:
#         form = DiadiemThamquanForm()
#     return render(request, 'tours/diadiem_thamquan.html', {'form': form})

# def lichtrinh_tour_view(request, ma_tour):
#     Lichtrinhtour_instance = []
#     for i in range(1, Tour.objects.get(id=ma_tour).so_ngay + 1):
#         Lichtrinhtour_instance.append(Lichtrinhtour(stt_ngay=i))
#     if request.method == 'POST':
#         forms = [LichtrinhtourForm(request.POST, prefix=str(i), instance=instance) for i, instance in enumerate(Lichtrinhtour_instance)]
#         if all([form.is_valid() for form in forms]):
#             for form in forms:
#                 lichtrinh_tour = form.save(commit=False)
#                 tour_instance = get_tour_instace
#                 lichtrinh_tour.ma_tour = tour_instance
#                 lichtrinh_tour.save()
#             return HttpResponse('success')
#     else:
#         forms = [LichtrinhtourForm(prefix=str(i), instance=instance) for i, instance in enumerate(Lichtrinhtour_instance)]
#     return render(request, 'tours/lichtrinh_tour.html', {'forms': forms})

def show_ngaykh_tourdaingay_form(wizard):
    cleaned_data= wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('so_dem')

from collections import OrderedDict
from django.forms import BaseFormSet

def create_tour(request):
        if request.method == 'POST':
            tour_form = NewTourForm(request.POST)
            ngay_khoi_hanh_form = NgayKhoiHanhTourForm(request.POST)
            lichtrinhtour_form = LichtrinhtourForm(request.POST)

            if tour_form.is_valid():
                tour = tour_form.save(commit=False)
                has_ngay = tour.so_ngay > 0
                tour.save()
                TourInstance=Tour.objects.filter(ma_cn = tour.ma_cn).order_by('ma_tour').last()
                if has_ngay:
                    return redirect('tour:add_ngaykhoihanh_tour', tour = TourInstance.ma_tour)
                else:
                    if lichtrinhtour_form.is_valid():
                        for i in range(1, tour.so_ngay + 1):
                            lichtrinhtour_instance = Lichtrinhtour(stt_ngay=i)
                            lichtrinhtour_instance.save()
                            tour.lichtrinhtour_set.add(lichtrinhtour_instance)

                    return redirect(reverse('tour:lichtrinh_tour'), tour = TourInstance)

        else:
            tour_form = NewTourForm()
            ngay_khoi_hanh_form = NgayKhoiHanhTourForm()
            lichtrinhtour_form = LichtrinhtourForm()

        context = {
            'tour_form': tour_form,
            'ngay_khoi_hanh_form': ngay_khoi_hanh_form,
            'lichtrinhtour_form': lichtrinhtour_form,
        }

        return render(request, 'tour/create_tour.html', context)
from django.urls import reverse

from django.forms import formset_factory

def add_ngaykhoihanh_tour(request, tour):
    TourInstance = get_object_or_404(Tour, pk=tour)
    NgayKhoiHanhFormSet = formset_factory(NgayKhoiHanhTourForm, extra=1)
    
    if request.method == 'POST':
        formset = NgayKhoiHanhFormSet(request.POST)
        
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    ngay_khoi_hanh = form.save(commit=False)
                    ngay_khoi_hanh.ma_tour = TourInstance
                    ngay_khoi_hanh.save()
            
            if 'save_and_add_another' in request.POST:
                return redirect('tour:add_ngaykhoihanh_tour', tour=TourInstance.ma_tour)
            elif 'next' in request.POST:
                # Redirect to LichtrinhtourForm after NgaykhoihanhTourdaiForm is done
                for i in range(1, TourInstance.so_ngay + 1):
                    lichtrinhtour_instance = Lichtrinhtour(stt_ngay=i, ma_tour=TourInstance)
                    lichtrinhtour_instance.save()

                    # Redirect to DiadiemThamquanForm for each Lichtrinhtour
                return redirect('tour:add_diadiem_thamquan', tour = TourInstance.ma_tour, day_number=1)              


    else:
        formset = NgayKhoiHanhFormSet()

    context = {
        'formset': formset,
        'tour': TourInstance,
    }
    
    return render(request, 'tour/ngaykhoihanh_tour.html', context)


def add_diadiem_thamquan(request, tour, day_number):
    TourInstance = get_object_or_404(Tour, pk=tour)
    has_next_day = day_number < TourInstance.so_ngay
    day = day_number
    lichtrinhtour_instance = get_object_or_404(Lichtrinhtour,ma_tour=tour, stt_ngay=day_number )
    if request.method == 'POST':
        diadiem_form = DiadiemThamquanForm(request.POST)
        
        if diadiem_form.is_valid():
            diadiem = diadiem_form.save(commit=False)
            diadiem.lichtrinhtour = lichtrinhtour_instance
            diadiem.ma_tour = TourInstance.ma_tour
            diadiem.stt_ngay = day
            diadiem.save()
            
            if 'save_and_add_another' in request.POST:
                return redirect('tour:add_diadiem_thamquan', tour = TourInstance.ma_tour, day_number=day)
            elif 'next_day' in request.POST:
                return redirect('tour:add_diadiem_thamquan', tour = tour, day_number=day_number + 1)
            else:
                # Handle final submission
                return redirect('tour:tours')
    
    else:
        diadiem_form = DiadiemThamquanForm()
    
    context = {
        'diadiem_form': diadiem_form,
        'has_next_day': has_next_day,
    }
    
    return render(request, 'tour/diadiem_thamquan.html', context)


class NewTourView(SessionWizardView):
    form_list = [NewTourForm, NgayKhoiHanhTourForm]  
    template_name = 'tour/form.html'
    condition_dict = {"1": show_ngaykh_tourdaingay_form}
    diadiemthamquan_list = []

    # def get_context_data(self, form, **kwargs):
    #     context = super().get_context_data(form=form, **kwargs)
    #     context['form_list'] = self.get_form_list()
    #     return context
    
    def post(self, *args, **kwargs):

        form = self.get_form()
        if self.steps.current == '1':
            form_data=self.get_form_step_data(form)
            
            # self.storage.set_step_files(self.steps.current, self.process_step_files(form))
            
            if'save_and_add_another' in self.request.POST:
                
                self.diadiemthamquan_list.append(form_data)
            elif 'wizard_goto_step' in self.request.POST:
                # self.diadiemthamquan_list.append(form_data)
                pass
                    

        return super(NewTourView, self).post(*args, **kwargs)




    def done(self, form_list, **kwargs):
        form_data = self.get_all_cleaned_data()

        with transaction.atomic():
            
            tour_instance = form_list[0] # Save the Tour instance
            tour_instance.save()
            TourInstance=Tour.objects.filter(ma_cn = form_data['ma_cn']).order_by('ma_tour').last()
            
            if tour_instance.cleaned_data.get('so_dem'):
                ngaykhtour_instance = form_list[1].save(commit=False)
                

                ngaykhtour_instance.ma_tour = TourInstance
                ngaykhtour_instance.save()
                
                
                
                lichtrinhtour_instance = []
                for i in range(form_data['so_ngay']):
                    lichtrinhtour_instance.append(Lichtrinhtour(
                        ma_tour = TourInstance,
                        # ngay_khoihanh=ngaybatdau + timedelta(days=i),
                        stt_ngay= i+1,
                    ))
                    lichtrinhtour_instance[i].save()

                    # diadiemthamquan_instance = form_list[2].save(commit=False)
                    # diadiemthamquan_instance.lichtrinhtour= lichtrinhtour_instance
                    # diadiemthamquan_instance.save()
                # for diadiem_data in self.diadiemthamquan_list:
                diadiemthamquan_instance = form_list[0].save()
                diadiemthamquan_instance.lichtrinhtour = lichtrinhtour_instance
                diadiemthamquan_instance.save()
            # chuyendi_instance.ma_tour = TourInstance
            # chuyendi_instance.save()
            
            # # Calculate the difference between ngayketthuc and ngaybatdau
            # ngaybatdau = form_data['chuyendi_form']['ngaybatdau']
            # ngayketthuc = form_data['chuyendi_form']['ngayketthuc']
            # date_diff = (ngayketthuc - ngaybatdau).days
            
            # dvccdvchuyen_forms = []
            # for i in range(date_diff):
            #     lichtrinhchuyen_instance = LichtrinhChuyen(
            #         # ma_tour=form_data['ma_tour'],
            #         # ngay_khoihanh=ngaybatdau + timedelta(days=i),
            #         stt_ngay= i,
            #         chuyendi=chuyendi_instance
            #     )
            #     lichtrinhchuyen_instance.save()

            #     dvccdvchuyen_form = form_list[2].cleaned_data
            #     # Set fields for DvccDvchuyendiForm based on your logic
            #     dvccdvchuyen_form['lichtrinhchuyen'] = lichtrinhchuyen_instance
            #     dvccdvchuyen_forms.append(dvccdvchuyen_form)

# Now use the adjusted form_data to create and save instances
# (Note: You will need to adjust this part based on your actual code structure)
            # for dvccdvchuyen_form in dvccdvchuyen_forms:
            #     dvccdvchuyen_instance = DonviccdvChuyenForm(**dvccdvchuyen_form)
            #     dvccdvchuyen_instance.save()
                    
    
            return HttpResponse('success')


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