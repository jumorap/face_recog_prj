import os
import cv2
import face_recognition
import numpy as np

path = 'Images'
images = []
class_names = []
myList = os.listdir(path)

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
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode_face = face_recognition.find_encodings(img)[0]
        encode_list.append(encode_face)

    return encode_list

encode_list_known_faces = find_encodings(images)

print(len(encode_list_known_faces))