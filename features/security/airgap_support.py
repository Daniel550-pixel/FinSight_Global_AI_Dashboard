EXTERNAL_CALLS_ENABLED = False
def execute_local(task):
    if EXTERNAL_CALLS_ENABLED:
        raise Exception('Air-gapped mode: external calls forbidden')
    return f'Executed {task} locally'
