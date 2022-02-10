# FF-Assignment
## Setup
1) Only one command is needed from root: `docker compose up --build`

2) If you don't have docker installed you can do the following:
    - `pip install -r .\requirements.txt`
    - `python main/manage.py makemigrations`
    - `python main/manage.py migrate`
    - `python main/manage.py runscript setup_demo`
    - `python main/manage.py runserver`

With docker a superuser `admin:admin` is created automatically, you need to add this manually as well if you need it with the second installation method.

3) Visit the site at: http://127.0.0.1:8000/

*Submitted by Kalvyn Roux*