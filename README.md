# azure-ad-react-python-app
Implement SSO in ReactJs and Python applications.

# For Application Setup
-  Clone this repository in the local system
``` https://github.com/darjidhruv26/azure-ad-react-python-app.git ```

## Strt Frontend ReactJs Application
- Go to Frontend directory

  `cd frontend`
  
- Install all required packages by using this command

  `npm install`

- Start the Application by using this command

  `npm start`

  ## Start Backend Python Application
- Go to the Backend directory

 `cd backend`

- Create Virtual Environment

 `python -m venv venv`

- Activate the Virtual Environment
  
 `.\venv\Scripts\activate`

-  Install all dependencies for this application

 `pip install -r requirements.txt`

- Make Migrations for `authapp`(this will generate the migration files for your models)

 `python manage.py makemigrations authapp`

- Apply Migrations (this will create the database tables based on the migration files)

 `python manage.py migrate`

- Run the Server

 `python manage.py runserver`

  
