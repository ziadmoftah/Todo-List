

def get_all_todo_list_data(connection, list_id ):
    cursor = connection.cursor()
    query = ("SELECT lis.title list_title, prio1.name list_priority, tas.title task_title, prio2.name task_priority, tas.is_completed task_status , "
             "sub.title subtask_title, sub.is_completed subtask_status "
             "JOIN todo_list.todo_list_task tas "
             "ON lis.id_todo_list = tas.id_list "
             "JOIN todo_list.subtask sub "
             "ON sub.id_task = tas.id_todo_list_task "
             "JOIN todo_list.priority prio1 "
             "ON lis.id_priority = prio1.id_priority "
             "JOIN todo_list.priority prio2 "
             "ON tas.id_priority = prio2.id_priority "
             "Where lis.id_todo_list = " + str(list_id) )
    cursor.execute(query)
    data= []
    for (list_title, list_priority, task_title, task_priority, task_is_completed, subtask_title, subtask_is_completed) in cursor:
        data.append([list_title, list_priority, task_title, task_priority, task_is_completed, subtask_title, subtask_is_completed])
    return data