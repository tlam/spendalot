from django.contrib import messages
from django.shortcuts import render

from .forms import UploadFileForm


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.handle_uploaded_file(request.FILES['file'])
            messages.success(request, 'Successfully loaded')
    else:
        form = UploadFileForm()
    context = {
        'form': form,
    }
    return render(request, 'statements/index.html', context)
