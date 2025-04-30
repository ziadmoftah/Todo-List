

def get_all_todo_list_data(connection ):
    cursor = connection.cursor()
    query = ("SELECT lis.title, lis.order, prio1.name, tas.title, tas.order, prio2.name, tas.is_completed, sub.title, sub.is_completed  FROM todo_list.todo_list lis "
            "JOIN todo_list.todo_list_task tas "
            "ON lis.id_todo_list = tas.id_list "
            "JOIN todo_list.subtask sub "
            "ON sub.id_task = tas.id_todo_list_task "
            "JOIN todo_list.priority prio1 "
            "ON lis.id_priority = prio1.id_priority "
            "JOIN todo_list.priority prio2 "
            "ON tas.id_priority = prio2.id_priority ")
    cursor.execute(query)
    data= []
    for (list_title, list_order, list_priority, task_title, task_order, task_priority, task_is_completed, subtask_title, subtask_is_completed) in cursor:
        data.append([list_title, list_order, list_priority, task_title, task_order, task_priority, task_is_completed, subtask_title, subtask_is_completed])
    return data