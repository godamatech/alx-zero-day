from . import models
from blog.models import Blog
from blog.forms import BlogForm
from django.contrib import messages
from django.shortcuts import render, redirect
from student.models import Record, Notification
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda user: user.groups.filter(name='staff').exists())
def index_view(request):
    user = request.user
    records = Record.objects.all()
    students = models.User.objects.filter(groups__name="student", level=user.level)

    for student in students:
        student.records = student.record_set.filter(score__isnull=True)

    context = {"records": records, "students": students}
    return render(request, "staff/index.html", context)

@login_required
@user_passes_test(lambda user: user.groups.filter(name='staff').exists())
def post_view(request):
    posts = Blog.objects.filter(lecturer=request.user)
    print(posts)

    if request.method == 'POST':
        form = BlogForm(request.POST)

        if form.is_valid() and form.save():
            messages.success(request, "Post saved successfully")
        else:
            print(form.errors)
            messages.warning(request, "Something went wrong")
        return redirect('staff:post-view')

    context = {"posts":posts}
    return render(request, "staff/post.html", context)


@login_required
@user_passes_test(lambda user: user.groups.filter(name='staff').exists())
def detail_view(request, id):
    record = Record.objects.get(id=id)

    if request.method == "POST":
        score = request.POST.get("score")
        remark = request.POST.get("remark")

        record.score = float(score) if score else None
        record.remark = remark
        record.save()

        Notification.objects.create(
            user=record.user,
            description=f"Lecturer {request.user.username} have assess your record: '{record.title}' and gave a remark and score",
        )
        return redirect("staff:detail", id=id)

    context = {"record": record}
    return render(request, "staff/detail.html", context)


@login_required
@user_passes_test(lambda user: user.groups.filter(name='staff').exists())
def student_view(request, id):
    student = models.User.objects.get(id=id)
    records = Record.objects.filter(user=student)

    context = {"student": student, "records": records}
    return render(request, "staff/student.html", context)
