import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """This fixture applies @pytest.mark.django_db to each test"""
