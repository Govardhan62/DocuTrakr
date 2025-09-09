from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import tempfile, os ,subprocess

@login_required
def convert_to_pdf(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]

        if not uploaded_file.name.lower().endswith(".docx"):
            return HttpResponseBadRequest("Please upload a DOCX file.")

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                input_path = os.path.join(temp_dir, uploaded_file.name)
                output_dir = temp_dir

                # Save uploaded file
                with open(input_path, "wb") as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)

                # Run LibreOffice to convert DOCX -> PDF
                subprocess.run(
                    [r"C:\Program Files\LibreOffice\program\soffice.exe",
                    "--headless",
                    "--convert-to", "pdf:writer_pdf_Export",
                    "--outdir", output_dir,
                    input_path],
                    check=True
                )

                output_path = os.path.splitext(input_path)[0] + ".pdf"

                with open(output_path, "rb") as f:
                    pdf_data = f.read()

            response = HttpResponse(pdf_data, content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="converted.pdf"'
            return response

        except Exception as e:
            return HttpResponseBadRequest(f"Conversion error: {e}")

    return render(request, "convert_to_pdf.html")


from pdf2docx import Converter # type: ignore

@login_required
def convert_to_doc(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]

        if not uploaded_file.name.lower().endswith(".pdf"):
            return HttpResponseBadRequest("Please upload a PDF file.")

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                input_path = os.path.join(temp_dir, uploaded_file.name)
                output_path = os.path.splitext(input_path)[0] + ".docx"

                # Save uploaded PDF
                with open(input_path, "wb") as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)

                # Convert PDF -> DOCX
                cv = Converter(input_path)
                cv.convert(output_path, start=0, end=None)
                cv.close()

                with open(output_path, "rb") as f:
                    doc_data = f.read()

            response = HttpResponse(doc_data, content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response["Content-Disposition"] = 'attachment; filename="converted.docx"'
            return response

        except Exception as e:
            return HttpResponseBadRequest(f"Conversion error: {e}")

    return render(request, "convert_to_doc.html")
