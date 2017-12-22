from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.
from animal_lover.serializers import *
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate


class UserLoginAPIView(APIView):

    permission_classes = (AllowAny,)
    response_serializer = UserSerializer
    http_method_names = ['post', ]
    user = None

    def post(self, request, **kwargs):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = authenticate(**serializer.data)

                if user is not None:
                        user_token, created = Token.objects.get_or_create(user=user)
                        return Response({'user': self.response_serializer(user).data, 'token': user_token.key},
                                        status=status.HTTP_200_OK)
                return Response({'success': False, 'error': "user is not authenticated"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'error': ex.__unicode__(), 'success': False})


class UserSignupAPIView(CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny, )
    response_serializer = UserSerializer
    http_method_names = ['post', ]
    model = User
    user = None

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user = serializer.instance
            user.set_password(serializer.validated_data.get('password'))
            user.is_active = True
            user_token, created = Token.objects.get_or_create(user=user)
            return Response({'user': self.response_serializer(serializer.instance).data, 'success': True, 'token': user_token })
        except Exception as ex:
            return Response({'error': ex.__unicode__(), 'success': False})


class AnimalView(ListCreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = AnimalViewSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):

        try:
            id = self.kwargs.get('animal')
            queryset = self.model.objects.filter(id=id)
            return queryset
        except Exception as ex:
            raise Exception(_(ex.__unicode__()))

    def create(self, request, *args, **kwargs):
        try:
            object = self.model.objects.create(
                owner=self.request.user,
                name=self.kwargs.get('name'),
                type=self.kwargs.get('type'),
            )
        except Exception as ex:
            return Response({'message': ex.__unicode__(), 'status': False},
                            status=status.HTTP_417_EXPECTATION_FAILED)

        serializer = self.serializer_class(object, many=False, context={'obj': object})
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DeleteAnimalView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = AnimalViewSerializer
    model = serializer_class.Meta.model

    def post(self, request):

        id = self.kwargs.get('animal')
        try:
            if request.user.is_authenticated():
                Animal.objects.get(id=id).delete()
            return Response({'message': 'animal delete'})
        except Exception as ex:
            return Response({'message': ex.__unicode__(), 'status': False},
                        status=status.HTTP_417_EXPECTATION_FAILED)


class UpdateAnimalView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = AnimalViewSerializer
    model = serializer_class.Meta.model

    def post(self, request):

        id = self.kwargs.get('animal')
        try:
            if request.user.is_authenticated():
                obj, updated = Animal.objects.update_or_create(id=id, defaults=self.kwargs)
                serializer = self.serializer_class(obj, many=False, context={'obj', obj})
            return Response({serializer.data})
        except Exception as ex:
            return Response({'message': ex.__unicode__(), 'status': False},
                        status=status.HTTP_417_EXPECTATION_FAILED)