from django.shortcuts import render
from .models import (
    User,
    Organization,
    Network,
    Membership,
    Environment,
    CertificateRelated,
)
from rest_framework import viewsets

from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    UserSerializer,
    OrganizationSerializer,
    NetworkSerializer,
    MembershipSerializer,
    EnvironmentSerializer,
    CertificateRelatedSerializer,
)

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # register
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserSerializer},
        operation_id="create_user",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # update
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserSerializer},
        operation_id="update_user",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    # Create
    # A User will be Created with a Organization
    @swagger_auto_schema(
        request_body=OrganizationSerializer,
        responses={200: OrganizationSerializer},
        operation_id="create_organization",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class NetworkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Network.objects.all()
    serializer_class = NetworkSerializer

    # Create
    # A Network is a combination of Some Organizations, and will be init with an Organization
    @swagger_auto_schema(
        request_body=NetworkSerializer,
        responses={200: NetworkSerializer},
        operation_id="create_network",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

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
