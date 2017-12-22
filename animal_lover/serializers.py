from rest_framework import serializers

from animal_lover.models import User, Animal


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password', )

    def __init__(self, **kwargs):
        self.fields['username'].required = False
        self.fields['password'].required = False
        self.fields['email'].required = False
        self.fields['name'].required = False
        super(SignupSerializer, self).__init__(**kwargs)


class LoginSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255, required=False)

    def __init__(self, **kwargs):
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['email'].error_messages['required'] = 'username or email is required'
        super(LoginSerializer, self).__init__(**kwargs)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('email', 'name', 'gender', 'birth_date', 'image')


class AnimalViewSerializer(serializers.ModelSerializer):

    owner = UserSerializer()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Animal
        fields = ['owner', 'type', 'name']

    def get_type(self, obj):
        if obj.type == 1:
            return 'cat'
        elif obj.type == 2:
            return 'dog'
