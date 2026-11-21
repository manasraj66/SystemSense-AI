from .collector_service import list_processes
def get_process_table(limit=100):
    return list_processes(limit)
