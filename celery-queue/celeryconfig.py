result_expires = 3600
task_create_missing_queues = True
task_routes = {
    "tasks.upload": {"queue": "upload"},
    "tasks.profile": {"queue": "profile"},
}
