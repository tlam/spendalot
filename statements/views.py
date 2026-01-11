from django.contrib import messages
from django.shortcuts import render

from .forms import UploadFileForm
from data_sources.dropbox_client import DropboxClient


def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if request.POST.get("dropbox-data"):
            client = DropboxClient()
            client.load_expenses()
            messages.success(request, "Dropbox file downloaded")
        else:
            if form.is_valid():
                form.handle_uploaded_file(request.FILES["file"])
                messages.success(request, "Successfully loaded")
    else:
        form = UploadFileForm()
    context = {
        "form": form,
    }
    return render(request, "statements/index.html", context)
