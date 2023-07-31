from django import forms

from .models import Tour, Info, Status, City, Category
from django.contrib.auth.models import User
INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'


class NewTourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ('tentour', 'giavelenguoilon', 'giaveletreem', 'giavedoannguoilon', 'giavedoantreem',
                  'sokhachtourtoithieu', 'sokhachtourtoida', 'sokhachdoantoithieu', 'sodem', 'songay', 'machinhanh')

class NewTourInfoForm(forms.ModelForm):
    class Meta:
        model= Info
        fields =('category','city','image','description','status')


class EditTourForm(forms.ModelForm):

     class Meta:
        model = Tour
        fields = ('tentour', 'giavelenguoilon', 'giaveletreem', 'giavedoannguoilon', 'giavedoantreem',
                  'sokhachtourtoithieu', 'sokhachtourtoida', 'sokhachdoantoithieu', 'sodem', 'songay', 'machinhanh')
class EditInfoTourForm(forms.ModelForm):
     class Meta:
        model= Info
        fields =('category','city','image','description','status')
