import os
import random
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import requests
from .models import PDF, Publication_user, advertisement, sparks
import hashlib
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import fitz  # PyMuPDF
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
import fitz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from PIL import Image
from io import BytesIO
from .models import PDF, Publication_user
import base64

def encrypt_password(password):
    # Using SHA-256 for password hashing
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()
# Create your views here.
def dashboard(request):
    print("ok")
    if request.method == 'POST':
        search_text = request.POST.get('submit')
        pdfs = PDF.objects.filter(Publication_id__isnull=False, title__icontains=search_text).order_by('date')
        if not pdfs:
            pdfs = PDF.objects.filter(Publication_id__isnull=False).order_by('-date')
    else:
        # pdfs = PDF.objects.filter(Publication_id__isnull=False)
        pdfs = PDF.objects.filter(Publication_id__isnull=False).order_by('-date')

    # Paginate the PDF queryset
    paginator = Paginator(pdfs, 10)  # Set the number of records per page (e.g., 10)
    page = request.GET.get('page')
    print(page)

    try:
        pdfs_page = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, display the first page
        pdfs_page = paginator.page(1)
    except EmptyPage:
        # If the page parameter is out of range (e.g., 9999), display the last page
        pdfs_page = paginator.page(paginator.num_pages)

    # Fetch corresponding Publication_user based on Publication_id
    # Assuming each PDF is related to a single Publication_user
    publication_data = []
    for pdf in pdfs_page:
        try:
            publication_user = Publication_user.objects.get(pk=pdf.Publication_id)
            publication_data.append({'pdf': pdf, 'publication_user': publication_user})
        except Publication_user.DoesNotExist:
            pass  # Handle the case where the corresponding Publication_user is not found
    total_pages = paginator.num_pages
    # print(total_pages)
    # print(pdfs_page.number)
    # img=request.session.get('img', None)
    try:
        user=Publication_user.objects.get(pk=request.session.get('user_id'))
        img=user.profile
    except:
        img=None
        pass
    
    context = {'publication_data': publication_data,'total_pages': total_pages,'pdfs_page': pdfs_page,'img':img}
    return render(request, 'dashboard.html',context)


from django.core.exceptions import ValidationError
import re

def is_valid_title(title):
    # Check if title contains only letters and '|'
    # return re.match("^[a-zA-Z| ]+$", title)
    return re.match("^[a-zA-Z| ]+$", title.strip()) is not None

def is_valid_file_extension(file_name, allowed_extensions):
    # Check if the file has an allowed extension
    return any(file_name.endswith(extension) for extension in allowed_extensions)



def upload(request):

    if 'user_id' not in request.session:
        messages.error(request, "Please Login Before Upload Your File!")
    else:
        if request.method == 'POST':
            # Get form data from request.POST
            title = request.POST.get('title')
            description = request.POST.get('description')

            # Get file data from request.FILES
            file = request.FILES.get('file')
            cover_image = request.FILES.get('cover_image')

            # Validate form data (add more validation if needed)
            if title and file and cover_image:
                # Specify allowed file extensions
                allowed_file_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.svg', '.webp','fifi']
                print(file.name)
                # Validate file extensions
                if not is_valid_file_extension(file.name, allowed_file_extensions) or not is_valid_file_extension(cover_image.name, allowed_file_extensions):
                    messages.error(request, "Invalid file type. Allowed types: PDF, JPG, JPEG, PNG")
                    return redirect("/upload/")

                # Create a new PDF instance and save it
                pdf = PDF(
                    Publication_id=request.session.get('user_id'),
                    title=title,
                    desc=description,
                    file=file,
                    cover_image=cover_image,
                    date=datetime.now().date()
                )
                try:
                    pdf.save()
                    messages.success(request, "Uploaded Successfully!")
                    return redirect("/upload/")

                except ValidationError as e:
                    messages.error(request, f"Validation Error: {e}")
                    return redirect("/upload/")

                except Exception as e:
                    messages.error(request, f"Oops! Something Wrong. Error: {e}")
                    return redirect("/upload/")

            else:
                messages.error(request, "Invalid input. Please check your input data.")
                return redirect("/upload/")

    # img = request.session.get('img', None)
    try:
        user=Publication_user.objects.get(pk=request.session.get('user_id'))
        img=user.profile
        pub_name=user.Publication_Name
        desc=user.description
    except:
        img=None
        pass
    return render(request, 'upload.html', {'img': img})

