# Clone Repository

- <b>HTTPS</b>

  ```git
  git clone https://gitlab.com/bucal/bucal-bms.git
  ```

- <b>SSH</b>

  ```git
  git clone git@gitlab.com:bucal/bucal-bms.git
  ```

# Front-end Installation

## Requirements:

1. <b>NodeJs</b>
2. <b>NPM</b>

## Installation

1. Go to **frontend** folder.

   ```
   cd examsync/frontend
   ```
   
3. Install npm dependencies.

   ```
   npm install
   ```

4. Run dev server.

   ```
   npm run start
   ```

4. Run tailwind server

   ```
   npm run tailwind
   ```

# Back-end Installation

## Requirements:

1. <b>Python3</b>
2. <b>Postgresql</b>

## Installation

After installing requirements above, follow the steps below:

1. Go to backend directory.

   ```
   cd backend
   ```

2. Create a virtual environment.

   ```
   python3 -m venv venv
   ```

   

3. Activate virtual environment.

   - For windows:

     ```
     source venv/Scripts/activate
     ```

   - For Ubuntu:

     ```
     source venv/bin/activate
     ```
   
4. Install Django and all project dependencies.

   ```
   pip install -r requirements.txt
   ```

   

5. Setup the database.

   1. Create a user and database in postgresql

      > - How to create a user:
      >
      >   - https://phoenixnap.com/kb/postgres-create-user
      >
      > - How to create a database
      >
      >   `CREATE DATABASE <database_name>;`

   2. Open your favorite text editor or IDE.

   3. Open settings.py located in **core/settings.py**.

   4. Scroll down to:

      > DATABASES = {
      >
      > ​	'default': {
      >
      > ​		'ENGINE': 'django.db.backends.postgresql',
      >
      > ​		'NAME': your_database_name,
      >
      > ​		'USER': database_username,
      >
      > ​		'PASSWORD': database_user_password,
      >
      > ​		'HOST': '',
      >
      > ​		'PORT': '5432'
      >
      > ​	}
      >
      > }

6. Migrate tables to database.

   ```
   python3 manage.py migrate
   ```

   

7. Create a superuser account

   ```
   python3 manage.py createsuperuser
   ```

8. Run the Django server.

   ```
   python3 manage.py runserver
   ```