1. Clone the repo
2. Configure the directi/settings.py and change the settings of the database(USER, PASSWORD)
3. Open mysql in console and run command "CREATE DATABASE django_db"
4. Run commnand "python manage.py syncdb" which would create the necessary tables
5. Run the queries present in "bestwatch.sql" file present in the root directory.
Note: It is necessary to populate the bestwatch_genres, bestwatch_shows, bestwatch_shows_genres tables
6. Run command "python manage.py runserver"
7. Goto http://localhost:8000/bestwatch/ 