def uploadss(request):

    if 'user_id' not in request.session:
        messages.error(request,"Please Login Before Upload Your Notes!")
    else:
        if request.method == 'POST':
            # Get form data from request.POST
            title = request.POST.get('title')
            description = request.POST.get('description')

            # Get file data from request.FILES
            file = request.FILES.get('file')
            cover_image = request.FILES.get('cover_image')

            # Validate form data (add more validation if needed)
            if title and file and cover_image:
                # Create a new PDF instance and save it
                pdf = PDF(
                    Publication_id=request.session.get('user_id'),
                    title=title,
                    desc=description,
                    file=file,
                    cover_image=cover_image,
                    date=datetime.now().date()
                )
                try:

                    pdf.save()
                    messages.success(request,"Uploaded Successfully!")
                    return redirect("/upload/")
                    
                except:
                    messages.error(request,"Oops! Something Wrong.")
                    return redirect("/upload/")

    # img=request.session.get('img', None)
    user=Publication_user.objects.get(pk=request.session.get('user_id'))
    img=user.profile
    pub_name=user.Publication_Name
    desc=user.description
    return render(request, 'upload.html',{'img':img})





def profile(request):
    if request.method == 'POST':
        print("ohk")
        login_email = request.POST['email']
        raw_password = request.POST['password']
        encrypted_password = encrypt_password(raw_password)
        try:
            user=Publication_user.objects.get(email=login_email,password=encrypted_password)
            # Storing data in the session
            request.session['user_id'] = user.pk
            request.session['pub_name'] = user.Publication_Name
            request.session['desc'] = user.description
            request.session['img'] = user.profile.name

            # Retrieving data from the session
            # user_id = request.session.get('user_id')
            # pub_name = request.session.get('img', None)
            messages.success(request, 'Login Success.')
        except Exception as e:
            messages.error(request, e)
            pass
    img=request.session.get('img', None)
    pub_name=request.session.get('pub_name', None)
    desc=request.session.get('desc', None)

    try:
        user=Publication_user.objects.get(pk=request.session.get('user_id'))
        img=user.profile
        pub_name=user.Publication_Name
        desc=user.description
    except:
        img=None
        pass


    pdfs = PDF.objects.filter(Publication_id=request.session.get('user_id')).order_by('-date')
    publication_data = []
    for pdf in pdfs:
        try:
            publication_user = Publication_user.objects.get(pk=pdf.Publication_id)
            publication_data.append({'pdf': pdf, 'publication_user': publication_user})
        except Publication_user.DoesNotExist:
            pass
    
    return render(request, 'profile.html',{'img':img,'pub_name':pub_name,'desc':desc,'publication_data':publication_data})
    
def sign_up(request):
    if request.method == 'POST':
        Publication_name = request.POST['Publication_name']
        email = request.POST['username']
        raw_password = request.POST['password']
        encrypted_password = encrypt_password(raw_password)

        # Check for duplicate email
        try:
            user_exist=Publication_user.objects.get(email=email)
            print(user_exist)
            messages.error(request, 'Email is already taken.')
            return redirect('/profile/')
        except:
            pass
        today_date = datetime.now().date()
        # Create a new user
        try:
            user = Publication_user.objects.create(Publication_Name=Publication_name, email=email, password=encrypted_password,DOC=today_date)
            messages.success(request, 'Account created successfully.')
            if user:
                user=Publication_user.objects.get(email=email,password=encrypted_password)
                # Storing data in the session
                request.session['user_id'] = user.pk
                request.session['pub_name'] = user.Publication_Name
                request.session['desc'] = user.description
                request.session['img'] = user.profile.name
                return redirect("/profile/")
            # profile(request,email=email,password=raw_password)
        except Exception as e:
            print(e)
            messages.success(request, 'Oops! Please Try Again.')




    return render(request, 'sign_up.html',)
