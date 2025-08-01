from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.settings import api_settings


class MSAJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        user_id_field = api_settings.USER_ID_CLAIM
        user_id = validated_token.get(user_id_field)

        user_email = validated_token.get('email')

        if not user_id:
            raise exceptions.AuthenticationFailed(
                f'토큰 페이로드에 "{user_id_field}" 정보가 없습니다. ㅠㅠ')

        if not user_email:
            raise exceptions.AuthenticationFailed(
                f'토큰 페이로드에 "email" 정보가 없습니다. ㅠㅠ')

        class ProxyUser:
            def __init__(self, id, email, is_staff=False, is_superuser=False, scopes=None):
                self.id = id
                self.email = email
                self._is_staff = is_staff
                self._is_superuser = is_superuser
                self._scopes = scopes if scopes is not None else []

            @property
            def is_authenticated(self):
                return True

            @property
            def is_staff(self):
                return self._is_staff

            @property
            def is_superuser(self):
                return self._is_superuser

            def has_perm(self, perm, obj=None):
                return True

            def __str__(self):
                return f"ProxyUser(id={self.id}, email={self.email})"

            @property
            def pk(self):
                return self.id

            @property
            def username(self):
                return str(self.id)

        is_staff_from_token = validated_token.get('is_staff', False)
        is_superuser_from_token = validated_token.get('is_superuser', False)
        scopes_from_token = validated_token.get('scopes', [])

        user = ProxyUser(
            id=user_id,
            email=user_email,
            is_staff=is_staff_from_token,
            is_superuser=is_superuser_from_token,
            scopes=scopes_from_token
        )

        return user, validated_token
