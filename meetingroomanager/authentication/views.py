from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.response import Response

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    TokenSerializer,
)


class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = {}
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        print(headers)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
                status=status.HTTP_200_OK,
            )
        else:
            print(serializer.errors)
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserTokenAPIView(RetrieveDestroyAPIView):
    lookup_field = "key"
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        Token.objects.get(key=request.auth.key).delete()
        return Response(
            data={"message": "User logged out"},
            status=status.HTTP_204_NO_CONTENT
        )
