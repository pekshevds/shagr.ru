from typing import Any
from django.http import HttpRequest
from django.conf import settings

from django.core.mail import send_mail
from client_app.models import Client
from client_app.schemas import (
    ClientCredentialSchema,
    ClientSchemaIncoming,
    SendEmailSchemaOutgoing,
)
from repositories import client_repository
from services.jwt_tokens import HS256


def check_clients_pin(client: Client, code: str) -> bool:
    return code in [
        pin.code for pin in client_repository.fetch_active_clients_pins(client)
    ]


def check_credentials(client_schema: ClientCredentialSchema) -> bool:
    client = client_repository.fetch_client_by_email(email=client_schema.email)
    if not client:
        return False
    if not check_clients_pin(client, client_schema.pin):
        return False
    return True


def fetch_token_by_credentials(client_schema: ClientCredentialSchema) -> str:
    if not check_credentials(client_schema):
        return ""
    return HS256.get_token(
        client_schema.email, settings.SECRET_KEY, settings.TOKEN_EXP_MIN
    )


def fetch_pin_by_client(client_schema: ClientSchemaIncoming) -> str:
    client = client_repository.fetch_client_by_email(email=client_schema.email)
    if not client:
        return ""
    return client_repository.create_new_pin(client)


def client_by_token(token: str) -> Client | None:
    payload = HS256.extract_data(token, settings.SECRET_KEY)
    if not payload:
        return None
    return client_repository.fetch_client_by_email(email=payload.name)


def _extract_token_from(token_storage: dict[str, Any]) -> str:
    raw_token = token_storage.get("Authorization")
    if raw_token:
        return raw_token.replace("Bearer", "").strip()
    return ""


def extract_token_from_headers(request: HttpRequest) -> str:
    return _extract_token_from(request.headers)


def extract_token_from_cookies(request: HttpRequest) -> str:
    return _extract_token_from(request.COOKIES)


def extract_token(request: HttpRequest) -> str:
    return extract_token_from_headers(request) or extract_token_from_cookies(request)


def send_pin_by_email(pin_schema: SendEmailSchemaOutgoing) -> None:
    message = (
        f"Покупатель: {pin_schema.client_name}",
        f"Одноразовый пароль: {pin_schema.pin}",
    )
    send_mail(
        subject="Одноразовый пароль для входа на shagr.ru",
        message="\n".join(message),
        recipient_list=[pin_schema.email],
        from_email=None,
    )


"""def process_incoming_request(request: RequestSchemaIncoming) -> None:
    message = (
        "Пожалуйста, перезвоните мне",
        f"Покупатель: {request.name}",
        f"Номер телефона: {request.phone}",
        f"Эл. почта: {request.email}",
    )
    send_mail(
        subject="Запрос на обратный звонок",
        message="\n".join(message),
        recipient_list=[settings.EMAIL_TO_INCOMING_REQUEST],
        from_email=None,
    )"""


"""def process_feedback(feedback: FeedbackSchemaIncoming) -> None:
    message = (
        f"Покупатель: {feedback.name}",
        f"Номер телефона: {feedback.phone}",
        f"Эл. почта: {feedback.email}",
        f"Сообщение:\n{feedback.message}",
    )
    send_mail(
        subject="Обратная связь",
        message="\n".join(message),
        recipient_list=[settings.EMAIL_TO_FEEDBACK],
        from_email=None,
    )"""
