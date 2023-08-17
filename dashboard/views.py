from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse

from .forms import YearForm

@login_required
def index(request):
    form = YearForm(request.GET)
    if form.is_valid():
        year = form.cleaned_data['year']
        with connection.cursor() as cursor:
            cursor.callproc('cau_I_3_ThongKeDoanhThu', [year])
            results = cursor.fetchall()
        # return HttpResponse(results)
        return render(request, 'dashboard/index.html', {'results': results})
    return render(request, 'dashboard/index.html', {'form': form})
