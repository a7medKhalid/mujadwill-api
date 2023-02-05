from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .helpers.ImportSections import importSectionsFunction



from .models import *
from .serializers import *

class upload_sections(APIView):
    
    # upload sections csv file
    def post(self, request, format=None):
        
        importSectionsFunction(request.FILES['file'])
        return Response(status=status.HTTP_201_CREATED)

        