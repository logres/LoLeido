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

# Some API not viewset


from rest_framework.views import APIView
from Orchestration.Identity.external_api import (
    create_ca,
    delete_ca,
    get_ca,
    get_ca_list,
    create_fabric_peer,
    delete_fabric_peer,
    get_fabric_peer,
    get_fabric_orderer,
    create_fabric_orderer,
    delete_fabric_orderer,
    get_fabric_orderer_list,
    instantiate_chaincode
)


class setup_environment(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    def post(self, request, format=None):
        # parse request
        environment_id = request.data.get('environment_id')
        membership_id = request.data.get('membership_id')
        Fabric_ca_certificate = request.data.get('Fabric_ca_certificate')
        peer_node_count = request.data.get('peer_node_count')
        orderer_node_count = request.data.get('orderer_node_count')
        # get environment
        environment = Environment.objects.get(id=environment_id)
        # get membership
        membership = Membership.objects.get(id=membership_id)
        # Some External API

        # Create CA
        ca_name = "ca-{}".format(environment.name)

        # register peer and orderer

        # set up orderer
        create_fabric_peer()
        # enroll orderer

        # set up peer
        create_fabric_orderer()
        # enroll peer
        
        # create channel

        # join channel


class install_chaincode(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    def post(self, request, format=None):
        # parse request
        chaincode = request.data.get('chaincode')
        # get environment
        environment_id = request.data.get('environment_id')
        membership_id = request.data.get('membership_id')

        environment = Environment.objects.get(id=environment_id)
        membership = Membership.objects.get(id=membership_id)

        # Some External API
        # install chaincode

        install_chaincode(
            environment_id=environment_id,
            membership_id=membership_id,
            chaincode=chaincode,
            certificate = membership.certificate_related.certificate,
        )

        # instantiate chaincode
        instantiate_chaincode(
            environment_id=environment_id,
            membership_id=membership_id,
            chaincode=chaincode,
            certificate = membership.certificate_related.certificate,
        )
        

class invoke_chaincode(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    def post(self, request, format=None):
        # parse request
        chaincode = request.data.get('chaincode')
        # get environment
        environment_id = request.data.get('environment_id')
        membership_id = request.data.get('membership_id')

        environment = Environment.objects.get(id=environment_id)
        membership = Membership.objects.get(id=membership_id)

        # Some External API
        # invoke chaincode
        invoke_chaincode(
            environment_id=environment_id,
            membership_id=membership_id,
            chaincode=chaincode,
            certificate = membership.certificate_related.certificate,
        )


