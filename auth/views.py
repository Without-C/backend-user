import json
from django.http import JsonResponse

def test_view(request):
    if request.method == 'GET':
        return JsonResponse({
            'message': 'get test',
            'status': 'success'
        })

    elif request.method == 'POST':
        try:
            received_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        return JsonResponse({
            'message': 'post test',
            'data_received': received_data,
            'status': 'success'
        })

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
