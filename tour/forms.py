from django import forms

from .models import Tour, Info, NgaykhoihanhTourdai, ChiNhanh
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout


from django.utils.translation import gettext_lazy as _
from datetime import datetime

class NewTourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('ten_tour', 'anh', 'ngay_batdau', 'giave_kl_nguoilon', 'giave_kl_treem', 'giave_kd_nguoilon', 'giave_kd_treem',
                  'sokhach_toithieu', 'sokhach_toida', 'sokhachdoan_toithieu', 'so_dem', 'so_ngay', 'ma_cn')
        # ma_cn = forms.ModelChoiceField(queryset = ChiNhanh.objects.all())
        labels = {
            'ten_tour': _('Tên tour'),
            'anh': _('Ảnh'),
            'ngay_batdau': _('Ngày bắt đầu'),
            'giave_kl_nguoilon': _('Giá vé lẻ người lớn'),
            'giave_kl_treem': _('Giá vé lẻ trẻ em'),
            'giave_kd_nguoilon': _('Giá vé đoàn người lớn'),
            'giave_kd_treem': _('Giá vé đoàn trẻ em'),
            'sokhach_toithieu': _('Số khách tôi thiểu'),
            'sokhach_toida': _('Số khách tối đa'),
            'sokhachdoan_toithieu': _('Số khách đoàn tối thiểu'),
            'so_dem': _('Số đêm'),
            'so_ngay': _('Số ngày'),
            'ma_cn': _('Chi Nhánh')
        }
        widgets = {
            'ten_tour': forms.TextInput(attrs={'class': 'form-input'}),
            'anh': forms.TextInput(attrs={'class': 'form-input'}),
            'ngay_batdau': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'giave_kl_nguoilon': forms.NumberInput(attrs={'class': 'form-input'}),
            'giave_kl_treem': forms.NumberInput(attrs={'class': 'form-input'}),
            'giave_kd_nguoilon': forms.NumberInput(attrs={'class': 'form-input'}),
            'giave_kd_treem': forms.NumberInput(attrs={'class': 'form-input'}),
            'sokhach_toithieu': forms.NumberInput(attrs={'class': 'form-input'}),
            'sokhach_toida': forms.NumberInput(attrs={'class': 'form-input'}),
            'sokhachdoan_toithieu': forms.NumberInput(attrs={'class': 'form-input'}),
            'so_dem': forms.NumberInput(attrs={'class': 'form-input'}),
            'so_ngay': forms.NumberInput(attrs={'class': 'form-input'}),
            'ma_cn': forms.Select(attrs={'class': 'form-input'}),
        }


class NgayKhoiHanhTourForm(forms.ModelForm):
    ngay = forms.MultipleChoiceField(
        choices=[(str(i), i) for i in range(1, 32)],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
    )
    
    class Meta:
        model = NgaykhoihanhTourdai
        fields = ('ngay',)

class NewTourInfoForm(forms.ModelForm):
    class Meta:
        model= Info
        fields =('category','diemxp','diemden','description','status')


class EditTourForm(forms.ModelForm):

     class Meta:
        model = Tour
        model = Tour
        fields = ('ten_tour','anh', 'ngay_batdau','giave_kl_nguoilon', 'giave_kl_treem', 'giave_kd_nguoilon', 'giave_kd_treem',
                  'sokhach_toithieu', 'sokhach_toida', 'sokhachdoan_toithieu', 'so_dem', 'so_ngay', 'ma_cn')
     class Meta:
        model= Info
        fields =('category','diemxp','diemden','description','status')
