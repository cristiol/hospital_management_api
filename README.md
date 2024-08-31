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

