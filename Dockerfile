RUN apt-get update
RUN apt-get -y install libgl1-mesa-gl
RUN pip3 install opencv-python-headless
RUN apt-get update && apt-get install libgl1-mesa-glx -y
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y


