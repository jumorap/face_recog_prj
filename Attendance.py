import os
import cv2
import face_recognition
import numpy as np
import smtplib
import time
import pyttsx3
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

path = 'Images'
images = []
class_names = []
myList = os.listdir(path)
after_detect = []

print(myList)

# We are just generating the image name to after use it in
# face recognition only adding a photo to root 'images'
for cl in myList:
    cur_img = cv2.imread(f'{path}/{cl}')
    images.append(cur_img)
    class_names.append(os.path.splitext(cl)[0])

print(class_names)


def find_encodings(images):
    encode_list = []

    for img in images:
        # The image is convert between RGB and BGR color spaces
        # (with or without alpha channel) after, given an image,
        # return the 128-dimension face encoding for each face in the image,
        # and is append the result in [encode_list]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode_face = face_recognition.face_encodings(img)[0]
        encode_list.append(encode_face)

    return encode_list


# [send_mail_record] permit send an mail to tell us
# when somebody appear in camera, and advise it
def send_mail_record(name, img):
    # Next mail is of your preference.
    #
    # Like [sender_address] we define the string of the mail from
    # where we wanna send the message, and we can define another
    # variable like password
    sender_address = 'your_email@outlook.com'

    # Like server in this case we use Outlook for comfort,
    # but we can select the server of our preference like gmail
    session = smtplib.SMTP("smtp.outlook.com", 587)
    session.starttls()
    # Here we use [session] to login in our account from where the
    # message gonna be send
    session.login(sender_address, 'your_password')

    # We define who send the mail, the subject and content
    message = MIMEMultipart()
    message['From'] = sender_address
    message['subject'] = name + ' is in front of the camera'

    # Convert the VideoCapture image [img] in the file [face_img]
    # to be send in a mail and advise who is in camera.
    #
    # [face_img] generate different files of all faces that appeared
    # front of the camera. This is thought to add new faces only with
    # one look with a specific and different name depending of date
    # and hour when was make the picture
    timer = time.strftime("%d%m%y%H%M%S")
    face_img = "new_recog/send_image%d.jpg" % int(timer)
    cv2.imwrite(face_img, img)
    file = open(face_img, 'rb')
    attach_image = MIMEImage(file.read())
    attach_image.add_header('Content-Disposition', 'attachment', filename=face_img)
    message.attach(attach_image)

    # After, we write who gonna receive the message and log out
    text = message.as_string()
    session.sendmail(sender_address, 'who_receive@mail.com', text)
    session.quit()


def say_hello(name, img):
    # After match the user's face, we question if the person was looked before, if is
    # so, then won't happen something, else we gonna add their name in [after_detect]
    # and is called the def [send_mail_record], where we gonna advise who is in camera.
    # Additional to it, the machine say a message when recognize the face of somebody
    if name not in after_detect:

        print(name)

        # Generate one string concatenated with [name] and one integer that define
        # the voice rate or voice speed.
        # After, using pyttsx3 library, we start the 'reader', and is saved in [player]
        # to after send [say_my_name] to be reader with the speed defined in [new_voice_rate]
        say_my_name = f'¡Hola! ¿Cómo estás {name}?'
        new_voice_rate = 145

        player = pyttsx3.init()
        player.setProperty('rate', new_voice_rate)
        player.say(say_my_name)
        player.runAndWait()

        after_detect.append(name)
        send_mail_record(name, img)
        cv2.imshow("Somebody", img)


encode_list_known_faces = find_encodings(images)

print('Complete')

cap = cv2.VideoCapture(0)

while True:
    # We do that the system is "listening" constantly the camera
    # who was opened before with [cap]
    success, img = cap.read()
    img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    # First, we trace and calculate the distance of the image
    face_current_frame = face_recognition.face_locations(img_small)
    encode_face_current_frame = face_recognition.face_encodings(img_small, face_current_frame)

    for encode_face, face_loc in zip(encode_face_current_frame, face_current_frame):
        match_face = face_recognition.compare_faces(encode_list_known_faces, encode_face)
        face_dista = face_recognition.face_distance(encode_list_known_faces, encode_face)

        match_index = np.argmin(face_dista)

        y1, x2, y2, x1 = face_loc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        name = "UNKNOWN"
        if match_face[match_index]:
            # When the conditions is met, is select the name of person who
            # appear in camera if they are registered on file "images" with
            # their respective name
            name = class_names[int(match_index)].upper()

            # Is generated a box where tanks to library 'face_recognition', we
            # trace the face of our users, and is multiplied for 4, because
            # would generate a little rectangle that don't match with the user's
            # face. And after bottom this is generated another box where is
            # wrote the name that match with the face
            #
            # Both within, we define the color of border and background of our
            # boxes, too is defined the font, their size and color
            cv2.rectangle(img, (x1, y1 - 30), (x2, y2 + 20), (0, 255, 0), 1)
            cv2.rectangle(img, (x1, y2 - 15), (x2, y2 + 20), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 5, y2 + 10), cv2.FONT_ITALIC, 0.7, (255, 255, 255), 2)

            say_hello(name, img)
        else:
            cv2.rectangle(img, (x1, y1 - 30), (x2, y2 + 20), (0, 0, 255), 1)
            cv2.rectangle(img, (x1, y2 - 15), (x2, y2 + 20), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, name, (x1 + 5, y2 + 10), cv2.FONT_ITALIC, 0.7, (255, 255, 255), 2)

            say_hello(name, img)

    # With cv2.imshow we open a window where look the "camera process"
    # and the name of who appear in camera
    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
