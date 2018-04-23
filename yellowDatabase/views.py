from django.shortcuts import render

#@login_required
def media_xsendfile(request, path, document_root):
    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Sendfile'] = (os.path.join(document_root, path)).encode('utf-8')
    return response

# Create your views here.
