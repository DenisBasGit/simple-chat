from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests.chat.factory import MessageFactory
from tests.chat.factory.thread import ThreadFactory
from tests.users.factory import UserFactory


class TestCreateThread(APITestCase):
    """Test Create thread"""

    def setUp(self) -> None:
        """Set up method"""
        self.url = reverse("api:chat_app:thread")
        self.user = UserFactory()

    def test_url(self):
        """Test url"""
        url = "/api/v1/chat/thread/"
        response = self.client.post(self.url)
        self.assertEqual(url, self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_not_authenticated(self):
        """Test not authenticated"""
        data = {
            "participant": UserFactory().id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_thread(self):
        """Test create thread"""
        data = {"participant": UserFactory().id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_thread_with_exists_participant(self):
        """Test create thread with exists participant"""
        participant = UserFactory()
        thread = ThreadFactory.create(participants=[self.user, participant])
        data = {"participant": participant.id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], thread.id)


class TestListThreadByUser(APITestCase):
    """Test list thread by user"""
    def setUp(self) -> None:
        """Set up"""
        self.user = UserFactory()
        self.threads = ThreadFactory.create_batch(10, participants=[self.user, UserFactory()])
        self.url = reverse("api:chat_app:thread_user", kwargs={"user_id": self.user.id})

    def test_url(self):
        """Test url"""
        url = "/api/v1/chat/thread/user/%s/" % self.user.id
        response = self.client.get(self.url)
        self.assertEqual(url, self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_not_authenticated(self):
        """Test not authenticated"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_of_thread_by_user(self):
        """Test get list of thread by user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)


class TestCreateMessage(APITestCase):
    """Test create message"""
    def setUp(self) -> None:
        """Set up"""
        self.user = UserFactory()
        self.thread = ThreadFactory.create(participants=[self.user, UserFactory()])
        self.url = reverse("api:chat_app:message", kwargs={"pk": self.thread.pk})

    def test_url(self):
        """Test url"""
        url = "/api/v1/chat/thread/%s/message/" % self.user.id
        response = self.client.post(self.url)
        self.assertEqual(url, self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_not_authenticated(self):
        """Test not authenticated"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_participant_of_thread(self):
        """Test not participant of thread"""
        self.client.force_authenticate(user=UserFactory())
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_thread_not_exists(self):
        """Test thread not exists"""
        url = "/api/v1/chat/thread/%s/message/" % 0
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_message_empty_data(self):
        """Test create message empty data"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_message_success(self):
        """Test create message success"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data={"text": "test"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestListMessagesForThread(APITestCase):
    """Test list message for thread"""

    def setUp(self) -> None:
        """Set up"""
        self.user = UserFactory()
        self.thread = ThreadFactory.create(participants=[self.user, UserFactory()])
        MessageFactory.create_batch(10, thread=self.thread)
        self.url = reverse("api:chat_app:message", kwargs={"pk": self.thread.pk})

    def test_url(self):
        """Test url"""
        url = "/api/v1/chat/thread/%s/message/" % self.user.id
        response = self.client.get(self.url)
        self.assertEqual(url, self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_not_authenticated(self):
        """Test not authenticated"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_participant_of_thread(self):
        """Test not participant of thread"""
        self.client.force_authenticate(user=UserFactory())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_thread_not_exists(self):
        """Test thread not exists"""
        url = "/api/v1/chat/thread/%s/message/" % 0
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_message_success(self):
        """Test get message success"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)


class TestReadMessage(APITestCase):
    """Test read message"""

    def setUp(self) -> None:
        """Set up"""
        self.user = UserFactory()
        self.participant = UserFactory()
        self.thread = ThreadFactory.create(participants=[self.user, self.participant])
        self.message = MessageFactory.create(thread=self.thread, sender=self.participant)
        self.url = reverse("api:chat_app:message_read", kwargs={"pk": self.message.pk})

    def test_url(self):
        """Test url"""
        url = "/api/v1/chat/message/%s/read/" % self.message.id
        response = self.client.post(self.url)
        self.assertEqual(url, self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_not_authenticated(self):
        """Test not authenticated"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_participant_of_thread(self):
        """Test not participant of thread"""
        self.client.force_authenticate(user=UserFactory())
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_read_own_message(self):
        """Test cannot read own message"""
        self.client.force_authenticate(user=self.participant)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_message_not_exists(self):
        """Test message not exists"""
        url = "/api/v1/chat/thread/%s/message/" % 0
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_message_success(self):
        """Test read message sucess"""
        self.client.force_authenticate(user=self.user)
        self.assertFalse(self.message.is_read)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)


class TestCountUnreadMessage(APITestCase):
    """Test count unread message"""

    def setUp(self) -> None:
        """Set up"""
        self.user = UserFactory()
        self.participant = UserFactory()
        self.thread = ThreadFactory.create(participants=[self.user, self.participant])
        MessageFactory.create_batch(10, thread=self.thread, sender=self.participant)
        self.url = reverse("api:chat_app:message_user")

    def test_url(self):
        """Test url"""
        url = "/api/v1/chat/message/user/unread/"
        response = self.client.get(self.url)
        self.assertEqual(url, self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_not_authenticated(self):
        """Test not authenticated"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_count_unread_message_success(self):
        """Test count unread message"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)
