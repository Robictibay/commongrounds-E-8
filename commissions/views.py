from django.shortcuts import render
from .models import Commissions

def commission_list(request):
    commissions = Commissions.objects.all()
    ctx = {"commissions": commissions}
    return render(request, "commissions/commission_list.html", ctx)


def commission_specific(request, pk):
    commission = Commissions.objects.get(pk=pk)
    ctx = {"commission": commission}
    return render(request, "commissions/commisssion_specific.html", ctx)

# Create your views here.
