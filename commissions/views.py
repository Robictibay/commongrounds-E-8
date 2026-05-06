from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Commission, Job, JobApplication
from .forms import CommissionForm


def commission_list(request):
    commissions = Commission.objects.all()

    created_commissions = []
    applied_commissions = []

    if request.user.is_authenticated:

        created_commissions = Commission.objects.filter(
            maker=request.user.profile
        )

        applied_commissions = Commission.objects.filter(
            job__jobapplication__applicant=request.user.profile
        ).distinct()

        commissions = Commission.objects.exclude(
            pk__in=created_commissions
        ).exclude(
            pk__in=applied_commissions
        )
        
    ctx = {"commissions": commissions, "created_commissions": created_commissions, "applied_commissions": applied_commissions}
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
        
        already_applied = JobApplication.objects.filter(
            job=job,
            applicant=request.user.profile
        ).exists()
        
        if already_applied:
            return redirect(
                "commissions:commission_specific",
                pk=commission.pk
            )
        
        JobApplication.objects.create(
            job=job,
            applicant=request.user.profile
        )

        accepted_count = JobApplication.objects.filter(
            job=job,
            status="Accepted"
        ).count()

        if accepted_count >= job.manpower_required:
            job.status = "Full"
            job.save()

        all_full = True

        for current_job in jobs:
            if current_job.status != "Full":
                all_full = False
        
        if all_full:
            commission.status = "Full"
            commission.save()
        return redirect(
            "commissions:commission_specific",
            pk=commission.pk
        )
    
    total_manpower = 0
    open_manpower = 0

    for job in jobs:
        accepted_count = JobApplication.objects.filter(
            job=job,
            status="Accepted"
        ).count()

        total_manpower += job.manpower_required
        open_manpower += job.manpower_required - accepted_count

    ctx = {"commission": commission, "jobs": jobs, "total_manpower": total_manpower, "open_manpower": open_manpower}
    return render(request, "commissions/commission_specific.html", ctx)

<<<<<<< HEAD

<<<<<<< HEAD

# Create your views here.
=======
=======
@login_required
>>>>>>> 92a9ca9 (restricted create commissions and update commissions based on login)
def commission_create(request):

    if request.user.profile.role != "Commission Maker":
        return redirect("commissions:commission_list")

    form = CommissionForm()

    if request.method == "POST":
        form = CommissionForm(request.POST)

        if form.is_valid():
            commission = form.save(commit=False)
            commission.maker = request.user.profile
            commission.save()

            return redirect(
                "commissions:commission_specific",
                pk=commission.pk
            )
    
    ctx = {"form": form}
    return render(request, "commissions/commission_form.html", ctx)
    
@login_required
def commission_update(request, pk):

    if request.user.profile.role != "Commission Maker":
        return redirect("commissions:commission_list")
    
    commission = Commission.objects.get(pk=pk)

    if commission.maker != request.user.profile:
        return redirect(
            "commissions:commission_specific",
            pk=commission.pk
        )

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
