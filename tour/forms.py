from django import forms

from .models import Tour, Info, NgaykhoihanhTourdai
from django.contrib.auth.models import User
INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'


class NewTourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('ten_tour','anh', 'ngay_batdau','giave_kl_nguoilon', 'giave_kl_treem', 'giave_kd_nguoilon', 'giave_kd_treem',
                  'sokhach_toithieu', 'sokhach_toida', 'sokhachdoan_toithieu', 'so_dem', 'so_ngay', 'ma_cn')
    def __init__(self, *args, **kwargs):
        super(NewTourForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['ten_tour'].widget.attrs['style'] = 'width:400px; height:30px;'
        self.fields['anh'].widget.attrs['style']  = 'width:800px; height:30px;'
class NgayKhoiHanhTourForm(forms.ModelForm):
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
