from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from account_helper.models import Realm
from account_manager.api.v1.permissions import RealmAdminPermission
from account_manager.api.v1.realm.serializers import ExtendedRealmSerializer, RealmUpdateSerializer, \
    RealmCreateSerializer
from account_manager.utils.main_views import get_group_user_count_wrapper


class RealmGroupsApi(generics.ListCreateAPIView):
    """
    list:
    Return the <code>Booking</code> defined by the <code>booking_id</code>.
    """
    permission_classes = [IsAuthenticated, RealmAdminPermission]
    serializer_class = ExtendedRealmSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExtendedRealmSerializer
        if self.request.method == 'POST':
            return RealmCreateSerializer
        return ExtendedRealmSerializer

    def get_queryset(self):
        django_user = self.request.user
        if django_user.is_superuser:
            realms = Realm.objects.order_by('name').all()

        else:
            realms = Realm.objects.filter(admin_group__user__username__contains=django_user.username).order_by('name')
        if realms:
            return [get_group_user_count_wrapper(realm) for realm in realms]
        return realms

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise ValidationError("Realm creation requires super user privileges")
        return super().create(request, args, kwargs)


class RealmGroupApi(generics.RetrieveUpdateDestroyAPIView):
    """
    list:
    Return the <code>Booking</code> defined by the <code>booking_id</code>.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RealmUpdateSerializer
    queryset = Realm.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "realm_id"
