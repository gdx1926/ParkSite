from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from park.models import Document
from park.forms import DocumentForm
import requests
import json
import mysite.settings

# Create your views here.

@csrf_exempt
def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect("/park/list/")
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    if documents:
        lastDocument = Document.objects.latest('id')

    url = 'https://api.openalpr.com/v2/recognize?recognize_vehicle=1&country=us&secret_key=sk_de519850c0c074c9ff4b38c9'
    with open(mysite.settings.BASE_DIR+lastDocument.docfile.url, 'rb') as f:
        r = requests.post(url, files={'image': f})
        pastebin_url = r.text

    info = json.loads(pastebin_url)
    plate = info["results"][0]["plate"];
    region = info["results"][0]["region"].upper();
    color = info["results"][0]["vehicle"]["color"][0]["name"];


    # Render list page with the documents and the form
    return render_to_response(
        'park/list.html',
        {'documents': documents,
         'lastDocument': lastDocument,
         'form': form,
         'plate': plate,
         'region': region,
         'color': color}
    )

def index(request):
    return render_to_response('park/index.html')