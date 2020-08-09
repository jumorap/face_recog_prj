import os
import cv2
import face_recognition
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
def send_mail_record(name):
    # Next mail is of your preference.
    #
    # Like [sender_address] we define the string of the mail from
    # where we wanna send the message, and we can define another
    # variable like password
    sender_address = 'yourmail@outlook.com'

    # Like server in this case we use Outlook for comfort,
    # but we can select the server of our preference like gmail
    session = smtplib.SMTP("smtp.outlook.com", 587)
    session.starttls()
    # Here we use [session] to login in our account from where the
    # message gonna be send
    session.login(sender_address, 'yourpassword')

    # We define who send the mail, the subject and content, after
    # convert the mail to string in a plain mail
    message = MIMEMultipart()
    message['From'] = sender_address
    message['subject'] = 'Hello! There is somebody'
    mail_content = name + " is in front of camera"
    message.attach(MIMEText(mail_content, 'plain'))
    text = message.as_string()

    # After, we write who gonna receive the message and log out
    session.sendmail(sender_address, 'who_receive@mail.com', text)
    session.quit()


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
            name = class_names[match_index].upper()

            # Is generated a box where tanks to library 'face_recognition', we
            # trace the face of our users, and is multiplied for 4, because
            # would generate a little rectangle that don't match with the user's
            # face. And after bottom this is generated another box where is
            # wrote the name that match with the face
            #
            # Both within, we define the color of border and background of our
            # boxes, too is defined the font, their size and color
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)

            # After match the user's face, we question if the person was looked, if is
            # so, then won't happen something, else we gonna add their name in [after_detect]
            # and is called the def [send_mail_record], where we gonna advise who is in camera
            if name not in after_detect:
                after_detect.append(name)
                send_mail_record(name)
        else:
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 0, 255), cv2.FILLED)

        cv2.putText(img, name, (x1 + 5, y2 - 10), cv2.FONT_ITALIC, 0.7, (255, 255, 255), 2)

    # With cv2.imshow we open a window where look the "camera process"
    # and the name of who appear in camera
    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
