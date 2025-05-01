from pydantic import BaseModel

class Subtask(BaseModel):
    task_id : int
    title: str
    is_completed: bool = None


def get_subtask_date(connection, subtask_id):
    cursor = connection.cursor()
    query = ("SELECT title, is_completed "
    "FROM todo_list.subtask "
    "WHERE id_subtask =" + str(subtask_id))
    cursor.execute(query)
    data = []
    for (title, is_completed) in cursor:
        data.append([title, is_completed])
    return data

def create_subtasks(connection, subtask_data ):
    cursor = connection.cursor()
    query = ("INSERT INTO todo_list.subtask (`id_task`, `title`) "
             "VALUES (%s, %s)" )
    data = []
    for (task_id, subtask_title) in subtask_data:
        data.append((str(task_id) , subtask_title))
    print(data)
    cursor.executemany(query, data)
    connection.commit()

# to be implemented
def edit_subtask(connection , subtask_data ,subtask_id):
    cursor = connection.cursor()
    query = ("UPDATE todo_list.subtask "
             "SET `title` = "+ subtask_data.title +
             " WHERE (`id_subtask` = " + str(subtask_id) +")")


def delete_subtask(connection , subtask_id):
    cursor = connection.cursor()
    query = ("DELETE FROM todo_list.subtask "
             "WHERE id_subtask = "+ str(subtask_id))
    cursor.execute(query)
    connection.commit()

def delete_all_subtask_of_task_id(connection, task_id):
    cursor = connection.cursor()
    query = ("DELETE FROM todo_list.subtask "
             "WHERE id_task = " + str(task_id))
    cursor.execute(query)
    connection.commit()
