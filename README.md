 # Blog Lite App

App developed by [Nithesh Kanna S](mailto:21f2001271@student.onlinedegree.iitm.ac.in) (21f2001271)

Made with care using HTML, CSS, Flask, Bootstrap

____

## Steps to run this app
- Create a Virtual environment in the same directory
  - `python -m venv venv` for Windows.
  - `virtualenv venv` for Linux or MacOS.
- Activate the Virtual environment
  - `venv\Scripts\activate` for Windows.
  - `source venv/bin/activate` for Linux or MacOS.
- Run the app `python app.py`
- Don't forget to deactivate the Virtual environment when you're done exploring
  - `venv\Scripts\deactivate` for Windows.
  - `source venv/bin/deactivate` for Linux or MacOS.
___

## Folder Structure

- ### /applications
  - [api.py](applications/api.py) - Contains API calls to get, put, delete, post
  - [/config.py](applications/config.py) - Configuration of database.
  - [/controllers.py](applications/controllers.py) - Contains all routes for the app
  - [/database.py](applications/database.py) - Configuration of SQL Alchemy.
  - [/forms](applications/forms.py) - Contains all WT forms for the app
  - [/models.py](applications/models.py) - Contains Database schemas.

- ### /db_directory
  - [MAD1/sqlite3](db_directory/MAD1.sqlite3) - Local Database for the app 

- ### /flask_session
  - Contains files of User Login session

- ### /static
  - [photos](static/photos) - Contains all Uploaded photos
  - [/style.css](static/styles.css) - Stylesheet.
  - [/rests.css](static/rests.css) - Background Image.

- ### /templates 
  - [/base.html](templates/base.html) - Base template of all pages.
  - [/edit_post.html](templates/edit_post.html) - Template for edit post page.
  - [/edit_profile.html](templates/edit_profile.html) - Template for edit profile page.
  - [/error.html](templates/error.html) - Template for error page
  - [/explore.html](templates/explore.html) - Template for explore page
  - [/feed.html](templates/feed.html) - Template for feed page
  - [/followers.html](templates/followers.html) - Template for followers page
  - [/following.html](templates/following.html) - Template for following page
  - [/formhelpers.html](templates/formhelpers.html) - Template for form helpers
  - [/post.html](templates/post.html) - Template for post page
  - [/post_detail.html](templates/post_detail.html) - Template for post detail page
  - [/profile.html](templates/profile.html) - Template for profile page
  - [/results.html](templates/results.html) - Template for search results page
  - [/search.html](templates/search.html) - Template for search page
  - [/signin.html](templates/signin.html) - Template for signin page
  - [/signup.html](templates/signup.html) - Template for signup page

- ### [/app.py](app.py) - Configuration of Application.
- ### [/CHECKLIST.md](CHECKLIST.md) - Checklist for Project Submission.
- ### [/README.md](README.md) - Readme file for the Project
- ### [/BlogLite App Report.pdf](BlogLite%20App%20Report.pdf) - Project Report.
- ### [/requirements.txt](requirements.txt) - Packages required
- ### [Video](https://drive.google.com/file/d/133s0CWlGhgB99Dfh2z4UBJFbN9w23jEb/view?usp=sharing)
___