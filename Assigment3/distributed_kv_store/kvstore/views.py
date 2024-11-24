from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import KeyValue
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

def get_data(request, key):
    """
    Retrieve the value for a given key.
    """
    data = get_object_or_404(KeyValue, key=key)
    return JsonResponse({'key': data.key, 'value': data.value})


@require_http_methods(["POST", "PUT"])
@csrf_exempt
def set_data(request):
    """
    Handle create and update operations.
    - POST: Creates a new key-value pair or updates an existing one.
    - PUT: Updates the value of an existing key.
    """
    try:
        data = json.loads(request.body)
        key = data.get("key")
        value = data.get("value")

        if not key or not value:
            return JsonResponse({'error': 'Key and value are required'}, status=400)

        if request.method == "POST":
            obj, created = KeyValue.objects.update_or_create(key=key, defaults={'value': value})
            status_code = 201 if created else 200
            message = 'created' if created else 'updated'
            return JsonResponse({'key': obj.key, 'value': obj.value, 'message': f"Data {message}"}, status=status_code)

        elif request.method == "PUT":
            try:
                obj = KeyValue.objects.get(key=key)
                obj.value = value
                obj.save()
                return JsonResponse({'key': obj.key, 'value': obj.value, 'message': 'Data updated'}, status=200)
            except KeyValue.DoesNotExist:
                return JsonResponse({'error': 'Key not found for update'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
