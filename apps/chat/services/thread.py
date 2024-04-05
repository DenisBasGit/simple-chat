from typing import TYPE_CHECKING, Tuple

from django.db import transaction

from apps.chat.models import Thread, ThreadUserRelation

if TYPE_CHECKING:
    from django.contrib.auth.models import User


class ThreadService:

    @classmethod
    def _create(cls) -> Thread:
        """
        Main Create thread

        Return:
            thread: Thread
        """

        return Thread.objects.create()

    @classmethod
    @transaction.atomic
    def create(cls, participant: "User", user: "User") -> Tuple[Thread, bool]:
        """
        Create thread

        Args:
            participant: User
            user: User

        Return:
            Tuple(Thread, bool)
        """
        thread = cls.get_one_thread_with_participant(user, participant)
        created = False
        if thread is None:
            created = True
            thread = cls._create()
            cls._add_participant(thread, participant)
            cls._add_participant(thread, user)
        return thread, created

    @classmethod
    def delete(cls, thread: Thread):
        """Delete thread"""
        thread.delete()

    @classmethod
    def _add_participant(cls, thread: Thread, participant: "User"):
        """
        Add participant to thread

        Args:
            thread: Thread
            participant: User
        """
        ThreadUserRelation.objects.create(thread=thread, user=participant)

    @classmethod
    def get_one_thread_with_participant(cls, user: "User", participant: "User"):
        """
        Get one with participant

        Args:
            user: User
            participant: User
        """
        return Thread.objects.filter(
            id__in=ThreadUserRelation.objects.filter(user=participant).values("thread"),
            participants=user
        ).distinct().first()

    @classmethod
    def is_participant_of_thread(cls, thread: Thread, user: "User") -> bool:
        """
        Is participant of thread

        Args:
            thread: Thread
            user: User

        Return:
            bool
        """
        return thread.participants.filter(id=user.id).exists()
