# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.completed_task import CompletedTask  # noqa: E501
from swagger_server.models.task import Task  # noqa: E501
from swagger_server.models.todo_list import TodoList  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTodoController(BaseTestCase):
    """TodoController integration test stubs"""

    def test_add_list(self):
        """Test case for add_list

        creates a new list
        """
        todoList = TodoList()
        response = self.client.open(
            '/aweiker/ToDo/1.0.0/lists',
            method='POST',
            data=json.dumps(todoList),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_task(self):
        """Test case for add_task

        add a new task to the todo list
        """
        task = Task()
        response = self.client.open(
            '/aweiker/ToDo/1.0.0/list/{id}/tasks'.format(id='id_example'),
            method='POST',
            data=json.dumps(task),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_list(self):
        """Test case for get_list

        return the specified todo list
        """
        response = self.client.open(
            '/aweiker/ToDo/1.0.0/list/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_task(self):
        """Test case for put_task

        updates the completed state of a task
        """
        task = CompletedTask()
        response = self.client.open(
            '/aweiker/ToDo/1.0.0/list/{id}/task/{taskId}/complete'.format(id='id_example', taskId='taskId_example'),
            method='POST',
            data=json.dumps(task),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_lists(self):
        """Test case for search_lists

        returns all of the available lists
        """
        query_string = [('searchString', 'searchString_example'),
                        ('skip', 1),
                        ('limit', 50)]
        response = self.client.open(
            '/aweiker/ToDo/1.0.0/lists',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
