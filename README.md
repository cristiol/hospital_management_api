# Hospital management api - Django rest framework 
This Django REST Framework application aims to efficiently manage a hospital by providing functionalities such as scheduling appointments, managing patient records, and generating medical reports.

## Personal Motivation
I built this project from scratch with the purpose of grasping a good understanding of the Django Rest Framework and its integration with technologies like Postgres, Celery, and RabbitMQ.

## Features

- **CRUD operations for users**: Doctors, assistants, and patients can be created, updated, and deleted.
- **JWT Authentication**: Secure authentication using JSON Web Tokens.
- **Role-Based Access Control**: Different levels of access based on user roles (e.g., doctors, patients, admins).
- **Specific permission**: For example, only an assigned doctor can update recommended treatment for a patient.
- **Appointments system**: A patient can make an appointment with a specific doctor, and the doctor and the patient receive an automated confirmation mail.
- **Reports**: designated enpoints for generating reports

## Technologies Used

- **Django REST Framework**: For API development, model management and APITestCases for unit and API testing.
- **PostgreSQL**: As the relational database for data storage
- **Celery and RabbitMQ**: For asynchronous task processing (e.g., sending emails).
- **Insomnia**: Real-time testing of API endpoints.
- **Docker**: For containerization and deployment of the application, providing a consistent and isolated environment.

## Arhitecture Diagram

![image](https://github.com/user-attachments/assets/3cbe14f8-2ded-4972-b559-87ed9569923c)

## Instalation 

### Prerequisites

- **Python**: The version specified in the requirements.txt file. It is recommended to use a Python version manager like pyenv to manage different Python versions.
- **A Python package manager**: pip is the most common, but you can also use others like poetry.
- **A text editor or an IDE**: Popular options include Visual Studio Code, PyCharm, Sublime Text.
-  **A terminal or command line**: To run installation and project management commands.
-  **Docker**: Required for running the project in a containerized environment.

### Installation and Setup

Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/cristiol/hospital_management_api.git

2. **Navigate to the Project Directory**:
   ```bash
   cd hospital_management_api

3. **Set up the email**
  - Create a .env file in the root of the project directory if it doesn't already exist.
  - Add your email address and other required email settings to the .env file.
  - If you are using a different email service provider than Outlook, make sure to update the EMAIL_HOST setting. For example, if you are using Gmail, you should change it to:
  ```
  EMAIL_HOST='smtp.gmail.com'
  ```

4. **Build and Run the Docker Containers**:
   ```bash
   docker-compose up --build

5. **Access the API**:
Once the Docker containers are running, the API will be accessible at http://localhost:8000.

6. **Access the RabbitMQ Management UI**: You can access the RabbitMQ Management UI at http://localhost:15672 using the credentials:
     ```
     Username: admin
     Password: admin
     ```
## Endpoints

**users/**

![image](https://github.com/user-attachments/assets/ba05c9c8-e00c-4bd8-bc23-1d76ef7948c1)

**doctors/**

![image](https://github.com/user-attachments/assets/e230de4d-06be-4bc6-86fb-9117f52a5911)

**assistants/**

![image](https://github.com/user-attachments/assets/d20f434b-4d80-4586-a7ad-39255a9a7a45)

**treatments/**

![image](https://github.com/user-attachments/assets/5f8142d2-a62c-4d4b-9090-bb9c8ecfccd6)

**patients/**

![image](https://github.com/user-attachments/assets/970730ec-8e84-41c9-82da-e3ef439d8398)

**reports/**

![image](https://github.com/user-attachments/assets/7fce7113-0412-45ea-999c-46c5347e93b6)

**appointments/**

![image](https://github.com/user-attachments/assets/166dd303-2e5b-4d6b-acbf-41808a27f0d7)

**Usage**

To interact with the API, use tools like Insomnia or Postman. Below are some example requests:

**Authentication**

Obtain a JWT token by sending a POST request with your credentials.

![image](https://github.com/user-attachments/assets/e087884a-2bee-4fb0-a454-e513967ae38b)

**CRUD Operations**

**Get All Patients**:

![image](https://github.com/user-attachments/assets/6029b1f0-ea61-4844-9bfb-16ac4a0ec59e)

**Create a new patient**

![image](https://github.com/user-attachments/assets/9a3061a3-7edf-4155-80a1-0dd210cf8281)

**Read a patient**

![image](https://github.com/user-attachments/assets/891cd4a9-c273-4165-91fe-17ac83ebc421)

**Update a patient**

![image](https://github.com/user-attachments/assets/2882f8f3-aabe-4f84-b706-be51ac342410)

**Delete a patient**

![image](https://github.com/user-attachments/assets/d82d4482-ac4c-4aad-b9f8-e2be376a8094)

# Testing

The API has a test suite implemented containing unit tests. You can check tests by doing:
```
$ docker-compose exec web python manage.py test
```
# Contributing

**How to Contribute**: You can contribute by forking the repository, making your changes on a new branch, and submitting a pull request.

**Code Conventions**: Follow PEP 8 for Python code. Use clear commit messages and add docstrings for all functions and classes.

# License

**License**: This project is licensed under the MIT License.

# Authors

Cristian Olteanu (Project Lead)
