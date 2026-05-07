from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Project, ProjectRating
from .forms import ProjectRatingForm, ProjectReviewForm, ProjectForm
from django.shortcuts import redirect
from accounts.mixins import RoleRequiredMixin
from django.db.models import Avg
from datetime import date
from .models import Favorite


class ProjectListView(ListView):
    model = Project
    template_name = "diyprojects/project_list.html"
    context_object_name = "projects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            profile = user.profile
            created_pk = Project.objects.filter(creator=profile).values_list(
                "pk", flat=True
            )
            favorited_pk = Project.objects.filter(
                favorited_by__profile=profile
            ).values_list("pk", flat=True)
            reviewed_pk = Project.objects.filter(
                reviews__reviewer=profile
            ).values_list("pk", flat=True)

            featured_pk = set(created_pk) | set(favorited_pk) | set(reviewed_pk)

            created = Project.objects.filter(creator=profile)
            favorited = Project.objects.filter(favorited_by__profile=profile)
            reviewed = Project.objects.filter(reviews__reviewer=profile).distinct()

            context["created_projects"] = created
            context["favorited_projects"] = favorited
            context["reviewed_projects"] = reviewed

            context["projects"] = Project.objects.exclude(pk__in=featured_pk)
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "diyprojects/project_detail.html"
    context_object_name = "project"

    def get_avg_ratings(self):
        project = self.object
        score = ProjectRating.objects.filter(project=project)
        average = score.aggregate(avg_score=Avg("score"))
        return average["avg_score"]

    def get_favorite_count(self):
        project = self.object
        favoriteCount = Favorite.objects.filter(project=project)
        count = favoriteCount.count()
        return count

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        profile = None
        if user.is_authenticated:
            profile = user.profile

        context["rating_form"] = ProjectRatingForm()
        context["review_form"] = ProjectReviewForm()
        context["average_scores"] = self.get_avg_ratings()
        context["favorite_count"] = self.get_favorite_count()
        context["is_creator"] = user.is_authenticated and profile == self.object.creator
        context["project_reviews"] = self.object.reviews.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_type = request.POST.get("form_type")

        if form_type in ["rating", "review", "favorite"]:
            if not request.user.is_authenticated:
                return redirect("accounts:permission-denied")

        if form_type == "rating":
            form = ProjectRatingForm(request.POST)

            if form.is_valid():
                rating = form.save(commit=False)
                rating.profile = request.user.profile
                rating.project = self.object
                rating.save()
                return redirect("diyprojects:project-detail", pk=self.object.pk)

        elif form_type == "review":
            form = ProjectReviewForm(request.POST, request.FILES)

            if form.is_valid():
                review = form.save(commit=False)
                review.reviewer = request.user.profile
                review.project = self.object
                review.save()
                return redirect("diyprojects:project-detail", pk=self.object.pk)

        elif form_type == "favorite":
            profile = request.user.profile
            project = self.object
            favorite = Favorite.objects.filter(project=project, profile=profile).first()
            if favorite:
                favorite.delete()
            else:
                Favorite.objects.create(
                    project=project, profile=profile, date_favorited=date.today()
                )
            return redirect("diyprojects:project-detail", pk=self.object.pk)
        return self.get(request, *args, **kwargs)


class ProjectCreateView(RoleRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "diyprojects/project_form.html"
    required_role = "Project Creator"

    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user.profile
            project.save()
            return redirect("diyprojects:project-list")

        return self.get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.creator = self.request.user.profile
        return super().form_valid(form)


class ProjectUpdateView(RoleRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "diyprojects/project_form.html"
    required_role = "Project Creator"

    def form_valid(self, form):
        form.instance.creator = self.request.user.profile
        return super().form_valid(form)
