# capstone-project

## Running the Web Application Locally

To run this web application on your local computer, follow the steps below:

1. Ensure that Python is installed on your machine.

2. Switch to the 'web-local' branch and clone it to your local directory:
  ```
  git clone -b web-local https://github.com/c23-it02/capstone-project.git
  ```
3. Navigate to the 'capstone-project' directory.

4. Install the virtual environment by running the following command:
```
python -m venv venv 
```
5. Activate the virtual environment:

- For Windows:

  ```
  venv\Scripts\activate
  ```

- For macOS and Linux:

  ```
  source venv/bin/activate
  ```

6. Install the dependencies listed in the 'requirements.txt' file:
```
pip install -r requirements.txt
```
7. Navigate to the 'mywebsite' directory.

8. Start the server by running the following command:
```
python manage.py runserver
```



Now, you can access the web application locally by opening your web browser and entering the appropriate URL.


