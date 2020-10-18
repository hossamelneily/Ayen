from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView

from account.models import Account
# from api.filters.account import PassportCopyFilter
from api.serializer.account import RegisterSerializer, AccountDocumentsSerializer, AccountMetaDataSerializer, \
    CustomLoginSerializer, AccountSerializer
from rest_framework import permissions, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_auth.views import LoginView, LogoutView
from rest_framework.exceptions import APIException, ValidationError


class Register(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)

    def perform_create(self, serializer):
        email = serializer.data["email"]
        password = serializer.data["password"]
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
            )
            try:
                account = Account.objects.create(
                    user=user,

                )
            except Exception as e:
                raise APIException({'detail': str(e)})
        except Exception as e:
            raise APIException({'detail': str(e)})

        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomLoginView(LoginView):

    def get_response(self):
        return Response(status=status.HTTP_200_OK)


class AccountMetaData(UpdateAPIView):
    serializer_class = AccountMetaDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['put']

    def get_object(self):
        try:
            return Account.objects.get(user=self.request.user)
        except Exception:
            raise ValidationError({'detail': 'User not have an account.'})


class AccountMetaDataListAPI(ListAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']
    queryset = Account.objects.all()


class AccountMetaDataDetailAPI(ListAPIView):
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('occupation',)


class AccountUploadDocuments(UpdateAPIView):
    serializer_class = AccountDocumentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['put']

    def get_object(self):
        try:
            return Account.objects.get(user=self.request.user)
        except Exception:
            raise ValidationError({'detail': 'User not have an account.'})



class AccountDocListAPI(ListAPIView):
    serializer_class = AccountDocumentsSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']
    queryset = Account.objects.all()


class AccountDocDetailAPI(ListAPIView):
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountDocumentsSerializer

    def get_queryset(self):
        queryset = Account.objects.all()
        keywords = self.request.query_params.get('search')
        if keywords:
            queryset = queryset.filter(passport_copy__icontains=keywords)
        return queryset
