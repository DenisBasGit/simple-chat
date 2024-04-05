import unittest

from apps.chat.api.serializers import CreateThreadSerializer, ThreadSerializer
from tests.chat.factory import ThreadFactory
from tests.users.factory import UserFactory


class CreateThreadSerializerTestCase(unittest.TestCase):
    """Create thread serializer test case"""
    def setUp(self) -> None:
        """Set up"""
        self.serializer = CreateThreadSerializer

    def test_serializer_with_empty_data(self) -> None:
        """Test serializer with empty data"""
        serializer = self.serializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors.keys()), ["participant"])

    def test_serializer_with_not_exists_participant(self) -> None:
        """Test serializer with not exists participant"""
        serializer = self.serializer(data={
            "participant": 0
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors.keys()), ["participant"])

    def test_serializer_with_correct_data_write(self) -> None:
        """Test serializer with correct data on write"""
        serializer = self.serializer(data={"participant": UserFactory().id})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(list(serializer.validated_data.keys()), ["participant"])

    def test_serializer_with_correct_data_read(self) -> None:
        """Test serializer with correct data on read"""
        serializer = self.serializer(UserFactory())
        self.assertEqual(list(serializer.data.keys()), ["id"])


class ListThreadSerializerTestCase(unittest.TestCase):
    """List thread serializer test case"""

    def setUp(self) -> None:
        """Set  up"""
        self.serializer = ThreadSerializer

    def test_serializer_check_fields(self) -> None:
        """Test serializer check fields"""
        thread = ThreadFactory()
        serializer = self.serializer(thread)
        self.assertEqual(list(serializer.data.keys()), ["id", "created", "updated", "participants"])
