# Copyright © 2024 Syed Saad Ali
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from home.models import Project,Bug,Profile
from datetime import datetime
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.hashers import check_password
# Create your views here.

def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'base.html')

@login_required
def base(request):
    return render(request,'base.html')

def loginuser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            if user.is_superuser:
                return render(request,'admin.html')
            elif user.is_staff:
                return render(request,'staff.html')
            else:
                return redirect("/home")
        else:
            return render(request,'login.html')
    return render(request,'login.html')

def logoutuser(request):
    logout(request)
    return redirect("/login")

def register(request):
    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        passw = request.POST['pass']
        email = request.POST['email']
        designation = request.POST['designation']
        if User.objects.filter(username=username).exists():
            return render(request,'register_error.html')
        else:
            newuser = User.objects.create_user(username,email,passw)
            newuser.last_name = lname
            newuser.first_name = fname
            newuser.username = username
            newuser.set_password(passw)
            newuser.email = email
            profile = Profile(user=newuser,Designation = designation)
            profile.save()
            newuser.save()
            if request.user.is_superuser:
                return redirect('/staffdisplayusers')
            return render(request,'login.html')
    return render(request,'register.html')

@login_required
def staff(request):
    if request.user.is_staff:
        return render(request,'staff.html')
    else:
        return redirect("/home")

@login_required
def project(request):
    my_data = Project.objects.all()
    return render(request,'project.html',{'my_data':my_data})

@login_required
def createproject(request):
    available_users = User.objects.all()
    context = {
        'available_users':available_users,
    }
    return render(request,'addproject.html',context)

@login_required
def addproject(request):
    if request.method == 'POST':
        Pname = request.POST.get('Pname')
        Pstatus = request.POST.get('Pstatus')
        Desc = request.POST.get('Desc')
        project = Project(Pname = Pname, Pstatus = Pstatus, Desc = Desc, date = datetime.today())
        user_ids = request.POST.getlist('users')
        project.save()
        project.users.add(*user_ids)
        project.save()
        my_data = Project.objects.all()
        return render(request,'project.html',{'my_data':my_data})
    return render(request,'project.html')

@login_required
def editproject(request, id):
    project = Project.objects.get(id=id)
    return render(request,'editproject.html',{'project':project})

@login_required
def projectusers(request, id):
    project = Project.objects.get(id=id)
    users = project.users.all()
    context = {
        'users':users,
        'project':project,
    }
    return render(request,'projectusers.html',context)

@login_required
def updateproject(request, id):
    if request.method =='POST':
        project = Project.objects.get(id=id)
        old_name = project.Pname
        project.Pname = request.POST.get('Pname')
        Bug.objects.filter(project=old_name).update(project=project.Pname)
        project.Pstatus = request.POST.get('Pstatus')
        project.Desc = request.POST.get('Desc')
        project.date = datetime.now()
        project.save()
        my_data = Project.objects.all()
        return render(request,'project.html',{'my_data':my_data})
    else:
        return render(request,'project.html')

@login_required
def Userproject(request):
    my_data = Project.objects.all()
    return render(request,'Userproject.html',{'my_data':my_data})

@login_required
def userprojects(request,id):
    user = User.objects.get(id=id)
    projects = Project.objects.filter(users=user)
    context = {
        'user':user,
        'projects':projects,
    }
    return render(request,'userprojects.html',context)


@login_required
def displayusers(request):
    my_data = User.objects.all()
    return render(request,'displayusers.html',{'my_data':my_data})

@login_required
def staffdisplayusers(request):
    my_data = User.objects.all()
    if request.user.is_superuser:
        return render(request,'admindisplayusers.html',{'my_data':my_data})
    return render(request,'staffdisplayusers.html',{'my_data':my_data})

def adduser(request):
    return render(request,'adduser.html')

def deleteuser(request,username):
    user = User.objects.get(username=username)
    user.delete()
    return redirect('/staffdisplayusers')

