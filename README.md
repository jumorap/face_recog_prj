# face_recog_prj
To create a face recognition system we used Opencv. The idea is bluid a system in house that can match face of the residents to give personal messages. But for now, the system send a mail with the face that was recognized.

- Platform supported **Windows, Linux, Mac**
- Tutorial oriented to: **Windows**

# What is?
- The project face_recog_prj was biuld in this fist part as a system that runs over the computer, and using the camera, recognize faces. The faces that aren't saved in "Images" are the faces that the system will assign a name (actual date and hour) and after it will be saved in "Images" file. When that happend (enven if is already saved in the file) the system will send a photo to e-mail registered in "mail.txt"


# How to install?
> 1. Open your console (press Windows + R, write cmd), press enter and clone the repo:
- git clone https://github.com/jumorap/face_recog_prj

> 2. Change the working directory to face_recog_prj
- cd face_recog_prj

> 3. Install the requirements
- python3 -m pip install -r requirements.txt

# How to use?
If do you wanna receive an e-mail when a face is recognized or added, you should edit the file: **mail.txt** and complete it with the instructions that appear there

Execute in your console: 
- cd face_recog_prj
- py Attendance.py

