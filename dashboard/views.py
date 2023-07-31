from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from tour.models import Tour

@login_required
def index(request):
    tours = Tour.objects.all() #use filter alreaddy

    return render(request, 'dashboard/index.html', {
        'tours': Tour,
    })
