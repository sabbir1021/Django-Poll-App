from django.shortcuts import redirect
from django.contrib import messages

class AictiveUserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(
                request, ('Please Login Fast'))
            return redirect('authenticate:login')


