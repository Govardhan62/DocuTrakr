from django.urls import path,include
from django.conf.urls import handler404
from .views import process_document,view_document,download_as_docx,download_as_pdf,delete_document,home
from .loginviews import login,logout,signup
from .pdfdoxconviews import convert_to_pdf,convert_to_doc

urlpatterns = [
    path('process_document',process_document,name='process_document'),
    path('view_document/<int:document_id>/',view_document, name='view_document'),
    path('download_as_pdf/<int:document_id>/', download_as_pdf, name='download_as_pdf'),
    path('download_as_docx/<int:document_id>/', download_as_docx, name='download_as_docx'),
    path('delete_document/<int:document_id>/',delete_document,name='delete_document'),
    path('',home,name='home'),
    path('signup',signup,name='signup'),
    path('logout',logout,name='logout'),
    path('login',login,name='login'),
    path('convert_to_pdf',convert_to_pdf,name='convert_to_pdf'),
    path('convert_to_doc',convert_to_doc,name='convert_to_doc'),
    path("__reload__/", include("django_browser_reload.urls")),
]
