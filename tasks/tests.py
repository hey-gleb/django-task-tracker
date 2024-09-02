# from django.contrib.auth.models import User, Group
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from .models import Project, Task
#
# class TaskTests(APITestCase):
#
#     def setUp(self):
#         self.manager_group, _ = Group.objects.get_or_create(name='Manager')
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.user.groups.add(self.manager_group)
#
#         self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')
#
#         # Simulate login to establish a session
#         self.client.login(username='testuser', password='testpassword')
#
#         # Create a project where the user is a member
#         self.project = Project.objects.create(title='Test Project', user=self.user)
#
#         # Create a task associated with the project
#         self.task = Task.objects.create(
#             title='Test Task',
#             description='This is a test task.',
#             project=self.project,
#             created_by=self.user,
#         )
#
#         # Define URLs for testing
#         self.list_create_url = reverse('task-list-create')
#         self.detail_url = reverse('task-detail', kwargs={'pk': self.task.id})
#
#     def test_create_task(self):
#         # Define the data for the new task
#         data = {
#             'title': 'New Task',
#             'description': 'This is a new task.',
#             'project': self.project.id,
#             'created_by': self.user.id
#         }
#
#         # Send a POST request to create a new task
#         response = self.client.post(self.list_create_url, data, format='json')
#
#         # Verify that the task was created successfully
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Task.objects.count(), 2)  # There should now be 2 tasks
#
#     def test_list_tasks(self):
#         # Send a GET request to retrieve the list of tasks
#         response = self.client.get(self.list_create_url)
#
#         # Verify that the response is successful and contains 1 task
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 1)
#
#     def test_retrieve_task(self):
#         # Send a GET request to retrieve the task details
#         response = self.client.get(self.detail_url)
#
#         # Verify that the response is successful and contains the correct task data
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['title'], 'Test Task')
#
#     def test_update_task(self):
#         # Define the updated data for the task
#         data = {
#             'title': 'Updated Task Name',
#         }
#
#         # Send a PUT request to update the task
#         response = self.client.put(self.detail_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.task.refresh_from_db()
#         self.assertEqual(self.task.name, 'Updated Task Name')
#         self.assertEqual(self.task.description, 'This is an updated description.')
#
#     def test_delete_task(self):
#         # Send a DELETE request to delete the task
#         response = self.client.delete(self.detail_url)
#
#         # Verify that the task was deleted successfully
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Task.objects.count(), 0)  # There should be no tasks left
#
#     def test_non_member_cannot_create_task(self):
#         # Simulate login as a non-manager user who is not a member of the project
#         self.client.logout()
#         self.client.login(username='otheruser', password='otherpassword')
#
#         # Attempt to create a task in a project where the user is not a member
#         data = {
#             'title': 'Task by non-member',
#             'description': 'This task should not be created.',
#         }
#
#         # Send a POST request to create a new task
#         response = self.client.post(self.list_create_url, data, format='json')
#
#         # Verify that the task was not created (forbidden)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(Task.objects.count(), 1)  # There should still be only 1 task
