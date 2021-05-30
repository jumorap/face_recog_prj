<p aligment="center">
    <img src="https://cdn.discordapp.com/attachments/766535715327836172/848375844178362408/unknown.png" alt="Logo image of Face recog proj">
</p>

- Platform supported **Windows, Linux, Mac**
- Usable in **Raspberry Pi**

# What is?
To create a face recognition that helps to watch specific places of the house was used Opencv. The idea is to build a house system that can match the face of the residents to give personal messages. The system sends a mail with the face and name (if is registered) of the person that was recognized.

The project face_recog_prj was built in first place as a system that runs over the computer or a Raspberry Pi, using a camera to recognizes faces.

For faces that aren't saved in "/Images", this tool will assign a name (actual date and hour), after, it will be saved in the "/Images" file. When that happened (even if is already saved in the file) the system will send a photo to the e-mail registered in "mail.txt"


# How to install?
**1.** Open your console and clone the repo:
```
git clone https://github.com/jumorap/face_recog_prj
```
**2.** Change the working directory to opera-extension-generator:
```
cd face_recog_prj
```
**3.** Install the requirements (You need to have installed Python3):
```
python3 -m pip install -r requirements.txt
```

# How to use?
**1.** Run i your console:
```
python3 Attendance.py
```

Note:<br/>
If do you wanna receive an e-mail when a face is recognized or added, you should edit the file: **mail.txt** and complete it with the instructions that appear there
`your_email@outlook.com`
`your_password`
`who_receive@mail.com`

# Possible troubles
If you are in Windows, using **python3** might not work. Use **python** instead.<br/>

- `ModuleNotFoundError: No module named 'cv2'` Then run in your console:
```
pip3 install opencv-python==4.5.2.52 --force --user
```
- `ModuleNotFoundError: No module named 'face_recognition'` Then run in your console:
```
pip3 install boost --force --user
pip3 install dlib==19.22.0 --force --user
pip3 install cmake==3.20.2 --force --user
pip3 install face_recognition==1.2.3 --force --user
```
Don't work? Download Conda environment [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) and run in your console:
```
conda install -c conda-forge dlib
conda install -c conda-forge cmake
conda install -c conda-forge face_recognition
```
Don't work? 
1. Download Microsoft Visual Studio 2015 or newer (check if build tools are enough).
2. Install the dependencies from the previous step, using `pip`

## License
MIT © Face Recog Prj