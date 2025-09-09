from datetime import datetime
import os
from django.shortcuts import get_object_or_404, render, redirect
from .forms import DocumentForm
from .models import Document
import docx  # type: ignore
import pdfplumber  # type: ignore
import pytesseract  # type: ignore
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import cv2  # type: ignore
import numpy as np
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter  # type: ignore
from reportlab.pdfgen import canvas  # type: ignore
from docx import Document as DocxDocument  # type: ignore
import io
from django.contrib import messages
import requests # type: ignore

# Set Tesseract path (if you want to keep local OCR as backup)
#pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# tesseract_path = os.getenv('TESSERACT_PATH', '/usr/bin/tesseract')  # Default to '/usr/bin/tesseract' if not set
# pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def extract_text_from_image_ocr_space(file_path):
    api_key = 'K82161001988957'  # Your OCR.Space free API key
    api_url = 'https://api.ocr.space/parse/image'
    with open(file_path, 'rb') as f:
        response = requests.post(
            api_url,
            files={'file': f},
            data={'language': 'eng', 'apikey': api_key}
        )
    result = response.json()
    if result.get('IsErroredOnProcessing') is False and 'ParsedResults' in result:
        return result['ParsedResults'][0]['ParsedText']
    else:
        return "Image OCR failed: " + result.get('ErrorMessage', 'Unknown error')


@csrf_exempt
@login_required
def process_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.created_at = datetime.now()
            document.save()

            file_path = document.file.path
            file_extension = file_path.split('.')[-1].lower()

            if file_extension == 'pdf':
                text = extract_text_from_pdf(file_path)
            elif file_extension == 'docx':
                text = extract_text_from_docx(file_path)
            elif file_extension in ['jpg', 'jpeg', 'png']:
                text = extract_text_from_image_ocr_space(file_path)
            else:
                text = "Unsupported file format"

            document.converted_text = text
            document.save()

            return render(request, 'document_text.html', {'text': text, 'document_id': document.id})
    else:
        form = DocumentForm()
    documents = Document.objects.filter(user=request.user)
    context = {
        'form': form,
        'documents': documents
    }
    return render(request, 'upload_document.html', context)


@login_required
def view_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)
    return render(request, 'document_text.html', {'text': document.converted_text, 'document_id': document_id})


@login_required
def download_as_pdf(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    text = document.converted_text
    textobject = p.beginText()
    textobject.setTextOrigin(100, 750)
    textobject.setFont("Helvetica", 12)
    lines = text.split('\n')
    for line in lines:
        textobject.textLine(line)
    p.drawText(textobject)
    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=document_{document_id}.pdf'
    return response


@login_required
def download_as_docx(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)
    doc = DocxDocument()
    doc.add_paragraph(document.converted_text)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename=document_{document_id}.docx'
    return response


@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)
    document.delete()
    messages.success(request, f'Document {document.file.name} was deleted successfully.')
    return redirect('process_document')


def home(request):
    return render(request, 'login.html')
