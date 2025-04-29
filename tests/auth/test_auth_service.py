import pytest
from app.users import AuthService
from app.config import Settings
from jose import jwt
from datetime import datetime,UTC, timedelta



@pytest.mark.asyncio
async def test_get_google_redirect_url__succes(auth_service, settings:Settings):
    auth_google_url = await  auth_service.get_google_redirect_url()
    settings_google_url = settings.get_url_redirect
    assert isinstance(auth_google_url, str)
    assert auth_google_url == settings_google_url



@pytest.mark.asyncio
async def test_get_yandex_redirect_url__succes(auth_service, settings:Settings):
    auth_yandex_url = await  auth_service.get_yandex_redirect_url()
    settings_yandex_url = settings.get_yandex_url_redirect
    assert isinstance(auth_yandex_url, str)
    assert auth_yandex_url == settings_yandex_url


@pytest.mark.asyncio
async def test_generate_access_token(auth_service, settings):
    user_id:int = 1

    access_token = auth_service.create_access_token(user_id=user_id)
    decode_access_token = jwt.decode(token=access_token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITM,])
    decode_user_id = decode_access_token.get('user_id')
    decode_exp = datetime.fromtimestamp(decode_access_token.get('exp'),tz=UTC)

    assert decode_user_id == user_id
    assert decode_exp - datetime.now(tz=UTC) > timedelta(days=6)




@pytest.mark.asyncio
async def test_get_user_id_from_access_token(auth_service):
    user_id:int = 1

    access_token = auth_service.create_access_token(user_id=user_id)

    decode_user_id = auth_service.get_user_id_from_access_token(access_token=access_token)

    assert decode_user_id == user_id