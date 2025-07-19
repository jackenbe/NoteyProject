from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .form import RegistrationForm, GroupForm, JoinUniversityForm, GroupNoteCreationForm, PersonalNoteCreationForm
from django.contrib.auth import login
from .models import Profile, Group, Note
import uuid
from django.contrib import messages

@login_required(login_url='/login')
def home(request):
    context = {}
    if request.method =="POST":
        invite_code = request.POST.get('invite_code', ' ').strip()

        try:
            obj_code = uuid.UUID(invite_code)
        except ValueError:
            messages.error(request, "Invalid invite code.")
            return redirect('/groups')

        try:
            group = Group.objects.get(invite_code=obj_code)
            profile = Profile.objects.get(user=request.user)

            if group in profile.groups.all() or (group.university not in profile.universities.all()):
                context['error'] = "You're already in this group"
            else:
                profile.groups.add(group)
                context['success'] = 'Successfully Joined Group'
                return redirect('/groups')
        except Group.DoesNotExist:
            context['error'] = 'Group does not exist'
            return redirect("/groups")

    return render(request, 'main/home.html', context)

@login_required(login_url='/login')
def group_create(request):
    if request.method == "POST":
        form = GroupForm(request.POST, user=request.user)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            group.members.clear()
            profile = Profile.objects.get(user=request.user)
            group.members.add(request.user)
            profile.groups.add(group)
            return redirect("/home")
    else:
        form = GroupForm(user=request.user)

    return render(request, "main/group_create.html", {"form": form})

@login_required(login_url='/login')
def group_list(request):
    try:
        profile = Profile.objects.get(user=request.user)
        groups = profile.groups.all()
    except Profile.DoesNotExist:
        raise Http404("Profile does not exist")
    context ={
        "groups": groups,
        "user": request.user
    }
    if request.method == "POST":
        group_id = request.POST.get('group-id')
        group = Group.objects.get(id=group_id)
        if group and request.user == group.created_by:
            group.delete()
        return redirect('/home')
    return render(request, 'main/groups.html', context)

@login_required(login_url='/login')
def view_universities(request):
    profile = Profile.objects.get(user=request.user)
    universities = profile.universities.all()
    context = {
        "universities": universities
    }

    if request.method == "POST":
        form = JoinUniversityForm(request.POST, user=request.user)
        if form.is_valid():
            context['form'] = form
            university = form.cleaned_data['university']
            profile.universities.add(university)
            return redirect('/universities')
    else:
        form = JoinUniversityForm(user=request.user)
        context['form'] = form
    return render(request, 'main/universities.html', context)

@login_required(login_url='/login')
def group_view(request, id):
    try:
        obj = Group.objects.get(id=id)
    except Group.DoesNotExist:
        raise Http404

    notes = Note.objects.filter(group=obj).order_by('-created_time')

    context = {
        "group": obj,
        "notes": notes
    }

    return render(request, "main/group_view.html", context)

@login_required(login_url='/login')
def note_view(request, id):
    try:
        note = Note.objects.get(id=id)
    except Note.DoesNotExist:
        raise Http404("Note does not exist")

    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        raise Http404("Profile does not exist")

    if note.is_personal and request.user != note.author:
        return redirect('/home')

    if note.group and note.group not in profile.groups.all():
        return redirect('/home')

    if request.method == "POST":
        note_id = request.POST.get('note-id')
        note = Note.objects.get(id=note_id)
        if note and request.user == note.author:
            note.delete()
        return redirect('/home')

    context = {
        'note': note,
        'user': request.user
    }
    return render(request, "main/note_detail.html", context)

@login_required(login_url='/login')
def note_create(request, id):
    try:
        group = Group.objects.get(id=id)
    except Group.DoesNotExist:
        raise Http404("Group Does Not Exist")

    profile = Profile.objects.get(user=request.user)

    if group not in profile.groups.all():
        return HttpResponseForbidden("You are not a member of this group.")

    context = {}
    if request.method == "POST":
        form = GroupNoteCreationForm(request.POST, id=id, user=request.user)
        if form.is_valid():
            context['form'] = form
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return redirect(f'/group/{id}')
    else:
        form = GroupNoteCreationForm(id=id, user=request.user)
        context['form'] = form

    return render(request, 'main/note_create.html', context)

@login_required(login_url='/login')
def personal_view(request):
    notes = Note.objects.filter(author=request.user, is_personal=True).order_by('-created_time')
    context = {
        "notes": notes
    }

    return render(request, "main/personal_view.html", context)

@login_required(login_url='/login')
def personal_note_create(request):
    context = {}
    if request.method == "POST":
        form = PersonalNoteCreationForm(request.POST)
        if form.is_valid():
            context['form'] = form
            note = form.save(commit=False)
            note.author = request.user
            note.is_personal = True
            note.save()
            return redirect(f'/personal')
    else:
        form = PersonalNoteCreationForm()
        context['form'] = form

    return render(request, 'main/personal_note_create.html', context)

def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            profile = Profile.objects.create(user=user)
            profile.universities.add(form.cleaned_data['university'])
            return redirect('/home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {'form': form})
