import pytest
from Identity.models import (
    User,
    Organization,
    Network,
    Membership,
    Environment,
    CertificateRelated,
    UserOrganization,
    OrganizationNetwork,
    MembershipEnvironment,
)
from django.conf import settings


@pytest.fixture(scope="module")
def db_setup():
    # use a sqlite database for testing
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_db",
    }
    yield


@pytest.mark.django_db
def test_user(db_setup):
    # create a user
    user = User.objects.create(username="test_user")
    # check that the user has been created
    assert User.objects.count() == 1
    # check that the username is correct
    assert User.objects.get(username="test_user").username == "test_user"


@pytest.mark.django_db
def test_organization(db_setup):
    # create a organization
    organization = Organization.objects.create(name="test_organization")
    # check that the organization has been created
    assert Organization.objects.count() == 1
    # check that the name is correct
    assert (
        Organization.objects.get(name="test_organization").name == "test_organization"
    )


@pytest.mark.django_db
def test_user_organization(db_setup):
    # create a user
    user = User.objects.create(username="test_user")
    # create a organization
    organization = Organization.objects.create(name="test_organization")
    # set user.organization to organization
    user.organization.add(organization)
    # check that the user_organization has been created
    assert UserOrganization.objects.count() == 1
    # check that the user is correct
    assert UserOrganization.objects.get(user=user).user == user
    # check that the organization is correct
    assert (
        UserOrganization.objects.get(organization=organization).organization
        == organization
    )


@pytest.mark.django_db
def test_network(db_setup):
    # create a network
    network = Network.objects.create(name="test_network")
    # check that the network has been created
    assert Network.objects.count() == 1
    # check that the name is correct
    assert Network.objects.get(name="test_network").name == "test_network"

@pytest.mark.django_db
def test_organization_network(db_setup):
    # create a organization
    organization = Organization.objects.create(name="test_organization")
    # create a network
    network = Network.objects.create(name="test_network")
    # set organization.network to network
    network.organization.add(organization)
    # check that the organization_network has been created
    assert OrganizationNetwork.objects.count() == 1
    # check that the organization is correct
    assert OrganizationNetwork.objects.get(organization=organization).organization == organization
    # check that the network is correct
    assert OrganizationNetwork.objects.get(network=network).network == network


@pytest.mark.django_db
def test_membership(db_setup):
    # create a Network
    network = Network.objects.create(name="test_network")
    # create a Organization
    organization = Organization.objects.create(name="test_organization")
    # create a membership
    membership = Membership.objects.create(name="test_membership", network=network, organization=organization)
    # check that the membership has been created
    assert Membership.objects.count() == 1
    # check that the name is correct
    assert Membership.objects.get(name="test_membership").name == "test_membership"

@pytest.mark.django_db
def test_Environment(db_setup):
    # create a Network
    network = Network.objects.create(name="test_network")
    # create a Environment
    environment = Environment.objects.create(name="test_environment", network=network)
    # check that the environment has been created
    assert Environment.objects.count() == 1
    # check that the name is correct
    assert Environment.objects.get(name="test_environment").name == "test_environment"