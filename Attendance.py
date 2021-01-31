import os
import cv2
import face_recognition
import numpy as np
import smtplib
import time
import pyttsx3
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


# This will be a simple variable that save names that was returned by [say_hello]
after_detect = []

# Next variables get the e-mail values from "mail.txt", that the user will set
f = open('mail.txt', 'r')
your_email = str(f.readline())[:-1]
your_password = str(f.readline())[:-1]
who_receive = str(f.readline())[:-1]
f.close()


def cover_files_lunch():
    path = 'Images'
    images = []
    class_names = []
    my_list = os.listdir(path)

    print(my_list)

    # We are just generating the image name to after use it in
    # face recognition only adding a photo to root 'images'
    for cl in my_list:
        cur_img = cv2.imread(f'{path}/{cl}')
        images.append(cur_img)
        class_names.append(os.path.splitext(cl)[0])

    print(class_names)

    start(images, class_names)


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
    sender_address = your_email

    # Like server in this case we use Outlook for comfort,
    # but we can select the server of our preference like gmail
    session = smtplib.SMTP("smtp.outlook.com", 587)
    session.starttls()
    # Here we use [session] to login in our account from where the
    # message gonna be send
    session.login(sender_address, your_password)

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
    session.sendmail(sender_address, who_receive, text)
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
        say_my_name = f'Bienvenido {name}'
        new_voice_rate = 145

        player = pyttsx3.init()
        player.setProperty('rate', new_voice_rate)
        player.say(say_my_name)
        player.runAndWait()

        after_detect.append(name)
        try:
            send_mail_record(name, img)
            print("Sent")
        except:
            print("ERROR: Chek the your connection and file mail.text")
        cv2.imshow("Somebody", img)


def start(images, class_names):
    encode_list_known_faces = find_encodings(images)
    cap = cv2.VideoCapture(0)

    print('Complete')

    while True:
        # We do that the system is "listening" constantly the camera
        # who was opened before with [cap]
        success, img = cap.read()
        img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
        color_box = (0, 255, 0)

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
                color_box = (0, 255, 0)
            else:
                # If the face don't match with the models from "Images", will be
                # saved with an identifier *%d%m%y%H%M%S* and after will be
                # added to "Images" set
                color_box = (0, 0, 255)
                timer = time.strftime("%d%m%y%H%M%S")
                face_img = "Images/%d.jpg" % int(timer)
                cv2.imwrite(face_img, img)
                break

            # Is generated a box where tanks to library 'face_recognition', we
            # trace the face of our users, and is multiplied for 4, because
            # would generate a little rectangle that don't match with the user's
            # face. And after bottom this is generated another box where is
            # wrote the name that match with the face
            #
            # Both within, we define the color of border and background of our
            # boxes, too is defined the font, their size and color
            cv2.rectangle(img, (x1, y1 - 30), (x2, y2 + 20), color_box, 1)
            cv2.rectangle(img, (x1, y2 - 15), (x2, y2 + 20), color_box, cv2.FILLED)
            cv2.putText(img, name, (x1 + 5, y2 + 10), cv2.FONT_ITALIC, 0.7, (255, 255, 255), 2)
            say_hello(name, img)

        # With cv2.imshow we open a window where look the "camera process"
        # and the name of who appear in camera
        cv2.imshow('Webcam', img)
        cv2.waitKey(1)

        if color_box == (0, 0, 255):
            break

    cover_files_lunch()


cover_files_lunch()
