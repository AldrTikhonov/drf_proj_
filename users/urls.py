from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (UserCreateAPIView, PaymentsCreateApiView)

app_name = UsersConfig.name


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    # path("payment/", PaymentsListApiView.as_view(), name="payment_list"),
    # path(
    #     "payment/<int:pk>/", PaymentsRetrieveApiView.as_view(), name="payment_retrieve"
    # ),
    path("payment/create/", PaymentsCreateApiView.as_view(), name="payment_create"),
    # path(
    #     "payment/<int:pk>/update/",
    #     PaymentsUpdateApiView.as_view(),
    #     name="payment_update",
    # ),
    # path(
    #     "payment/<int:pk>/delete/",
    #     PaymentsDestroyApiView.as_view(),
    #     name="payment_delete",
    # ),
]
