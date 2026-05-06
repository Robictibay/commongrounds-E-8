from django.shortcuts import render
from .models import Commission


def commission_list(request):
    commissions = Commission.objects.all()
    ctx = {"commissions": commissions}
    return render(request, "commissions/commission_list.html", ctx)


def commission_specific(request, pk):
    commission = Commission.objects.get(pk=pk)
    ctx = {"commission": commission}
    return render(request, "commissions/commission_specific.html", ctx)



# Create your views here.
