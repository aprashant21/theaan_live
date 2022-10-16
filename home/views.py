from django.shortcuts import render,HttpResponseRedirect,redirect
from home import floorsheet
from .models import API, BLOG, NOTE
from .form import APIForm, BLOGForm, NOTEForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json

# Create your views here.
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')

resultJson = floorsheet.FloorSheetClass.floorsheet() #This is flootsheet json

@api_view(['GET'])
def floorsheet(request):
    return Response(json.loads(resultJson))

def blogs(request):
    blog= (BLOG.objects.all()).exclude(blogId=2)
    first_blog = BLOG.objects.filter(blogId=2)
    context={
        'blogs':blog,
        'blogs1':first_blog
    }
    return render(request, 'blogs.html',context)

def dashboard(request):
    # authorization of pages
    if not request.user.is_authenticated:
        messages.error(request, "kindly login first")
        return redirect  ('/')
    if not request.user.is_superuser:
        messages.error(request, "The page you want to access is restricted !")
        return redirect('/') #authorization ends here

    users = User.objects.all()
    blogs= BLOG.objects.all()
    notes = NOTE.objects.all()
    notes_length = len(notes)
    blogs_length=len(blogs)
    users_length= len(users)
    context={
        'total_notes':notes_length,
        'total_blogs': blogs_length,
        'total_users': users_length
    }
    return render(request, 'dashboard.html', context)

#forms : handles api form , blog form and note form 
def forms(request):
    # authorization of pages
    if not request.user.is_authenticated:
        messages.error(request, "kindly login first")
        return redirect  ('/')
    if not request.user.is_superuser:
        messages.error(request, "The page you want to access is restricted !")
        return redirect('/') #authorization ends here

    if request.method == "POST" :
        if 'apiSubmit' in request.POST :
            fm = APIForm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Your form has been saved !')
                fm = APIForm()
                return HttpResponseRedirect('forms')

        elif 'blogSubmit' in request.POST :
            fm1=BLOGForm(request.POST, request.FILES)
            if fm1.is_valid():
                fm1.save()
                messages.success(request, 'Your form has been saved !')               
                fm1=BLOGForm()
                return HttpResponseRedirect('forms')

        elif 'noteSubmit' in request.POST :
            fm2=NOTEForm(request.POST)
            if fm2.is_valid():
                fm2.save()
                messages.success(request, 'Your form has been saved !')               
                fm2=NOTEForm()
                return HttpResponseRedirect('forms')
    else:
        fm = APIForm()
        fm1= BLOGForm() 
        fm2= NOTEForm()

    context={
        'form':fm,
        'form1':fm1,
        'form2':fm2
    }
    
    return render(request,'forms.html',context)

def handleShowNotes(request):
    notes = NOTE.objects.all()
    context={
        'note':notes
    }
    return render(request,'notes.html',context)

def handleApiDelete(request,id):
    api = API.objects.filter(pk=id)
    api.delete()
    messages.success(request, 'Your api has been deleted !')
    return HttpResponseRedirect('/apiTableAdmin')

def handleNoteDelete(request,id):
    note = NOTE.objects.filter(pk=id)
    note.delete()
    messages.success(request, 'Your note has been deleted !')
    return HttpResponseRedirect('/noteTableAdmin')

def apiTableAdmin(request):
    # authorization of pages
    if not request.user.is_authenticated:
        messages.error(request, "kindly login first")
        return redirect  ('/')
    if not request.user.is_superuser:
        messages.error(request, "The page you want to access is restricted !")
        return redirect('/') #authorization ends here

    api = API.objects.all()
    context={
        'api':api
    }
    return render(request, 'apiTableAdmin.html',context)

def noteTableAdmin(request):
    # authorization of pages
    if not request.user.is_authenticated:
        messages.error(request, "kindly login first")
        return redirect  ('/')
    if not request.user.is_superuser:
        messages.error(request, "The page you want to access is restricted !")
        return redirect('/') #authorization ends here

    note = NOTE.objects.all()
    context={
        'notes':note
    }
    return render(request, 'noteTableAdmin.html',context)

