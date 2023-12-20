from django.shortcuts import render
from django.contrib.auth.models import (
    User,
    Organization,
    Network,
    Membership,
    Environment,
    CertificateRelated,
)

from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class NetworkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class EnvironmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer


class CertificateRelatedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = CertificateRelated.objects.all()
    serializer_class = CertificateRelatedSerializer
