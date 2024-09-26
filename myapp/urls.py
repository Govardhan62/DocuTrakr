from django.urls import path,include
from django.conf.urls import handler404
from .views import process_document,view_document,download_as_docx,download_as_pdf,delete_document

handler404 = 'myapp.views.demo' 

urlpatterns = [
    path('',process_document,name='process_document'),
    path('view_document/<int:document_id>/',view_document, name='view_document'),
    path('download_as_pdf/<int:document_id>/', download_as_pdf, name='download_as_pdf'),
    path('download_as_docx/<int:document_id>/', download_as_docx, name='download_as_docx'),
    path('delete_document/<int:document_id>/',delete_document,name='delete_document'),
]
