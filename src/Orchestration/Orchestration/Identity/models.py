from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from enum import Enum
# from polymorphic.models import PolymorphicModel
# Create your models here.

# Lot's of Model will be created here

# Identity Model

# class Identity(PolymorphicModel):
#     pass

class User (AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True, blank=True)
    # Abstract User contains
    # username
    # first_name
    # last_name
    # email
    # password
    # and many more

    # Permission Related
    # groups = models.ManyToManyField(Group, related_name='identity_users') 
    organization = models.ManyToManyField('Organization', through='UserOrganization')
    

class Organization (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True, blank=True)
    name = models.CharField(max_length=100)

class UserOrganization (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

class Network (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True, blank=True)
    name = models.CharField(max_length=100)
    organization = models.ManyToManyField(Organization, through='OrganizationNetwork')

class OrganizationNetwork (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)

# Belong to Network and Organization
class Membership (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True, blank=True)
    name = models.CharField(max_length=100)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

class EnvironmentType (Enum):
    FABRIC = "FABRIC"
    ETHEREUM = "ETHEREUM"

class EnvironmentProtocal (Enum):
    RAFT = "RAFT"

class EnvironmentClient (Enum):
    GETH = "GETH"
    FABRIC = "FABRIC"

class Environment (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True, blank=True)
    name = models.CharField(max_length=100)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    membership = models.ManyToManyField(Membership, through='MembershipEnvironment')
    _type = models.CharField(max_length=100, choices=[(tag, tag.value) for tag in EnvironmentType])
    protocal = models.CharField(max_length=100, choices=[(tag, tag.value) for tag in EnvironmentProtocal])
    client = models.CharField(max_length=100, choices=[(tag, tag.value) for tag in EnvironmentClient])

class MembershipEnvironment (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True, blank=True)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)

# Certificate and PrivateKey Publickey

class CertificateRelated (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True, blank=True)
    name = models.CharField(max_length=100)
    certificate = models.CharField(max_length=10000)
    private_key = models.CharField(max_length=10000)
    public_key = models.CharField(max_length=10000)

# Resource 
## Fabric 
    
class FabricCA (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True, blank=True)
    name = models.CharField(max_length=100) # CA Name
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)

class NodeType(Enum):
    PEER = "PEER"
    ORDERER = "ORDERER"

class Node (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True, blank=True)
    name = models.CharField(max_length=100)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    node_type = models.CharField(max_length=100, choices=[(tag, tag.value) for tag in NodeType])
    # certificate_related = models.ForeignKey(CertificateRelated, on_delete=models.CASCADE)



# class FabricClient (models.Model):
#     id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True, blank=True)
#     name = models.CharField(max_length=100)
#     network = models.ForeignKey(Network, on_delete=models.CASCADE)
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
#     environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    # certificate_related = models.ForeignKey(CertificateRelated, on_delete=models.CASCADE)

# class FabricAdmin (models.Model):
#     id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True, blank=True)
#     name = models.CharField(max_length=100)
#     network = models.ForeignKey(Network, on_delete=models.CASCADE)
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
#     environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    # certificate_related = models.ForeignKey(CertificateRelated, on_delete=models.CASCADE)

