from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample, inline_serializer

from apps.chat.api.serializers import CreateThreadSerializer, ThreadSerializer, CreateMessageSerializer, \
    MessageSerializer
from apps.utils import SwaggerWrapper


class CreateThreadSwagger(SwaggerWrapper):
    """Create Thread Documentation"""

    summary = "Create thread"
    description = "Create thread or retreive thread with participant"
    tags = ["Chat"]

    responses = {
        "200": CreateThreadSerializer(),
        "400": CreateThreadSerializer(),
        "401": inline_serializer(
            name="Authorization Error",
            fields={
                'detail': serializers.CharField(),
            }
        )
    }
    request = CreateThreadSerializer()

    examples=[
        OpenApiExample(
            name="Success",
            summary="Example",
            description="Success example",
            value={
                "id": 6,
                "created": "2024-04-05T12:21:37.766264+03:00"
            },
            response_only=True,
            status_codes=["200", "201"]
        ),
        OpenApiExample(
            name="Success",
            value={
                "participant": 1,
            },
            summary="Example",
            description="Success example",
            request_only=True,
        ),
        OpenApiExample(
            name="Validation Error",
            value={
                "participant": [
                    "This field is required.",
                    "This field may not be null.",
                    "Invalid pk \"10\" - object does not exist."
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

class DeleteThreadSwagger(SwaggerWrapper):
    """Delete Thread Documentation"""

    summary = "Delete thread"
    description = "Delete thread"
    tags = ["Chat"]

    responses = {
        "204": None,
        "401": inline_serializer(name="Authorization Error", fields={'detail': serializers.CharField()}),
        "403": inline_serializer(name="Permission Error", fields={'detail': serializers.CharField()}),
        "404": inline_serializer(name="Not found", fields={'detail': serializers.CharField()})
    }

    request = None

    examples = [
        OpenApiExample(
            name="Success",
            summary="Example",
            description="Success example",
            value=None,
            response_only=True,
            status_codes=["204"]
        ),
        OpenApiExample(
            name="Authentication error",
            value={
                "detail": "No active account found with the given credentials"
            },
            summary="Authentication error",
            description="This error occurs in cases when any input data doesn't meet existing ones in DB.",
            response_only=True, status_codes=["401"]
        ),
        OpenApiExample(
            name="Permission Denied",
            value={"detail": "You do not have permission to perform this action."},
            summary="Permission Denied",
            description="You do not have permission to perform this action.",
            response_only=True, status_codes=["403"]
        ),
        OpenApiExample(
            name="Not found",
            value={"detail": "No Thread matches the given query."},
            summary="Not found",
            description="You cannot perform this action",
            response_only=True,
            status_codes=["404"]
        )
    ]


class ListThreadByUserSwagger(SwaggerWrapper):
    """List thread by user"""

    summary = "List thread by user"
    description = "List thread by user"
    tags = ["Chat"]

    responses = {
        "200": ThreadSerializer(),
        "401": inline_serializer(name="Authorization Error", fields={'detail': serializers.CharField()}),

    }

    request = None

    examples = [
        OpenApiExample(
            name="Success",
            summary="Example",
            description="Success example",
            value={
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "created": "2024-04-04T13:32:30+03:00",
                        "updated": "2024-04-04T13:32:31+03:00",
                        "participants": [
                            1,
                            2
                        ]
                    }
                ]
            },
            response_only=True,
            status_codes=["201"]
        ),
        OpenApiExample(
            name="Authentication error",
            value={"detail": "No active account found with the given credentials"},
            summary="Authentication error",
            description="This error occurs in cases when any input data doesn't meet existing ones in DB.",
            response_only=True,
            status_codes=["401"]
        ),
    ]


class CreateMessageForThreadSwagger(SwaggerWrapper):
    """Create message for thread swagger"""

    summary = "Create message for thread"
    description = "Create message for thread by user"
    tags = ["Chat"]

    responses = {
        "201": CreateMessageSerializer(),
        "401": inline_serializer(name="Authorization Error", fields={'detail': serializers.CharField()}),
        "403": inline_serializer(name="Permission Error", fields={'detail': serializers.CharField()}),
        "404": inline_serializer(name="Not found", fields={'detail': serializers.CharField()})
    }


    request = CreateMessageSerializer

    examples = [
        OpenApiExample(
            name="Success",
            summary="Example",
            description="Success request example",
            value={"text": "Test message"},
            request_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            name="Success",
            summary="Example",
            description="Success example",
            value={
                "text": "Test message"
            },
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            name="Authentication error",
            value={"detail": "No active account found with the given credentials"},
            summary="Authentication error",
            description="This error occurs in cases when any input data doesn't meet existing ones in DB.",
            response_only=True,
            status_codes=["401"]
        ),
        OpenApiExample(
            name="Permission Denied",
            value={"detail": "You do not have permission to perform this action."},
            summary="Permission Denied",
            description="You do not have permission to perform this action.",
            response_only=True,
            status_codes=["403"]
        ),
        OpenApiExample(
            name="Not found",
            value={"detail": "No Thread matches the given query."},
            summary="Not found",
            description="Not found",
            response_only=True,
            status_codes=["404"]
        )
    ]


class GetMessageForThreadSwagger(SwaggerWrapper):
    """Create message for thread swagger"""
    summary = "Get message for thread"
    description = "Get message for thread by user"
    tags = ["Chat"]

    responses = {
        "200": MessageSerializer(),
        "401": inline_serializer(name="Authorization Error", fields={'detail': serializers.CharField()}),
        "403": inline_serializer(name="Permission Error", fields={'detail': serializers.CharField()}),
        "404": inline_serializer(name="Not found", fields={'detail': serializers.CharField()})
    }


    request = None

    examples = [
        OpenApiExample(
            name="Success",
            summary="Example",
            description="Success example",
            value={
                "count": 14,
                "next": "http://localhost:8080/api/v1/chat/thread/1/message/?limit=10&offset=10",
                "previous": None,
                "results": [
                    {
                        "id": 15,
                        "sender": "John Smith",
                        "text": "Test Message",
                        "created": "2024-04-05T13:18:33.198295+03:00",
                        "is_read": False
                    },
                    {
                        "id": 14,
                        "sender": "John Smith",
                        "text": "Test Message",
                        "created": "2024-04-05T13:18:32.562315+03:00",
                        "is_read": False
                    },
                ]
            },
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            name="Authentication error",
            value={"detail": "No active account found with the given credentials"},
            summary="Authentication error",
            description="This error occurs in cases when any input data doesn't meet existing ones in DB.",
            response_only=True,
            status_codes=["401"]
        ),
        OpenApiExample(
            name="Permission Denied",
            value={"detail": "You do not have permission to perform this action."},
            summary="Permission Denied",
            description="You do not have permission to perform this action.",
            response_only=True,
            status_codes=["403"]
        ),
        OpenApiExample(
            name="Not found",
            value={"detail": "No Thread matches the given query."},
            summary="Not found",
            description="Not found",
            response_only=True,
            status_codes=["404"]
        )
    ]


class ReadMessageSwagger(SwaggerWrapper):
    """Read message for thread swagger"""
    summary = "Read message"
    description = "Read message"
    tags = ["Chat"]

    responses = {
        "401": inline_serializer(name="Authorization Error", fields={'detail': serializers.CharField()}),
        "403": inline_serializer(name="Permission Error", fields={'detail': serializers.CharField()}),
        "404": inline_serializer(name="Not found", fields={'detail': serializers.CharField()})
    }


    request = None

    examples = [
        OpenApiExample(
            name="Authentication error",
            value={"detail": "No active account found with the given credentials"},
            summary="Authentication error",
            description="This error occurs in cases when any input data doesn't meet existing ones in DB.",
            response_only=True,
            status_codes=["401"]
        ),
        OpenApiExample(
            name="Permission Denied",
            value={"detail": "You do not have permission to perform this action."},
            summary="Permission denied to thread",
            description="You do not have permission to perform this action.",
            response_only=True,
            status_codes=["403"]
        ),
        OpenApiExample(
            name="Permission Denied ",
            value={"detail": "You do not have permission to perform this action."},
            summary="Permission denied to message",
            description="You cannot mark as read your own message",
            response_only=True,
            status_codes=["403"]
        ),
        OpenApiExample(
            name="Not found",
            value={"detail": "No Thread matches the given query."},
            summary="Not found",
            description="Not found",
            response_only=True,
            status_codes=["404"]
        )
    ]


class GetCountUnReadMessageSwagger(SwaggerWrapper):
    """Get count of unread message for user """
    summary = "Count unread messsage"
    description = "Get count of unread message for user "
    tags = ["Chat"]

    responses = {
        "200": inline_serializer(name="Authorization Error", fields={'count': serializers.IntegerField()}),
        "401": inline_serializer(name="Authorization Error", fields={'detail': serializers.CharField()}),
    }


    request = None

    examples = [
        OpenApiExample(
            name="Success",
            summary="Example",
            description="Success example",
            value={"count": 14},
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            name="Authentication error",
            value={"detail": "No active account found with the given credentials"},
            summary="Authentication error",
            description="This error occurs in cases when any input data doesn't meet existing ones in DB.",
            response_only=True,
            status_codes=["401"]
        ),
    ]
