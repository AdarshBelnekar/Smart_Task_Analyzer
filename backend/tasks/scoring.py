from datetime import date
from collections import defaultdict, deque


DEFAULT_WEIGHTS = {
    'importance_w': 2.5,
    'effort_w': 1.5,       
    'urgency_w': 3.0,       
    'dependency_w': 2.0,
}

def detect_cycle(tasks):
   
    graph = defaultdict(list)
    ids = set()
    for t in tasks:
        tid = str(t.get('id', ''))
        ids.add(tid)
    for t in tasks:
        src = str(t.get('id', ''))
        for d in t.get('dependencies', []) or []:
            graph[src].append(str(d))

    visited = set()
    stack = set()

    def dfs(node):
        if node in stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        stack.add(node)
        for nbr in graph.get(node, []):
            if dfs(nbr):
                return True
        stack.remove(node)
        return False

    # check nodes that appear in graph or ids
    for node in list(ids) + list(graph.keys()):
        if dfs(node):
            return True
    return False

def compute_urgency_days(days_left):

    if days_left <= 0:
        return 30
    return max(0, 30 - days_left)

def calculate_priority_for_task(task, today=None, weights=None, strategy='smart'):

    if weights is None:
        weights = DEFAULT_WEIGHTS
    if today is None:
        today = date.today()

    
    importance = float(task.get('importance') or 5)
    est_hours = task.get('estimated_hours') if task.get('estimated_hours') is not None else 1
    try:
        est_hours = float(est_hours)
        if est_hours < 0:
            est_hours = 0.0
    except Exception:
        est_hours = 1.0

    # days_left calculation
    due = task.get('due_date')
    days_left = None
    if due:
        if isinstance(due, str):
           
            try:
                from datetime import datetime
                due_date_obj = datetime.strptime(due, "%Y-%m-%d").date()
                days_left = (due_date_obj - today).days
            except Exception:
                days_left = None
        else:
            # assume date 
            days_left = (due - today).days
    else:
        days_left = None

    # urgency conversion
    if days_left is None:
    
        urgency_days = 0
    else:
        urgency_days = compute_urgency_days(days_left)

    dep_count = len(task.get('dependencies') or [])

    
    effort_base = max(0.0, min(10.0, 10.0 - est_hours))

   
    if strategy == 'fastest':
      
        score = (effort_base * (weights['effort_w'] * 2)) + (importance * weights['importance_w'] * 0.5) + (urgency_days * weights['urgency_w'] * 0.2) + (dep_count * weights['dependency_w'])
    elif strategy == 'high_impact':
        score = (importance * weights['importance_w'] * 2.0) + (effort_base * weights['effort_w'] * 0.3) + (urgency_days * weights['urgency_w'] * 0.2) + (dep_count * weights['dependency_w'])
    elif strategy == 'deadline':
        score = (urgency_days * weights['urgency_w'] * 2.0) + (importance * weights['importance_w'] * 0.5) + (effort_base * weights['effort_w'] * 0.3) + (dep_count * weights['dependency_w'])
    else: 
        score = (importance * weights['importance_w']) + (effort_base * weights['effort_w']) + (urgency_days * weights['urgency_w']) + (dep_count * weights['dependency_w'])

  
    explanation_parts = [
        f"importance={importance}*{weights['importance_w']}",
        f"effort_base={effort_base}*{weights['effort_w']}",
        f"urgency_days={urgency_days}*{weights['urgency_w']}",
        f"deps={dep_count}*{weights['dependency_w']}"
    ]
    explanation = "; ".join(explanation_parts)
    return round(float(score), 2), explanation
