from django.shortcuts import render

# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ReviewForm
from .models import Review

def rate_object_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            object_id = form.cleaned_data.get('object_id')
            review = form.cleaned_data.get('review')
            content_type_id = form.cleaned_data.get('content_type_id')
            c_type = ContentType.objects.get_for_id(content_type_id)
            obj = Review.objects.create(
                content_type=c_type,
                object_id=object_id,
                value=review,
                user=request.user
            )
            next_path = form.cleaned_data.get('next') # detail view
            return HttpResponseRedirect(next_path)
    return HttpResponseRedirect('/')