from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.chat.api.docs import (
    CreateMessageForThreadSwagger,
    CreateThreadSwagger,
    DeleteThreadSwagger,
    GetCountUnReadMessageSwagger,
    GetMessageForThreadSwagger,
    ListThreadByUserSwagger,
    ReadMessageSwagger,
)
from apps.chat.api.permissions import (
    IsMessageCannotReadPermission,
    IsMessageOfTheadPermission,
    IsParticipantOfThreadPermission,
)
from apps.chat.api.serializers import (
    CreateMessageSerializer,
    CreateThreadSerializer,
    MessageSerializer,
    ThreadSerializer,
)
from apps.chat.models import Message, Thread
from apps.chat.services import ThreadService
from apps.chat.services.message import MessageService


class ThreadAPIView(GenericAPIView):
    """
    Endpoint for thread

    Method post - create thread
    """
    queryset = Thread.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        """Get serializer class"""
        if self.request.method == "POST":
            return CreateThreadSerializer

    @CreateThreadSwagger.extend_schema
    def post(self, request, *args, **kwargs):
        """Post method"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED if serializer.created else status.HTTP_200_OK)


class ThreadDetailAPIView(GenericAPIView):
    """
    Endpoint for thread detail

    delete - Delete thread
    """
    queryset = Thread.objects.all()
    permission_classes = [IsAuthenticated, IsParticipantOfThreadPermission]
    service_class = ThreadService

    @DeleteThreadSwagger.extend_schema
    def delete(self, request, *args, **kwargs):
        """Delete Method"""
        instance = self.get_object()
        self.service_class.delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(ListThreadByUserSwagger.extend_schema, name="get")
class ThreadUserAPIView(ListAPIView):
    """Receive all thread by user id"""
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]
    service_class = ThreadService

    def get_queryset(self):
        """Get queryset"""
        user_id = self.kwargs.get("user_id")
        return Thread.objects.filter(participants=user_id)


class ThreadMessageAPIViews(GenericAPIView):
    """
    Thread Message

    post - Create message for thread
    get - Receive all messsages by thread
    """
    permission_classes = [IsAuthenticated, IsParticipantOfThreadPermission]

    def get_queryset(self):
        """Get queryset"""
        queryset = Thread.objects.all()
        if self.request.method == "GET":
            queryset = queryset.prefetch_related("messages__sender")
        elif self.request.method == "POST":
            queryset = queryset.prefetch_related("participants")
        return queryset

    def get_serializer_class(self, *args, **kwargs):
        """Get serializer class"""
        if self.request.method == "POST":
            return CreateMessageSerializer
        return MessageSerializer

    @CreateMessageForThreadSwagger.extend_schema
    def post(self, request, *args, **kwargs):
        """Post method"""
        thread = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, thread=thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @GetMessageForThreadSwagger.extend_schema
    def get(self, request, *args, **kwargs):
        """Get method"""
        thread = self.get_object()
        messages = thread.messages.all()
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)


class ReadMessageApiView(GenericAPIView):
    """Mark message as read"""
    queryset = Message.objects.select_related("thread").all()
    permission_classes = [IsAuthenticated, IsMessageOfTheadPermission, IsMessageCannotReadPermission]
    service_class = MessageService

    @ReadMessageSwagger.extend_schema
    def post(self, request, *args, **kwargs):
        """Post method"""
        instance = self.get_object()
        self.service_class.read(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserMessageAPIView(ListAPIView):
    """Receive count of unread message for user"""
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self) -> QuerySet["Message"]:
        """Get queryset"""
        messages = Message.objects.filter(
            is_read=False,
            thread__in=Thread.objects.filter(participants=self.request.user).values_list("id", flat=True)
        ).exclude(sender=self.request.user)
        return messages

    @GetCountUnReadMessageSwagger.extend_schema
    def get(self, request, *args, **kwargs):
        """Get method"""
        queryset = self.get_queryset()
        return Response({"count": queryset.count()})
