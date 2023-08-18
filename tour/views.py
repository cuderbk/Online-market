from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory
from django.urls import reverse
from django.shortcuts import render, redirect
from core.models import KhachDoan, KhachDoanLe, KhachHang, Phieudk, NhanVien
from .models import Category, Tour, Info, DiadiemThamquan, DiadiemThamquan, Lichtrinhtour, DiemDulich, LichtrinhChuyen, Chuyendi
from .forms import NewTourForm, EditTourForm, NewTourInfoForm, NgayKhoiHanhTourForm, HanhdongLichtrinhtourForm, HdvChuyendiForm, LichtrinhChuyenForm, LichtrinhtourForm, DiadiemThamquanForm, ChuyenDiForm,DonviccdvChuyenForm, BookingForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Category, Info, MultiStepFormModel
from formtools.wizard.views import SessionWizardView
from django.db.models import Case, When, IntegerField

from django.utils import timezone
from datetime import timedelta
from collections import OrderedDict
from django.db import transaction

from django.forms import BaseFormSet
from django.urls import reverse

from django.forms import formset_factory

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
    diadiem_thamquan = DiadiemThamquan.objects.filter(ma_tour=pk)
    return render(request, 'tour/detail.html', {
        'tour': tour,
        'diadiem_thamquan': diadiem_thamquan,
    })

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
                    lichtrinhtour_instance = Lichtrinhtour(stt_ngay=1, ma_tour=TourInstance)
                    lichtrinhtour_instance.save()

                    # Redirect to DiadiemThamquanForm for each Lichtrinhtour
                    return redirect('tour:add_diadiem_thamquan', tour = TourInstance.ma_tour, day_number=1)    

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
            diadiem.ma_tour = lichtrinhtour_instance
            diadiem.stt_ngay = lichtrinhtour_instance
            diadiem.lichtrinhtour = lichtrinhtour_instance
            diadiem.save()
            
            if 'save_and_add_another' in request.POST:
                return redirect('tour:add_diadiem_thamquan', tour = TourInstance.ma_tour, day_number=day)
            elif 'hdtour' in request.POST:
                return redirect('tour:add_hanhdong_lichtrinh_tour', tour = TourInstance.ma_tour, day_number=day)
            else:
                # Handle final submission
                return redirect('tour:tours')
    
    else:
        diadiem_form = DiadiemThamquanForm()
    
    context = {
        'diadiem_form': diadiem_form,
        'has_next_day': has_next_day,
        'day': day  ,
    }
    
    return render(request, 'tour/diadiem_thamquan.html', context)

def add_hanhdong_lichtrinh_tour(request,tour,day_number):
    TourInstance = get_object_or_404(Tour, pk=tour)
    has_next_day = day_number < TourInstance.so_ngay
    day = day_number
    lichtrinhtour_instance = get_object_or_404(Lichtrinhtour,ma_tour=tour, stt_ngay=day_number )
    if request.method == 'POST':
        hdtour_form = HanhdongLichtrinhtourForm(request.POST)
        
        if hdtour_form.is_valid():
            
            hdtour = hdtour_form.save(commit=False)
            hdtour.lichtrinhtour = lichtrinhtour_instance
            hdtour.ma_tour = lichtrinhtour_instance.ma_tour
            hdtour.stt_ngay = lichtrinhtour_instance.stt_ngay
            hdtour.save()
            if 'save_and_add_another' in request.POST:
                return redirect('tour:add_hanhdong_lichtrinh_tour   ', tour = TourInstance.ma_tour, day_number=day)
            elif 'next_day' in request.POST:
                return redirect('tour:add_diadiem_thamquan', tour = TourInstance.ma_tour, day_number=day +1 )
            else:
                # Handle final submission
                return redirect('tour:tours')
    
    else:
        hdtour_form = HanhdongLichtrinhtourForm()
    
    context = {
        'hdtour_form': hdtour_form,
        'has_next_day': has_next_day,
        'day': day,
    }
    
    return render(request, 'tour/hdtour.html', context)

def buy(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    today = timezone.now().date()
    chuyendi = Chuyendi.objects.filter(ma_tour=pk, ngay_khoihanh__gt=today) if tour.so_ngay == 1 else Chuyendi.objects.filter(ma_tour=pk, ngay_khoihanh__gt=today+timedelta(days=2))
    nhan_vien = NhanVien.objects.filter(ma_cn=tour.ma_cn, cong_viec=1).first()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data['email']
            phone = data['phone']
            chuyendi = Chuyendi.objects.filter(ma_tour=pk, ngay_khoihanh=data['departure_date']).first()
            existing_khachhang = KhachHang.objects.filter(email=email, sdt=phone).first()
            if existing_khachhang:
                khach_hang = existing_khachhang
            else:
                khach_hang = KhachHang.objects.create(
                        ho_ten = data['name'],
                        email = email,
                        sdt = phone,
                        dia_chi = data['address'],
                )
                
            # if data['participants'] >= tour.sokhachdoan_toithieu:
            #     khach_doan = KhachDoan.objects.create(
            #         ma_daidien = khach_hang
            #     )

            # if KhachDoan.objects.filter(ma_doan=data['group']).exists():
            #         khach_doan = KhachDoan.objects.filter(ma_doan=data['group']).first()
            #         khach_doan_le = KhachDoanLe.objects.create(
            #             ma_doan = khach_doan,
            #             ma_kh = khach_hang
            #         )
                
            phieudk = Phieudk.objects.create(
                ngay_dangky=today,
                ma_nv= nhan_vien,  # Assuming you have a logged-in user
                ma_kh=khach_hang,
                ma_tour=chuyendi.ma_tour,
                ngay_khoihanh=chuyendi.ngay_khoihanh,
                chuyendi=chuyendi
            )
            
            # for key, value in khach_doan.__dict__.items():
            #     print(f"{key}: {value}")
            return render(request, 'tour/booking_success.html')  # Redirect to a success page
    else:
        form = BookingForm()
    return render(request, 'tour/buy.html', {
        'tour': tour,
        'chuyendi': chuyendi,
        'form': form,
    })
    
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