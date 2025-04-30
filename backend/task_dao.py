

def get_task_subtask_data(connection, task_id):
    cursor = connection.cursor()
    query = ("SELECT sub.title, sub.is_completed "
            "FROM todo_list.subtask sub "
            "JOIN todo_list.todo_list_task task "
            "ON task.id_todo_list_task = sub.id_task "
            "WHERE  sub.id_task = " + str(task_id))
    cursor.execute(query)
    data = []
    for (title , is_completed) in cursor:
        data.append([title,is_completed])
    return data


def get_all_task_subtask_data(connection):
    cursor = connection.cursor()
    query = ("SELECT  task.id_todo_list_task, task.title ,sub.title, sub.is_completed "
            "FROM todo_list.subtask sub "
            "JOIN todo_list.todo_list_task task "
            "ON task.id_todo_list_task = sub.id_task")
    cursor.execute(query)
    data = []
    for (task_id , task_title, subtask_title , is_completed) in cursor:
        data.append( [task_id, task_title, subtask_title,is_completed ] )
    return data
