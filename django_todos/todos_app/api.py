import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Todo


class BaseCSRFExemptView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TodoListView(BaseCSRFExemptView):
    def get(self, request):
        
        filter_type = request.GET.get('status')

        if filter_type == 'active':
            model_list = Todo.objects.filter(completed=False)
            
        elif filter_type == 'completed':
            model_list = Todo.objects.filter(completed=True)
            
        else:
            filter_type = 'all'
            model_list = Todo.objects.all()
        
        results = []
        
        for model in model_list:
            appendable = {
                'id': model.id,
                'title': model.title,
                'completed': model.completed
            }
            
            results.append(appendable)
        
        resp = {
            'filter': filter_type,
            'count': len(model_list),
            'results': results
        }
        
        return JsonResponse(resp)

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        if not data:
            return HttpResponse(status=400)
        
        if 'completed' in data:
            result = Todo.objects.create(title=data["title"], completed=data['completed'])
        else:
            result = Todo.objects.create(title=data['title'])
        
        return JsonResponse('', status=201, safe=False)

class TodoDetailView(BaseCSRFExemptView):
    def get(self, request, todo_id):
        
        try:
        
            model = Todo.objects.get(id=todo_id)
        
            resp = {
                'id': model.id,
                'title': model.title,
                'completed': model.completed
            }
            
            return JsonResponse(resp, safe=False)
        
        except Todo.DoesNotExist:
            return HttpResponse(status=404)
            
        
    #Don't do it this way it's ugly. ewwwww    But it works 
    '''
    def get(self, request, todo_id):
        
        if Todo.objects.filter(id=todo_id).count() != 0: 
            model = Todo.objects.get(id=todo_id)
            
            resp = {
                'id': model.id,
                'title': model.title,
                'completed': model.completed
            }
            
            return JsonResponse(resp, safe=False)
            
        else:
            return HttpResponse(status=404)
    '''

    def delete(self, request, todo_id):
        try:
            model = Todo.objects.get(id=todo_id)
            model.delete()
        
            return HttpResponse(status=204)
            
        except Todo.DoesNotExist:
            return HttpResponse(status=404)

    def patch(self, request, todo_id):
                
        data = json.loads(request.body.decode('utf-8'))
        if not data:
            return HttpResponse(status=400)

        try:
                        
            model = Todo.objects.get(id=todo_id)
            
            if 'title' in data:
                model.title = data['title']
    
            if 'completed' in data:
                model.completed = data['completed']
                
            if 'action' in data:
                if model.completed == True:
                    model.completed = False
                elif model.completed == False:
                    model.completed = True
            
            model.save()
                
            return HttpResponse('', status=204)
        
        except Todo.DoesNotExist:
            return HttpResponse(status=404)
            

    def put(self, request, todo_id):
        
        data = json.loads(request.body.decode('utf-8'))
        if not data:
            return HttpResponse(status=400)

        try:
                        
            model = Todo.objects.get(id=todo_id)
            
            if 'completed' not in data:
                return JsonResponse({'error': 'Missing argument: completed'}, status=400)
            
            if 'title' not in data:
                return JsonResponse({'error': 'Missing argument: title'}, status=400)
            
            model.title = data['title']
            model.completed = data['completed']
            
            model.save()
                
            return HttpResponse('', status=204)
        
        except Todo.DoesNotExist:
            return HttpResponse(status=404)
            
        