# ToDo API: testing assignment.
A compact webservice to create and manage tasks.
Built with Django REST Framework, with PostgreSQL support and JWT authorization.

## 1) Features
- register and browse the list of available tasks;

- create and manage new tasks, with an option to assign them to another user;

- only the creator may assign permissions to read/update the task;

- only the creator may delete an existing task.

## 2) Installation

1) Download the package from GitHub:

    ```bash
    git clone git@github.com:Mirrasol/ToDo-API.git
    ```

2) Install using uv from your console:

    ```bash
    make install
    ```

    or set your own virtual environment using pip and other package managers.

3) Don't forget to create the '.env' file that contains your secret keys and database settings: 
 - Please refer to the '.env_example' file

4) Apply initial migration:

    ```bash
    uv run python manage.py migrate
    ```

5) Optionally, create superuser 'admin' with the password:

    ```bash
    uv run python manage.py createsuperuser --username admin --email admin@example.com
    ```

6) Run the project with a command:

    ```bash
    make run
    ```

7) If you wish to use a DRF browsable API, uncomment the following line in the 'settings.py':
    ```
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': [
            ...
            'rest_framework.renderers.BrowsableAPIRenderer',
    ```

## 3) Available endpoints

New users:

`POST`: `api/create-user/` - register a new user

Registered users:

`POST`: `api/token/` - issue a pair of access tokens (short- and long-lived)

`POST`: `api/token/refresh/` - use a long-lived access token to issue a new short-lived one

`GET`: `api/task/` - browse the list of created tasks

`POST`: `api/task/` - create a new task

`GET`: `api/task/{id}` - read an existing task (creator or assigned executor only)

`PUT`/`PATCH`: `api/task/{id}` - update an existing task (creator or assigned executor only)

`DELETE`: `api/task/{id}` - delete an existing task (creator only)
