# Schedu

This is a Django Web App designed to help UVA students plan and design their schedules and UVA advisors to review and approve/reject these schedules. It utilizes the UVA SIS API to retrieve course details and is hosted by Heroku. 

__Note:__ This is a continuation of a school project. It is important to note that several others contributed to the project and their names are listed below. While I contributed to the entire project, most of my work was done on the backend and testing which can be found in `portal/management/update_database.py`, `portal/views.py` and `portal/tests.py`

__Names:__ Gavin Fortner, Abby Dhakal, Ananya Ananda, Ashwin Shankar, Caleb Lee

__WEBSITE LINK:__ https://schedu.herokuapp.com/

__GUIDE:__

- __Student Login:__ Log in as a student and you can search for courses and add them to your shopping cart and then finally to your schedule. Additionally, you can request approval from the schedule page. 

- __Teacher Login:__ Log in as a teacher and look at your students' schedules. You must contact an administrator to have students assigned to you. 

- __Special Notes:__ The app only stores class details in the database. It does not actually store meeting/section times as this quickly filled up the database. Instead, it will store class details for all classes and then query the API for section details. This greatly improved space efficiency within the database and general speed/usability of the website. The database can be updated within CLI with `python manage.py update_database` (you will need database credentials)

