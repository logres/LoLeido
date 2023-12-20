from django.db import models
from django.contrib.auth.models import AbstractUser,  Group, Permission
# from polymorphic.models import PolymorphicModel
# Create your models here.

# Lot's of Model will be created here

# Identity Model

# class Identity(PolymorphicModel):
#     pass

class User (AbstractUser):
    id = models.UUIDField(primary_key=True)
    groups = models.ManyToManyField(Group, related_name='identity_users')
    user_permissions = models.ManyToManyField(Permission, related_name='identity_users')

class Organization (models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)

class UserOrganization (models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

class Network (models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

class OrganizationNetwork (models.Model):
    id = models.UUIDField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)

# Belong to Network and Organization
class Membership (models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class Environment (models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)

# Certificate and PrivateKey Publickey

class CertificateRelated (models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    certificate = models.CharField(max_length=10000)
    private_key = models.CharField(max_length=10000)
    public_key = models.CharField(max_length=10000)

# Resource 
## Fabric 

class PeerNode (models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    certificate_related = models.ForeignKey(CertificateRelated, on_delete=models.CASCADE)

class OrdererNode (models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    certificate_related = models.ForeignKey(CertificateRelated, on_delete=models.CASCADE)

class FabricClient (models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    certificate_related = models.ForeignKey(CertificateRelated, on_delete=models.CASCADE)

class FabricAdmin (models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    certificate_related = models.ForeignKey(CertificateRelated, on_delete=models.CASCADE)

