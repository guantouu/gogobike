FROM shnjp/python-opencv-dlib

RUN pip3 install glob3
RUN pip3 install numpy
RUN pip3 install pymysql
RUN pip3 install flask

COPY ./data /gogobike
COPY ./rec /gogobike
COPY ./src /gogobike
WORKDIR /gogobike/src

EXPOSE 8891
CMD python3 app.py
