import face_recognition

image_of_koushiq = face_recognition.load_image_file('./img/known/koushiq.jpg')

koushiq_face_encoding = face_recognition.face_encodings(image_of_koushiq)[0]


unknown_image = face_recognition.load_image_file('./img/unknown/unkoushiq.jpg')

unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]


results = face_recognition.compare_faces([koushiq_face_encoding] , unknown_face_encoding )

if results[0]:
    print('Face of koushiq')
else:
    print('not face of koushiq')

