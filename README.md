# Person and Object Detector


## Team Member

**Cloud Computing Path:**
- Ilham Dirgantara L.P.

**Machine Learning Path:**
- Ronaldyanto
- Zeindea Amanda
- Stela Marisa


## Running the Web Application Locally

To run this web application on your local computer, follow the steps below:

1. Ensure that Python is installed on your machine.

2. Switch to the 'web-local' branch and clone it to your local directory:
  ```
  git clone -b web-local https://github.com/c23-it02/capstone-project.git
  ```
3. Navigate to the 'capstone-project' directory.
```
cd capstone-project
```
4. Install the virtual environment by running the following command:
```
py -m pip install virtualenv
py -m venv venv
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
7. Because the memory tray model size is very large (+-200MB), it is not stored on GitHub. To download it, you can use the following link:
model_HDD.h5
```
https://drive.google.com/file/d/17iXiilrIyDivtYKWhlJne2K2k0l-Bj0_/view?usp=sharing
```
model_SSD.h5:
```
https://drive.google.com/file/d/1CZO73P0nI_-9aLtcGtqmgoNvgV2HF4nH/view?usp=drive_link
```
8. Save the model_HDD.h5 and model_SSD.h5 file to the directory capstone-project/memory_tray_detector/ml_models/.

9. Make sure that the command prompt (CMD) is in the capstone-project directory.

10. Start the server by running the following command:
```
py manage.py runserver
```



Now, you can access the web application locally by opening your web browser and entering the appropriate URL.


