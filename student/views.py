from . import models, forms
from blog.models import Blog
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test



@login_required
@user_passes_test(lambda user: user.groups.filter(name='student').exists())
def index_view(request):
    total = models.Record.objects.filter(user=request.user)
    posts = Blog.objects.filter(level=request.user.level)[:10]

    others = total.exclude(created_at__date=now().date())
    current = total.filter(user=request.user, created_at__date=now().date())

    notifications = models.Notification.objects.filter(user=request.user)

    context = {
        "total": total,
        "posts": posts,
        "others": others,
        "current": current,
        "notifications": notifications,
    }
    return render(request, "student/index.html", context)


@login_required
@user_passes_test(lambda user: user.groups.filter(name='student').exists())
def create_view(request):
    if request.method == "POST":
        form = forms.RecordForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            form.save()  # Don't save the form yet

            messages.success(request, "Log Added Successfully!")
            return redirect("student:index-view")

        messages.error(request, "Failed to save record")
        return redirect("student:create-view")
    else:
        form = forms.RecordForm()  # If the request method is not POST, create a new form instance
    return render(request, "student/create.html", {"form": form})


@login_required
@user_passes_test(lambda user: user.groups.filter(name='student').exists())
def download_file(request, record_id):
    record = models.Record.objects.get(id=record_id)
    if record.file_upload:
        # Assuming file_upload is a FileField
        response = HttpResponse(record.file_upload, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{record.file_upload.name}"'
        return response
    else:
        return HttpResponse("File not found", status=404)

@login_required
@user_passes_test(lambda user: user.groups.filter(name='student').exists())
def create_viewOld(request):
    if request.method == "POST":
        form = forms.RecordForm(request.POST)
        if form.is_valid():
            instance = form.save(False)

            instance.user = request.user
            instance.save()
            
            return redirect("student:index-view")

        messages.error(request, "Failed to save record")
        return redirect("student:create-view")
    return render(request, "student/create.html")
