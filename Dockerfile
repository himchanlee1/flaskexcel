RUN apt-get update -y
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get install -y libglib2.0-0
RUN apt-get update && apt-get install libgl1

