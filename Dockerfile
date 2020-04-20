FROM tensorflow/tensorflow:latest-gpu-py3
ARG USER
ENV HOME /home/${USER}
RUN apt update
RUN apt upgrade -y
RUN apt install -y xvfb freeglut3-dev ffmpeg> /dev/null
RUN useradd -m ${USER}
RUN gpasswd -a ${USER} sudo
RUN echo "${USER}:pass" | chpasswd
ADD requirement.txt ${HOME}
WORKDIR ${HOME}
RUN pip install -r requirement.txt
USER ${USER}
WORKDIR ${HOME}/source

