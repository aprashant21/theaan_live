from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="index"),
    path('floorsheet',views.floorsheet,name="floorsheet"),
    path('blogs',views.blogs, name="blogs"),
    path('notes',views.handleShowNotes, name="notes"),
    path('about',views.about, name="about"),

    #for backend or server side
    path('dashboard',views.dashboard, name="dashboard"),
    path('forms',views.forms, name="forms"),

    #for api data
    path('apiTableAdmin',views.apiTableAdmin, name="apiTableAdmin"),
    path("deleteApi/<int:id>",views.handleApiDelete,name='deleteApi'),
    path("updateApi/<int:id>",views.update_api,name='updateApi'),

    #for note data
    path('noteTableAdmin',views.noteTableAdmin, name="noteTableAdmin"),
    path("deleteNote/<int:id>",views.handleNoteDelete,name='deleteNote'),
    path("updateNote/<int:id>",views.update_note,name='updateNote'),


    #login,logout and signup
    path("signup",views.handleSignup,name='handleSignup'),
    path("login",views.handleLogin,name='handleLogin'),
    path("logout",views.handleLogout,name='handleLogout'),

    #for blog data
    path('blogTableAdmin',views.blogTableAdmin, name="blogTableAdmin"),
    path("deleteBlog/<int:id>",views.handleBlogDelete,name='deleteBlog'),
    path("updateBlog/<int:id>",views.update_blog,name='updateBlog'),
    path("Blogs/<int:id>",views.show_blogs,name='showBlog'),

    #for search
    path('searchNote',views.search_Note, name="searchNote"),
    path('searchBlog',views.search_Blog, name="searchBlog"),





]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)