def uploadpublication(request):
    if request.method == 'POST':
        try:
            proimg = request.FILES.get('proimg')  # Corrected access using parentheses
            pubnameedit = request.POST['pubnameedit']
            # print(pubnameedit)
            descedit = request.POST['descedit']
            user_id = request.session.get('user_id')
            user = Publication_user.objects.get(pk=user_id)
            if proimg:
                user.profile=proimg
            if pubnameedit:
                user.Publication_Name=pubnameedit
            if descedit:
                user.description=descedit
        
            user.save()
            messages.success(request,"Profile Updated Successfully")
        except Exception as e:
            print(e)
            messages.error(request,"Oops! Something Wrong!")
    return redirect("/profile/")




def view(request, pk):
    pdf_model = PDF.objects.get(pk=pk)
    pdf_title = pdf_model.title
    desc = pdf_model.desc
    date = pdf_model.date
    pdf_file_path = pdf_model.file.url
    response = requests.head(pdf_file_path)
    print(pdf_file_path)
    # Extract the part of the URL before the '?' mark
    file_path_without_query_params = pdf_file_path.split('?')[0]

    # Extract the file extension from the URL
    file_extension = file_path_without_query_params.split('.')[-1]

    # Check if the file extension corresponds to a PDF file
    if file_extension.lower() == 'pdf':
        request.session['pdf_file_path'] = pdf_file_path
        is_pdf=True
        img_path=None
    else:
        img_path=pdf_file_path
        is_pdf=False        
    # # Load a document using PyMuPDF
    # pdf_document = fitz.open(pdf_file_path)

    # # Loop over pages and render
    # image_list = []
    # for page_number in range(pdf_document.page_count):
    #     page = pdf_document[page_number]

    #     # Render the page to an image
    #     pix = page.get_pixmap(matrix=fitz.Matrix(4, 4))  # Scale factor (adjust as needed)

    #     # Convert the pixmap to PIL image
    #     pil_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    #     # Save the PIL image to a BytesIO object
    #     image_buffer = BytesIO()
    #     pil_image.save(image_buffer, format="JPEG")  # Adjust the format as needed

    #     # Append BytesIO objects to image_list
    #     image_list.append(image_buffer)

    # # Close the PDF document
    # pdf_document.close()

    # pdfs = PDF.objects.filter(Publication_id__isnull=False, title__icontains=pdf_title).order_by('date')
    # paginator = Paginator(pdfs, 10)
    # page = request.GET.get('page')

    # try:
    #     pdfs_page = paginator.page(page)
    # except PageNotAnInteger:
    #     pdfs_page = paginator.page(1)
    # except EmptyPage:
    #     pdfs_page = paginator.page(paginator.num_pages)

    # publication_data = []
    # for pdf in pdfs_page:
    #     try:
    #         publication_user = Publication_user.objects.get(pk=pdf.Publication_id)
    #         publication_data.append({'pdf': pdf, 'publication_user': publication_user})
    #     except Publication_user.DoesNotExist:
    #         pass
    
    # total_pages = paginator.num_pages
    try:
        total_records = advertisement.objects.count()
        random_index = random.randint(0, total_records - 1)
        random_record = advertisement.objects.all()[random_index]
        print(random_record.banner.url)
    except:
        random_record=None

    # img = request.session.get('img', None)
    try:
        user=Publication_user.objects.get(pk=request.session.get('user_id'))
        img=user.profile
        pub_name=user.Publication_Name
        desc=user.description
    except:
        img=None
        pass
    context = {
        'pdf_file_path':pdf_file_path,
        'is_pdf':is_pdf,
        'pdf_file_path':pdf_file_path,
        'img_path':img_path,
        # 'publication_data': publication_data,
        # 'total_pages': total_pages,
        # 'pdfs_page': pdfs_page,
        'img': img,
        'pdf_title': pdf_title,
        'desc': desc,
        'date': date,
        # 'image_list': image_list,
        'pk':pk,
        'random_record':random_record
    }

    return render(request, 'view.html', context)

