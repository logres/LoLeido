from django.urls import path, include
from rest_framework import routers
from .views import (
    UserViewSet,
    OrganizationViewSet,
    NetworkViewSet,
    MembershipViewSet,
    EnvironmentViewSet,
    CertificateRelatedViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"organizations", OrganizationViewSet)
router.register(r"networks", NetworkViewSet)
router.register(r"memberships", MembershipViewSet)
router.register(r"environments", EnvironmentViewSet)
router.register(r"certificates", CertificateRelatedViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # 可以添加其他URL模式
]