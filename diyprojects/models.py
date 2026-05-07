from django.db import models
from django.urls import reverse
from accounts.models import Profile
from django.core.validators import MinValueValidator, MaxValueValidator


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects"
    )
    creator = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_projects"
    )
    description = models.TextField()
    materials = models.TextField()
    steps = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("diyprojects:project-detail", args=[str(self.id)])


class Favorite(models.Model):
    STATUS_BACKLOG = "backlog"
    STATUS_TODO = "todo"
    STATUS_DONE = "done"

    STATUS_CHOICES = [
        (STATUS_BACKLOG, "Backlog"),
        (STATUS_TODO, "To-Do"),
        (STATUS_DONE, "Done"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="favorited_by",
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        related_name="favorited_projects",
    )
    date_favorited = models.DateField()
    project_status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default=STATUS_BACKLOG
    )


class ProjectReview(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="reviews",
    )
    reviewer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        related_name="project_reviews",
    )
    comment = models.TextField()
    image = models.ImageField(upload_to="images/", null=False, blank=False)


class ProjectRating(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        related_name="rated",
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        related_name="ratings",
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