#for signup
def handleSignup(request):
    if request.method == "POST":
        # get the entire signup parameters
        fname = request.POST['fname']
        lname = request.POST['lname']
        singupemail = request.POST['singupemail']
        signupUsername = request.POST['signupUsername']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # checking the parameters
        if User.objects.filter(username =signupUsername).first(): #check for username already taken or not
            messages.error(request, "This username is already taken")
            return HttpResponseRedirect('/')
        if pass1!=pass2: # check for password is same or not
            messages.error(request, "Password must be same")
            return HttpResponseRedirect('/')
        if len(signupUsername)>12: #check for username is upto 12 character or not
            messages.error(request,"username must be upto 12 characters")
            return HttpResponseRedirect('/')
        if User.objects.filter(email =singupemail).first(): #check for username already taken or not
            messages.error(request, "This email is already taken")
            return HttpResponseRedirect('/')
           

        # creating the users
        myuser =User.objects.create_user(signupUsername,singupemail,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()

        messages.success(request, "Your account has been successfully created. Welcome to theaan's world.")    

        return redirect('/')
    
    else:
        return HttpResponse("OOPSS ! --- 404 NOT FOUND ")

def handleLogin(request):
    if request.method == "POST":
     # get the entire signup parameters
        loginUsername = request.POST['loginUsername']
        loginpass = request.POST['loginPassword']
        
        user = authenticate(username = loginUsername,password=loginpass)

        if user is not None:
            login(request,user)
            messages.success(request,"Successfully logged-in")
            if request.user.is_superuser:
                return redirect('/dashboard')
            else:
                return redirect('/')
        else:
            messages.error(request,"Sorry ! Invalid crediantial !")
            return redirect('/')

    return HttpResponse("OOPS!!!! 404 not found")

def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect('/')

#for showing blog table content
def blogTableAdmin(request):
    # authorization of pages
    if not request.user.is_authenticated:
        messages.error(request, "kindly login first")
        return redirect  ('/')
    if not request.user.is_superuser:
        messages.error(request, "The page you want to access is restricted !")
        return redirect('/') #authorization ends here
        
    blog = BLOG.objects.all()
    context={
        'blogs':blog
    }
    return render(request, 'blogTableAdmin.html',context)

#it handles blog delete
def handleBlogDelete(request,id):
    blog = BLOG.objects.filter(pk=id)
    blog.delete()
    messages.success(request, 'Your blog has been deleted !')
    return HttpResponseRedirect('/blogTableAdmin')

# This is the method for update the api table
def update_api(request,id):
    if request.method == "POST":
        pi = API.objects.get(pk=id)
        fm=APIForm(request.POST,instance=pi)
        if fm.is_valid:
            fm.save()
            messages.success(request, 'Your api has been updated !')
            fm = APIForm()
    else:
        pi = API.objects.get(pk=id)
        fm=APIForm(instance=pi)

    return render(request,'updateApi.html',{'form':fm})

# This is the method for update the note table
def update_note(request,id):
    if request.method == "POST":
        pi = NOTE.objects.get(pk=id)
        fm=NOTEForm(request.POST,instance=pi)
        if fm.is_valid:
            fm.save()
            messages.success(request, 'Your note has been updated !')
            fm = NOTEForm()
    else:
        pi = NOTE.objects.get(pk=id)
        fm=NOTEForm(instance=pi)

    return render(request,'updateNotes.html',{'form':fm})

# This is the method for update the blog table
def update_blog(request,id):
    if request.method == "POST":
        pi = BLOG.objects.get(pk=id)
        fm=BLOGForm(request.POST,instance=pi)
        if fm.is_valid:
            fm.save()
            messages.success(request, 'Your blog has been updated !')
            fm = BLOGForm()
    else:
        pi = BLOG.objects.get(pk=id)
        fm=BLOGForm(instance=pi)

    return render(request,'updateBlogs.html',{'form':fm})

# This is the method for update the blog table
def update_blog(request,id):
    if request.method == "POST":
        pi = BLOG.objects.get(pk=id)
        fm=BLOGForm(request.POST,instance=pi)
        if fm.is_valid:
            fm.save()
            messages.success(request, 'Your blog has been updated !')
            fm = BLOGForm()
    else:
        pi = BLOG.objects.get(pk=id)
        fm=BLOGForm(instance=pi)

    return render(request,'updateBlogs.html',{'form':fm})

# This is the method for update the blog table
def show_blogs(request,id):
    pi = BLOG.objects.get(pk=id)
    context={
        'blogs':pi,
 }
    return render(request,'showBlogs.html',context)

#This function helps to search notes from note page
def search_Note(request):
    query = request.GET['queryNote']
    if len(query) > 25:
        messages.error(request,"You have only 25 character to search")
        return redirect('/')
    
    searchNote = NOTE.objects.filter(noteTitle__icontains = query)
    lengthSearchNote = len(searchNote)
    context = {
        'note':searchNote,
        'query':query,
        'lenSearch':lengthSearchNote
    }
    return render(request,'searchNotes.html',context)


#This function helps to search blogs from blog page
def search_Blog(request):
    query = request.GET['queryBlog']
    if len(query) > 25:
        messages.error(request,"You have only 25 character to search")
        return redirect('/')
    
    searchBlog = BLOG.objects.filter(blogTitle__icontains = query)
    lengthSearchBlog = len(searchBlog)
    context = {
        'blogs':searchBlog,
        'queryBlog':query,
        'lenSearch':lengthSearchBlog
    }
    return render(request,'searchBlog.html',context)