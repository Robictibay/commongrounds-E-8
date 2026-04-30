from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import ProfileUpdateForm, RegisterForm
from .models import Profile

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save() # Saves User, triggering signal to create Profile
            
            # Now fetch that auto-created Profile and update it
            profile = user.profile
            profile.display_name = form.cleaned_data['display_name']
            profile.email_address = form.cleaned_data['email']
            profile.save()

            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_form.html'

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('home')


def permission_denied_view(request):
    return render(request, 'accounts/permission_denied.html')