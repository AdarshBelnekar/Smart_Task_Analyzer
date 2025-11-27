import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .circular_detection import detect_cycles

from .serializers import TaskInputSerializer, TaskOutputSerializer
from .scoring import detect_cycle, calculate_priority_for_task

class AnalyzeTasks(APIView):
 

    def post(self, request):
        payload = request.data or {}
        tasks = payload.get('tasks')
        strategy = payload.get('strategy', 'smart')
        weights = payload.get('weights')  # optional

        if not isinstance(tasks, list):
            return Response({"error": "`tasks` must be a JSON array"}, status=status.HTTP_400_BAD_REQUEST)

        
        serializer = TaskInputSerializer(data=tasks, many=True)
        try:
            serializer.is_valid(raise_exception=True)
            tasks_valid = serializer.validated_data
        except Exception as exc:
            return Response({"error": "Invalid task data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

       
        if detect_cycle(tasks_valid):
            return Response({"error": "circular dependency detected"}, status=status.HTTP_400_BAD_REQUEST)

        results = []
        for t in tasks_valid:
            score, explanation = calculate_priority_for_task(t, weights=weights, strategy=strategy)
            out = dict(t)
            out['score'] = score
            out['explanation'] = explanation
            results.append(out)

        results.sort(key=lambda x: x['score'], reverse=True)
        out_ser = TaskOutputSerializer(results, many=True)
        return Response(out_ser.data, status=status.HTTP_200_OK)


class SuggestTasks(APIView):


    def get(self, request):
        tasks_param = request.query_params.get('tasks')
        strategy = request.query_params.get('strategy', 'smart')
        weights_param = request.query_params.get('weights')  # optional JSON 

        if not tasks_param:
            return Response({"error": "provide tasks JSON in 'tasks' query parameter"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tasks = json.loads(tasks_param)
        except Exception as exc:
            return Response({"error": "invalid JSON in 'tasks' param", "details": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(tasks, list):
            return Response({"error": "'tasks' must be a JSON array"}, status=status.HTTP_400_BAD_REQUEST)

       
        weights = None
        if weights_param:
            try:
                weights = json.loads(weights_param)
            except Exception:
                weights = None

       
        serializer = TaskInputSerializer(data=tasks, many=True)
        try:
            serializer.is_valid(raise_exception=True)
            tasks_valid = serializer.validated_data
        except Exception as exc:
            return Response({"error": "Invalid task data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

      
        if detect_cycle(tasks_valid):
            return Response({"error": "circular dependency detected"}, status=status.HTTP_400_BAD_REQUEST)

        scored = []
        for t in tasks_valid:
            score, explanation = calculate_priority_for_task(t, weights=weights, strategy=strategy)
            out = dict(t)
            out['score'] = score
            out['explanation'] = explanation
            scored.append(out)

        scored.sort(key=lambda x: x['score'], reverse=True)

        
        suggestions = []
        for task in scored[:3]:
          
            suggestions.append({
                "id": task.get('id'),
                "title": task.get('title'),
                "score": task.get('score'),
                "explanation": f"Score breakdown → {task.get('explanation')}"
            })

        return Response({"suggestions": suggestions}, status=status.HTTP_200_OK)


@api_view(['POST'])
def check_cycles(request):
  
    tasks = request.data
    if not isinstance(tasks, list):
        return Response({"error": "Expected a list of tasks"}, status=400)
    
    cycles = detect_cycles(tasks)
    return Response({"cycles": cycles})