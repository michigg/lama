from django.urls import path

from account_manager.api.v1.group.views import RealmGroupsApi, RealmGroupApi
from account_manager.api.v1.super_admin.views import SuperAdminUsersApi, SuperAdminUserApi, WelcomeMail, DeletionMail
from account_manager.api.v1.user.views import RealmUserApi, RealmUsersApi, RealmUserPasswordResetMail, \
    RealmUserWelcomeMail, RealmUserGroupsApi
from account_manager.api.v1.realm.views import RealmsApi, RealmApi, MailTestingApi

urlpatterns = [
    path('v1/realm/', RealmsApi.as_view()),
    path('v1/realm/<int:realm_id>/', RealmApi.as_view()),

    # Not done yet
    path('v1/realm/<int:realm_id>/mail/test/', MailTestingApi.as_view()),

    path('v1/realm/<int:realm_id>/group/', RealmGroupsApi.as_view()),
    path('v1/realm/<int:realm_id>/group/<str:group_dn>/', RealmGroupApi.as_view()),

    path('v1/realm/<int:realm_id>/user/', RealmUsersApi.as_view()),
    path('v1/realm/<int:realm_id>/user/<str:user_dn>/', RealmUserApi.as_view()),
    path('v1/realm/<int:realm_id>/user/<str:user_dn>/group/', RealmUserGroupsApi.as_view()),
    path('v1/realm/<int:realm_id>/user/<str:user_dn>/delete/cancel/', RealmUserPasswordResetMail.as_view()),
    path('v1/realm/<int:realm_id>/user/<str:user_dn>/mail/password-reset/', RealmUserPasswordResetMail.as_view()),
    path('v1/realm/<int:realm_id>/user/<str:user_dn>/mail/welcome/', RealmUserWelcomeMail.as_view()),

    path('v1/admin/user/', SuperAdminUsersApi.as_view()),
    path('v1/admin/user/<int:id>/', SuperAdminUserApi.as_view()),
    path('v1/admin/mail/welcome/', WelcomeMail.as_view()),
    path('v1/admin/mail/deletion/', DeletionMail.as_view()),
]