@login_required
def edituser(request,username):
    user = User.objects.get(username=username)
    if user.is_superuser:
        return render(request,'superusererror.html')
    else:
        if request.method=="POST":
            user = User.objects.get(username=username)
            fname = request.POST['fname']
            lname = request.POST['lname']
            user.first_name = fname
            user.last_name = lname
            status = request.POST['userstatus']
            designation = request.POST['designation']
            try:
                profile = Profile.objects.get(user=user)
                profile.Designation = designation
                profile.save()
            except Profile.DoesNotExist:
                profile = Profile(user=user, Designation=designation)
                profile.save()
            if status == "Staff Member":
                user.is_staff = True
                user.save()
            else:
                user.is_staff = False
                user.save()
            return redirect('/staffdisplayusers')
    return render(request,'edituser.html',{'user':user})

@login_required
def deleteproject(request,id):
    pr = Project.objects.get(id=id)
    Bug.objects.filter(project=pr.Pname).delete()
    pr.delete()
    my_data = Project.objects.all()
    return render(request,'project.html',{'my_data':my_data})

@login_required
def addbug(request):
    if request.method == "POST":
        project = request.POST.get('project')
        Severity = request.POST.get('Severity')
        Priority = request.POST.get('Priority')
        Assign = request.POST.get('Assign')
        Summary = request.POST.get('Summary')
        Desc = request.POST.get('Desc')
        Image = request.FILES.get('Image')
        status = request.POST.get('status')
        current_user = request.user.username
        bug = Bug(project=project,Severity=Severity,Priority=Priority,Assign=Assign,Summary=Summary,Desc=Desc,date=datetime.today(),created=timezone.now(),Image=Image,status=status,reportedby=current_user,resolvedby="None")
        bug.save()
        my_data = Bug.objects.all().order_by('created')
        reversed_data = my_data.reverse()  # Reverse the order
        if request.user.is_staff:
            return render(request, 'bugs.html', {'reversed_data': reversed_data})
        else:
            return redirect('/clientbugs')
    else:
        project = Project.objects.all()
        users = User.objects.filter(is_staff=True)
        context = {
            'project': project,
            'users': users,
        }
        return render(request,'addbug.html',context)

@login_required
def bugs(request):
    my_data = Bug.objects.all().order_by('created')
    reversed_data = my_data.reverse()  # Reverse the order
    return render(request, 'bugs.html', {'reversed_data': reversed_data})

