

def detect_cycles(tasks):
    graph = {task['id']: task.get('dependencies', []) for task in tasks}
    visited = set()
    rec_stack = set()
    cycles = []

    def dfs(node, path):
        if node not in graph:
            return
        if node in rec_stack:
            cycle_start_index = path.index(node)
            cycles.append(path[cycle_start_index:])
            return
        if node in visited:
            return

        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        for neighbor in graph.get(node, []):
            dfs(neighbor, path.copy())
        rec_stack.remove(node)

    for task_id in graph:
        dfs(task_id, [])

    return cycles
