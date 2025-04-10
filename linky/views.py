import os
import tempfile
import json
import traceback
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from yt_dlp import YoutubeDL

# ------------------ PAGE VIEWS ------------------
def index(request):
    return render(request, 'home.html')

def instruction(request):
    return render(request, 'insatagram-guide.html')

def instruction2(request):
    return render(request, 'facebook-guide.html')

def instruction3(request):
    return render(request, 'youtube-guide.html')

def policy(request):
    return render(request, 'privacy-policy.html')

def support(request):
    return render(request, 'support.html')

def terms_service(request):
    return render(request, 'terms.html')

def copyright_claims(request):
    return render(request, 'copyright.html')

def terms(request):
    return render(request, 'terms.html')

def copyright_view(request):
    return render(request, 'copyright.html')

# ------------------ DOWNLOAD VIDEO ------------------

@csrf_exempt
@require_POST
def download_video(request):
    try:
        data = json.loads(request.body)
        video_url = data.get('video_url')

        if not video_url:
            return JsonResponse({'error': '❌ Please enter a video URL.'}, status=400)

        # Set path to cookies.txt (in same folder as manage.py)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cookies_path = os.path.join(BASE_DIR, 'cookies.txt')

        if not os.path.exists(cookies_path):
            return JsonResponse({'error': '❌ cookies.txt file not found.'}, status=500)

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_template = os.path.join(tmp_dir, '%(title)s.%(ext)s')

            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': output_template,
                'quiet': True,
                'cookiefile': cookies_path,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)

            if not os.path.exists(filename):
                return JsonResponse({'error': '❌ Download failed. File not found.'}, status=500)

            # ✅ Read file into memory before temp dir is deleted
            with open(filename, 'rb') as f:
                video_bytes = f.read()
                video_name = os.path.basename(filename)

        # ✅ Return video as file response
        response = HttpResponse(video_bytes, content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{video_name}"'
        return response

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': f'❌ Video could not be downloaded: {str(e)}'}, status=500)