@login_required
def editbug(request,id):
    bug = Bug.objects.get(id=id)
    if bug.status == 'Resolved':
        return render(request, 'error_page.html', {'message': 'Bug is already resolved and cannot be edited.'})
    if request.method == "POST":
        bug = Bug.objects.get(id=id)
        if bug.status == 'Resolved':
            return render(request, 'error_page.html', {'message': 'Bug is already resolved and cannot be edited.'})
        bug.project = request.POST.get('project')
        bug.Severity = request.POST.get('Severity')
        bug.Priority = request.POST.get('Priority')
        bug.Assign = request.POST.get('Assign')
        bug.Summary = request.POST.get('Summary')
        bug.Desc = request.POST.get('Desc')
        bug.Image = request.FILES.get('Image')
        bug.status = request.POST.get('status')
        if bug.status=="Resolved":
            current_user = request.user.username
            bug.resolvedby = current_user
            bug.ended = timezone.now()
            time = bug.ended-bug.created
            bug.timetaken = str(time.days)+" days "+str(time.seconds//3600)+" hr"
        bug.save()
        my_data = Bug.objects.all().order_by('created')
        reversed_data = my_data.reverse()  # Reverse the order
        if request.user.is_superuser:
            return render(request, 'bugs.html', {'reversed_data': reversed_data})
        elif request.user.is_staff:
            return render(request, 'bugs.html', {'reversed_data': reversed_data})
        else:
            my_data = Bug.objects.all().filter(reportedby=request.user).order_by('created')
            reversed_data = my_data.reverse()  # Reverse the order
            return render(request, 'clientbugs.html', {'reversed_data': reversed_data})
    else:
        bug = Bug.objects.get(id=id)
        project = Project.objects.all()
        users = User.objects.all()
        context = {
            'bug':bug,
            'project':project,
            'users' :users,
        }
        return render(request,'editbug.html',context)

@login_required
def deletebug(request,id):
    bug = Bug.objects.get(id=id)
    bug.delete()
    my_data = Bug.objects.all().order_by('created')
    reversed_data = my_data.reverse()  # Reverse the order
    return render(request, 'bugs.html', {'reversed_data': reversed_data})

@login_required
def displaytasks(request,username):
    user = User.objects.get(username = username)
    full_name = user.first_name+" "+user.last_name+" - "+user.profile.Designation
    bugs = Bug.objects.filter(Assign = full_name)
    return render(request,'task.html',{'bugs':bugs})

@login_required
def displayclientbugs(request):
    my_data = Bug.objects.all().filter(reportedby=request.user).order_by('created')
    reversed_data = my_data.reverse()  # Reverse the order
    return render(request, 'clientbugs.html', {'reversed_data': reversed_data})

@login_required
def back(request):
    if request.user.is_superuser:
        return render(request,'admin.html')
    elif request.user.is_staff:
        return redirect('/staff')
    else:
        return redirect('/home')
    
@login_required
def viewproject(request,id):
    project = Project.objects.get(id=id)
    unresolved = Bug.objects.filter(project=project.Pname,status='Unresolved')
    resolved = Bug.objects.filter(project=project.Pname,status='Resolved')
    context = {
        'project':project,
        'unresolved':unresolved,
        'resolved':resolved,
    }
    return render(request,'viewproject.html',context)

def project_bug_graph(request):
    bug_counts = Bug.objects.values('project__Pname').annotate(total=Count('project')).order_by('project__Pname')
    project_names = [bug['project__Pname'] for bug in bug_counts]
    bug_totals = [bug['total'] for bug in bug_counts]
    context = {'project_names': project_names, 'bug_totals': bug_totals}
    return render(request, 'project_bug_graph.html', context)

@login_required
def reportdate(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        my_data = Bug.objects.filter(created__date__range=[start_date,end_date])
        return render(request,'Reportbugs.html',{'my_data':my_data})
        
    users = User.objects.all()
    return render(request,'reportdate.html',{'users':users})

#        name = request.POST.get("resolvedby")
#        if name=="All":
#            my_data = Bug.objects.filter(created__date__range=[start_date,end_date])
#            return render(request,'Reportbugs.html',{'my_data':my_data})
#        first_name,last_name = name.split()
#        user = User.objects.get(first_name=first_name, last_name=last_name)
#        username = user.username
#        my_data = Bug.objects.filter(created__date__range=[start_date,end_date],resolvedby=username)

@login_required
def editaccount(request):
    if request.method=="POST":
        user = request.user
        oldpassw = request.POST['oldpass']
        newpassw = request.POST['newpass']
        if check_password(oldpassw,user.password):
            user.set_password(newpassw)
            user.save()
            return redirect('/back')
        return render(request,'incorrectpass.html')
    return render(request,'editaccount.html')

@login_required
def reportusers(request):
    queryset1 = Bug.objects.values('reportedby').annotate(count=Count('*'))
    queryset2 = Bug.objects.values('resolvedby').annotate(count=Count('*'))
    reported_counts = {}
    resolved_counts = {}
    # Update counts based on queryset1
    for item in queryset1:
        reported_counts[item['reportedby']] = item['count']
    # Update counts based on queryset2
    for item in queryset2:
        resolvedby = item['resolvedby']
        resolved_counts[resolvedby] = item['count'] if resolvedby is not None else 0
    # Combine the counts for each username
    merged_data = []
    for username in set(reported_counts.keys()) | set(resolved_counts.keys()):
        merged_data.append({
            'username': username,
            'reported_count': reported_counts.get(username, 0),
            'resolved_count': resolved_counts.get(username, 0)
        })
    # Sort by username (optional)
    merged_data.sort(key=lambda x: x['username']) 
    for item in merged_data:
        try:
            user = User.objects.get(username=item['username'])
            full_name = f"{user.first_name} {user.last_name}" if user else "Unresolved Bug"
            item['full_name'] = full_name
        except User.DoesNotExist:
            item['full_name'] = "Unresolved Bug"   
    target_username = "Unresolved Bug"
    filtered_data = [item for item in merged_data if item['full_name'] != target_username]
    total_reported = sum(item['reported_count'] for item in filtered_data)
    total_resolved = sum(item['resolved_count'] for item in filtered_data)

    # Add an entry for "Total"
    filtered_data.append({
        'full_name': 'Total',
        'reported_count': total_reported,
        'resolved_count': total_resolved
    })
    filtered_data.append({
        'full_name': 'Bugs Unresolved',
        'reported_count': total_reported-total_resolved,
        'resolved_count': " "
    })
    return render(request,'Reportusers.html',{'filtered_data':filtered_data})

