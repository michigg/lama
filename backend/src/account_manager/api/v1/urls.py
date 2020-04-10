from django.urls import path

from account_manager.api.v1.realm_group_views import RealmGroupsApi, RealmGroupApi
from account_manager.api.v1.user.views import RealmUserApi, RealmUsersApi, RealmUserPasswordResetMail, \
    RealmUserWelcomeMail, RealmUserGroupsApi
from account_manager.api.v1.realm.views import RealmsApi, RealmApi, MailTestingApi

urlpatterns = [
    path('v1/realm/', RealmsApi.as_view()),
    path('v1/realm/<int:realm_id>/', RealmApi.as_view()),

    # Not done yet
    path('v1/realm/<int:realm_id>/mail/test/', MailTestingApi.as_view()),

    path('v1/realm/<int:realm_id>/group/', RealmGroupsApi.as_view()),
    path('v1/realm/<int:realm_id>/group/<int:group_id>/', RealmGroupApi.as_view()),

    path('v1/realm/<int:realm_id>/user/', RealmUsersApi.as_view()),
    path('v1/realm/<int:realm_id>/user/<str:user_dn>/', RealmUserApi.as_view()),
    path('v1/realm/<int:realm_id>/user/<str:user_dn>/group/', RealmUserGroupsApi.as_view()),
    path('v1/realm/<int:realm_id>/user/<str:user_dn>/delete/cancel/', RealmUserPasswordResetMail.as_view()),
    path('v1/realm/<int:realm_id>/user/<str:user_dn>/mail/password-reset/', RealmUserPasswordResetMail.as_view()),
    path('v1/realm/<int:realm_id>/user/<str:user_dn>/mail/welcome/', RealmUserWelcomeMail.as_view()),
]
