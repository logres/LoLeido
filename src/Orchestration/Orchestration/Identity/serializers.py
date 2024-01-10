from rest_framework import serializers
from .models import User, Organization, Network, Membership, Environment, CertificateRelated

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ['id']

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
        read_only_fields = ['id']

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = "__all__"
        read_only_fields = ['id']

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"
        read_only_fields = ['id']

class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = "__all__"
        read_only_fields = ['id']

class CertificateRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateRelated
        fields = "__all__"
        read_only_fields = ['id']
