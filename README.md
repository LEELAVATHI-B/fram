<div align = "center">
<img src="https://github.com/RMKCET-AI/tesseract/blob/master/cube/static/cube/icons/tesseract_logo.ico" alt="Tesseract" width="25" height="30"<h1 align="center" font-family="courier"> <b><font>Tesseract</font></b></h1>

 <br>
 <br>


[![Sonar Cloud](https://github.com/RMKCET-AI/tesseract/actions/workflows/build.yml/badge.svg)](https://github.com/RMKCET-AI/tesseract/actions/workflows/build.yml/badge.svg)
[![Azure](https://github.com/RMKCET-AI/tesseract/actions/workflows/master_tesseract7.yml/badge.svg)](https://github.com/RMKCET-AI/tesseract/blob/master/.github/workflows/master_tesseract7.yml)
<br/>
<br>
Tesseract is a web-app referring the task given by iamneo 
</div>

---

## Installation Instructions
The portal is a web application; to set it up, we require a python environment with Django and other project dependencies installed.
 Though one can work with the project without a virtual environment, it is recommended to use one to avoid conflicts with other projects

## General setup

1. Make sure that you have `Python 3`, `virtualenv` and `pip` installed.     
2. Clone the repository

    ```bash
        $ git clone https://github.com/RMKCET-AI/tesseract.git
        $ cd tesseract
    ```  
3. Create a python3 virtualenv, activate the environment and Install the project dependencies.  
    - For linux/macintosh:
    ```bash
        $ python3 -m venv venv
        $ source venv/bin/activate
        $ pip3 install -r requirements.txt
    ```   
    - For windows:
    ```bash
        python -m venv venv
        venv/Scripts/activate.bat
        pip install -r requirements.txt
    ```
## Docker setup
Refer docker [documentation](https://docs.docker.com/) for installation 

      
        $ docker-compose build  
        $ docker-compose up  
      

You have now successfully set up the project on your environment. 



### Steps to run
From now when you start your work, run ``source bin/activate`` inside the project repository and you can work with the django application as usual - 

```python
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py createsuperuser
python manage.py runserver
```


*Make sure you pull new changes from remote regularly.*

---
### Contributors
* [Harsha vardhan](https://github.com/thunder-07)
* [Jaswanth](https://github.com/JASWANTHJET)
* [Srinath](https://github.com/srinath0307)
* [Praveen](https://github.com/Praveen-18)  
* [Dileep](https://github.com/Dileepinukurthi)
