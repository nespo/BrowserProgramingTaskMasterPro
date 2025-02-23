import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from .models import Task

def index(request):
    """Render the main page."""
    return render(request, 'tasks/index.html')

@require_http_methods(["GET", "POST"])
def tasks_api(request):
    """
    GET: List tasks with optional filtering, searching, and sorting.
    POST: Create a new task.
    """
    if request.method == "GET":
        tasks = Task.objects.all()
        # Filter by status if provided (e.g., pending, completed)
        status_filter = request.GET.get('status')
        if status_filter:
            tasks = tasks.filter(status=status_filter)
        # Search by title if provided
        search_query = request.GET.get('search')
        if search_query:
            tasks = tasks.filter(title__icontains=search_query)
        # Sort by field if provided (only allow safe fields)
        sort_by = request.GET.get('sort')
        if sort_by in ['due_date', 'title']:
            tasks = tasks.order_by(sort_by)
        tasks = list(tasks.values())
        return JsonResponse(tasks, safe=False)
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            task = Task.objects.create(
                title=data.get('title', ''),
                description=data.get('description', ''),
                status=data.get('status', 'pending'),
                due_date=data.get('due_date', None)
            )
            response = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'due_date': task.due_date
            }
            return JsonResponse(response, status=201)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

@require_http_methods(["PUT", "DELETE"])
def task_api(request, pk):
    """
    PUT: Update a specific task.
    DELETE: Delete a specific task.
    """
    task = get_object_or_404(Task, pk=pk)
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.status = data.get('status', task.status)
            task.due_date = data.get('due_date', task.due_date)
            task.save()
            response = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'due_date': task.due_date
            }
            return JsonResponse(response)
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    elif request.method == "DELETE":
        task.delete()
        return JsonResponse({'result': 'Task deleted'})
