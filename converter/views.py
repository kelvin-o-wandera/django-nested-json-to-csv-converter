import requests
from django.conf import settings
from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.
def index(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        # fs = FileSystemStorage()
        # filename = fs.save(file.name, file)
        # uploaded_file_url = fs.url(filename)
        # return render(request, 'index.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })

    return render(request, "index.html", {})


def sample_json(request):
    myfile = requests.get("http://" + get_current_site(request).domain + settings.MEDIA_URL + '/sample_json/batters.json')
    response = HttpResponse(myfile.content, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=sample.json'
    return response
