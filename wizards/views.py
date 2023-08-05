from rest_framework import generics
from .serializers import WizardSerializer
from .models import Wizard
from .permissions import IsOwnerOrReadOnly


class WizardList(generics.ListCreateAPIView):
 
    queryset = Wizard.objects.all()
    serializer_class = WizardSerializer

class WizardDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)  
    queryset = Wizard.objects.all()
    serializer_class = WizardSerializer