def test(request):
    # pdf_url = "https://amrutamnotes.s3.amazonaws.com/media/pdfs/Computer_Fundamentals_FY_BCS_Amrutam_Tech.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA3FLD47SDGBD44Q5B%2F20240329%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T055001Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=847cee4c3f4eeb5aef07eacd4f7ebd8335869492b0e93dc14a79e7fa0bf13ea2"  # Update with your PDF URL
    pdf_url = request.session.get('pdf_file_path')

    # Fetch the PDF content
    response = requests.get(pdf_url)
    if response.status_code == 200:
        # Return the PDF content as HttpResponse
        return HttpResponse(response.content, content_type='application/pdf')
    else:
        return HttpResponse("Failed to fetch PDF", status=response.status_code)
def delete(request, pk):
    if 'user_id' not in request.session:
        messages.error(request, "Oops! Something Wrong!")
        return redirect("/")
    
    try:
        pdf = PDF.objects.get(pk=pk)
        if request.session.get('user_id')!=pdf.Publication_id:
            messages.error(request,"Oops! Something Wrong")
            return redirect("/")
        # Delete associated files from the file system
        if pdf.file:
            file_path = pdf.file.path
            if os.path.exists(file_path):
                os.remove(file_path)

        if pdf.cover_image:
            cover_image_path = pdf.cover_image.path
            if os.path.exists(cover_image_path):
                os.remove(cover_image_path)

        # Delete the PDF record from the database
        pdf.delete()
        messages.success(request,"PDF Deleted Successfully!!!")
    except:
        messages.error(request,'Oops! Please Try Again!!!')
    return redirect('/profile/')

def view_profile(request, pk):
    
    user=Publication_user.objects.get(pk=pk)
    pub_name=user.Publication_Name
    userimg=user.profile
    desc=user.description
    try:
        user=Publication_user.objects.get(pk=request.session.get('user_id'))
        img=user.profile
    except:
        img=None
        pass
    pdfs = PDF.objects.filter(Publication_id=pk).order_by('-date')
    publication_data = []
    for pdf in pdfs:
        try:
            publication_user = Publication_user.objects.get(pk=pdf.Publication_id)
            publication_data.append({'pdf': pdf, 'publication_user': publication_user})
        except Publication_user.DoesNotExist:
            pass
    return render(request, 'view_profile.html',{'userimg':userimg,'img':img,'pub_name':pub_name,'desc':desc,'publication_data':publication_data})
    
    # return redirect('/profile/')
def logout(request):
    # Destroy all session data
    request.session.flush()
    return redirect('/profile/')

def spark(request):
    if 'user_id' not in request.session:
        messages.error(request,"Please Login Before Upload Your Notes!")
    else:
        if request.method == 'POST':
            # Get form data from request.POST
            title = request.POST.get('title')
            # description = request.POST.get('description')

            # Get file data from request.FILES
            
            file = request.FILES.get('spark_image')

            # Validate form data (add more validation if needed)
            if title and file:
                # Specify allowed file extensions
                allowed_file_extensions = ['.jpg', '.jpeg', '.png', '.svg', '.webp','fifi']
                print(file.name)
                # Validate file extensions
                if not is_valid_file_extension(file.name, allowed_file_extensions):
                    messages.error(request, "Invalid file type. Allowed types:JPG, JPEG, PNG")
                    return redirect("/upload/")

                # Create a new PDF instance and save it
                pdf = sparks(
                    Publication_id=request.session.get('user_id'),
                    title=title,
                    file=file,
                    date=datetime.now().date()
                )
                try:
                    pdf.save()
                    messages.success(request, "Uploaded Successfully!")
                    return redirect("/upload/")

                except ValidationError as e:
                    messages.error(request, f"Validation Error: {e}")
                    return redirect("/upload/")

                except Exception as e:
                    messages.error(request, f"Oops! Something Wrong. Error: {e}")
                    return redirect("/upload/")
    all_sparks = sparks.objects.all()
    paginator = Paginator(all_sparks, 1)  # 1 post per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'total_pages': paginator.num_pages
    }
    return render(request, 'spark.html',{'page_obj':page_obj})