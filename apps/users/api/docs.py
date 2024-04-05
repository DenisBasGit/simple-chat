from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from drf_spectacular.utils import OpenApiExample, inline_serializer
from apps.utils import SwaggerWrapper


class AuthorizationSwagger(SwaggerWrapper):
    """Authorization-Documentation"""

    summary = "Authorization"
    description = "Authorization for User."
    tags = ['Users']

    responses = {
        "200": TokenObtainPairSerializer(),
        "401": inline_serializer(
            name="Error detail",
            fields={
                'detail': serializers.CharField(),
            }
        )
    }
    request = TokenObtainPairSerializer()

    examples=[
        OpenApiExample(
            name="Success",
            summary="Example",
            description="Success example",
            value={
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NzY4NDQ5MywiaWF0IjoxNjc3NjczNjkzLCJqdGkiOiIwODVlYWY1MDcxZGM0MDhjOWNhOGU5OTg4OTMwMmYzYSIsInVzZXJfaWQiOiI3ZTg2NzI1Ni04ZjBmLTRjMzgtYThjMi1iYTdkYTRiYjE3M2QifQ.iXQ3hgUaqX7rrNtS0eO29Os7CFpWki2vLasRmDyxNoQ",
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc3Njc3MjkzLCJpYXQiOjE2Nzc2NzM2OTMsImp0aSI6IjhlNTIyMTAxZDczODRlNjY5MGUyYmY0ZmNiNTdhNjlmIiwidXNlcl9pZCI6IjdlODY3MjU2LThmMGYtNGMzOC1hOGMyLWJhN2RhNGJiMTczZCJ9.lpBHCLjmyaRtgbUWta0cKAIC-rLarNcQqp8W1thbZO8"
            },
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            name="Authorization",
            value={
                "username":"admin",
                "password":"yourPassword",
            },
            summary="Example",
            description="Success example",
            request_only=True,
        ),
        OpenApiExample(
            name="Validation Error",
            value={
                "username": [
                    "This field is required.",
                    "This field may not be blank."
                ],
                "password": [
                    "This field is required.",
                    "This field may not be blank."
                ]
            },
            summary="Validation error",
            description="Errors",
            response_only=True,
            status_codes=["400"]
        ),
        OpenApiExample(
            name="Errors",
            value={
                "detail": "No active account found with the given credentials"
            },
            summary="Errors",
            description="This error occurs in cases when any input data doesn't meet existing ones in DB.",
            response_only=True,
            status_codes=["401"]
        ),
    ]

class RefreshSwagger(SwaggerWrapper):
    """Refresh-token-Documentation"""

    summary = "Refresh token"
    description = "Refresh token for User."
    tags = ['Users']

    responses = {
        "200": TokenRefreshSerializer(),
        "401": inline_serializer(
            name="Error detail",
            fields={
                'detail': serializers.CharField(),
            }
        )
    }
    request = TokenRefreshSerializer()

    examples=[
        OpenApiExample(
            name="Success",
            summary="Example",
            description="Success example",
            value={
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NzY4NDQ5MywiaWF0IjoxNjc3NjczNjkzLCJqdGkiOiIwODVlYWY1MDcxZGM0MDhjOWNhOGU5OTg4OTMwMmYzYSIsInVzZXJfaWQiOiI3ZTg2NzI1Ni04ZjBmLTRjMzgtYThjMi1iYTdkYTRiYjE3M2QifQ.iXQ3hgUaqX7rrNtS0eO29Os7CFpWki2vLasRmDyxNoQ",
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc3Njc3MjkzLCJpYXQiOjE2Nzc2NzM2OTMsImp0aSI6IjhlNTIyMTAxZDczODRlNjY5MGUyYmY0ZmNiNTdhNjlmIiwidXNlcl9pZCI6IjdlODY3MjU2LThmMGYtNGMzOC1hOGMyLWJhN2RhNGJiMTczZCJ9.lpBHCLjmyaRtgbUWta0cKAIC-rLarNcQqp8W1thbZO8"
            },
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            name="Authorization",
            value={
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NzY4NTY3OSwiaWF0IjoxNjc3Njc0ODc5LCJqdGkiOiI4NzU4YmNkOTg1OGQ0YzVmYjNiNmI2YjRiM2Y1N2RjMSIsInVzZXJfaWQiOiI3ZTg2NzI1Ni04ZjBmLTRjMzgtYThjMi1iYTdkYTRiYjE3M2QifQ.Uim215Uu38njbI7V2kd4RAi30gfVwpkTCul2S0jA7oK"
            },
            summary="Example",
            description="Success example",
            request_only=True,
        ),
        OpenApiExample(
            name="Validation Error",
            value={
                "refresh": [
                    "This field is required.",
                    "This field may not be blank."
                ]
            },
            summary="Validation error",
            description="",
            response_only=True,
            status_codes=["400"]
        ),
        # OpenApiExample(
        #     name="Errors",
        #     value={
        #         "detail": "error.token_not_valid",
        #     },
        #     summary="Errors",
        #     description="This error occurs when corrupted or expired refresh token is passed",
        #     response_only=True,
        #     status_codes=["401"]
        # )
    ]
