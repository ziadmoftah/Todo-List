from pydantic import BaseModel



class Task(BaseModel):
    title: str
    is_completed: bool = None
    priority_id: int
    list_id: int

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
            "RIGHT JOIN todo_list.todo_list_task task "
            "ON task.id_todo_list_task = sub.id_task")
    cursor.execute(query)
    data = []
    for (task_id , task_title, subtask_title , is_completed) in cursor:
        data.append( [task_id, task_title, subtask_title,is_completed ] )
    return data

def create_tasks(connection , task_data: Task):
    cursor = connection.cursor()
    query = ("INSERT INTO `todo_list`.`todo_list_task` (`title`, `id_priority`, `id_list`) "
             "VALUES (%s, %s, %s)")
    data = (task_data.title , str(task_data.priority_id) , str(task_data.list_id))
    cursor.execute(query , data)
    connection.commit()

def get_task_data(connection, task_id : int):
    cursor = connection.cursor()
    query = ("SELECT task.title, task.is_completed, prio.name " 
            "FROM todo_list.todo_list_task task "
            "JOIN todo_list.priority prio "
            "ON task.id_priority = prio.id_priority "
             "WHERE task.id_todo_list_task = "+ str(task_id))
    cursor.execute(query)
    task_data = []
    for ( task_title, task_is_completed, task_priority) in cursor:
        task_data.append({task_title, task_is_completed, task_priority})
    return task_data