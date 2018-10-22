import connexion
import six

from swagger_server.models.completed_task import CompletedTask  # noqa: E501
from swagger_server.models.task import Task  # noqa: E501
from swagger_server.models.todo_list import TodoList  # noqa: E501
from swagger_server import util


def add_list(todoList=None):  # noqa: E501
    """creates a new list

    Adds a list to the system # noqa: E501

    :param todoList: ToDo list to add
    :type todoList: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        todoList = TodoList.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def add_task(id, task=None):  # noqa: E501
    """add a new task to the todo list

     # noqa: E501

    :param id: Unique identifier of the list to add the task for
    :type id: dict | bytes
    :param task: task to add
    :type task: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        id = .from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        task = Task.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_list(id):  # noqa: E501
    """return the specified todo list

     # noqa: E501

    :param id: The unique identifier of the list
    :type id: dict | bytes

    :rtype: TodoList
    """
    if connexion.request.is_json:
        id = .from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def put_task(id, taskId, task=None):  # noqa: E501
    """updates the completed state of a task

     # noqa: E501

    :param id: Unique identifier of the list to add the task for
    :type id: dict | bytes
    :param taskId: Unique identifier task to complete
    :type taskId: dict | bytes
    :param task: task to add
    :type task: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        id = .from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        taskId = .from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        task = CompletedTask.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def search_lists(searchString=None, skip=None, limit=None):  # noqa: E501
    """returns all of the available lists

    Searches the todo lists that are available  # noqa: E501

    :param searchString: pass an optional search string for looking up a list
    :type searchString: str
    :param skip: number of records to skip for pagination
    :type skip: int
    :param limit: maximum number of records to return
    :type limit: int

    :rtype: List[TodoList]
    """
    return 'do some magic!'
