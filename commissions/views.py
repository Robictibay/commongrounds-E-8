from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Commission, Job, JobApplication
from .forms import CommissionForm


def commission_list(request):
    commissions = Commission.objects.all()
    ctx = {"commissions": commissions}
    return render(request, "commissions/commission_list.html", ctx)


def commission_specific(request, pk):
    commission = Commission.objects.get(pk=pk)
    jobs = commission.job_set.all()

    if request.method == "POST":

        if not request.user.is_authenticated:
            return redirect("login")
    
        job = Job.objects.get(
            pk=request.POST.get("job_id")
        )

        JobApplication.objects.create(
            job=job,
            applicant=request.user.profile
        )

        return redirect(
            "commissions:commission_specific",
            pk=commission.pk
        )
    
    ctx = {"commission": commission, "jobs": jobs}
    return render(request, "commissions/commission_specific.html", ctx)

<<<<<<< HEAD

<<<<<<< HEAD

# Create your views here.
=======
=======
@login_required
>>>>>>> 92a9ca9 (restricted create commissions and update commissions based on login)
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
    
@login_required
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
