from django.shortcuts import render, redirect
from .models import Commission
from .forms import CommissionForm


def commission_list(request):
    commissions = Commission.objects.all()
    ctx = {"commissions": commissions}
    return render(request, "commissions/commission_list.html", ctx)


def commission_specific(request, pk):
    commission = Commission.objects.get(pk=pk)
    jobs = commission.job_set.all()
    ctx = {"commission": commission, "jobs": jobs}
    return render(request, "commissions/commission_specific.html", ctx)


<<<<<<< HEAD

# Create your views here.
=======
def commission_create(request):

    form = CommissionForm()

    if request.method == "POST":
        form = CommissionForm(request.POST)

        if form.is_valid():
            commission = form.save(commit=False)
            commission.maker = request.user.profile
            commission.save()

            return redirect(
                "commission:commission_specific",
                pk=commission.pk
            )
    
    ctx = {"form": form}
    return render(request, "commission/commission_form.html", ctx)
    

def commission_update(request, pk):

    commission = Commission.objects.get(pk=pk)

    form = CommissionForm(instance=commission)

    if request.method == "POST":
        form = CommissionForm(request.POST, instance=commission)

        if form.is_valid():
            commission = form.save()
            return redirect(
                "commissions:commission_specific",
                pk=commission.pk
            )
        
    ctx = {"form": form, "commission": commission}
    return render(request, "commissions/commission_form.html", ctx)


>>>>>>> 30c113c (added Create Commission view, url, and template)
