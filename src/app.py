import os, sys, glob
import numpy
import cv2
import dlib
import pymysql
from flask import Flask, request, make_response, render_template
detector = dlib.get_frontal_face_detector()
descriptors = []
candidate = []

app = Flask('__name__')
database = pymysql.connect(host='172.18.0.2',
                           port=3306,
                           user='biker1',
                           passwd='0905905155',
                           db='gogobike',
                           charset='utf8'
                          )
IMAGE_PATH = '/gogobike/src/static/image'
FACES_PATH = '/gogobike/rec'
face_feature = dlib.shape_predictor(
    '/gogobike/data/shape_predictor_68_face_landmarks.dat'
)
face_rec = dlib.face_recognition_model_v1(
    '/gogobike/data/dlib_face_recognition_resnet_model_v1.dat'
)

def face_recognition(filenames):
    who = ''
    picture = cv2.imread(os.path.join(IMAGE_PATH, filenames))
    for f in glob.glob(os.path.join(FACES_PATH, "*.jpg")):
        base = os.path.basename(f)
        candidate.append(os.path.splitext(base)[0])
        img = cv2.imread(f)
        dets = detector(img, 1)
        for k, d in enumerate(dets):
            shape = face_feature(img, d)
            face_descriptor = face_rec.compute_face_descriptor(img, shape)
            v = numpy.array(face_descriptor)
            descriptors.append(v)
    dets = detector(picture, 1)
    dist = []
    for k, d in enumerate(dets):
        shape = face_feature(picture, d)
        face_descriptor = face_rec.compute_face_descriptor(picture, shape)
        d_test = numpy.array(face_descriptor)
        for i in descriptors:
            dist_ = numpy.linalg.norm(i - d_test)
            dist.append(dist_)
    c_d = dict(zip(candidate,dist))
    for key, value in sorted(c_d.items(), key=lambda d:d[1]):
        if value >= 0.6:
            who = key
            break
        else:
            who ='guest_' + filenames.split('.', 1)[0]
    return who
    


@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.exists(IMAGE_PATH):
        os.makedirs(IMAGE_PATH)
    image = request.files['upload']
    file_path = os.path.join(IMAGE_PATH, image.filename)
    image.save(file_path)
    name = face_recognition(image.filename)
    database = pymysql.connect(host='172.18.0.2',
                               port=3306,
                               user='biker1',
                               passwd='0905905155',
                               db='gogobike',
                               charset='utf8'
                             )
    cursor = database.cursor()
    cursor.execute(
        'INSERT INTO biker (filename, who) VALUES (%s, %s)',
        (image.filename, name)
    )
    database.commit()
    database.close()
    return ''

@app.route('/index')
def index():
    database = pymysql.connect(host='172.18.0.2',
                               port=3306,
                               user='biker1',
                               passwd='0905905155',
                               db='gogobike',
                               charset='utf8'
                             )
    cursor = database.cursor()
    cursor.execute(
        'SELECT filename, who FROM biker ORDER BY id DESC'
    )
    results = cursor.fetchall()
    database.close()
    print(results[0])
    return render_template(
        'map.html', results=results[0]
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8891)
