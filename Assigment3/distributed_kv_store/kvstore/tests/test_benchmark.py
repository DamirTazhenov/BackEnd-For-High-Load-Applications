# kvstore/tests/test_benchmark.py
import pytest
from django.utils import timezone
from kvstore.models import KeyValue


@pytest.mark.django_db
def test_read_performance():
    start_time = timezone.now()
    for _ in range(1000):
        KeyValue.objects.all().first()  # Read operation
    duration = timezone.now() - start_time
    print(f"Read operations took {duration.total_seconds()} seconds")
    assert duration.total_seconds() < 10  # Set a threshold, e.g., < 10 seconds
