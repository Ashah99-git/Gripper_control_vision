
FROM ubuntu:20.04

# Install Open3D system dependencies and pip
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y
RUN apt-get install -y python3 python3-dev python3-pip
RUN apt-get install -y xorg-dev libglu1-mesa-dev
RUN apt-get install -y libblas-dev liblapack-dev liblapacke-dev
RUN apt-get install -y libsdl2-dev libc++-7-dev libc++abi-7-dev libxi-dev
RUN apt-get install -y clang-7
RUN pip install cmake
RUN apt-get install -y apt-utils build-essential git
RUN git clone --recursive https://github.com/intel-isl/Open3D
WORKDIR /Open3D
RUN git submodule update --init --recursive
RUN mkdir build
WORKDIR /build
RUN apt-get install -y libosmesa6-dev
RUN cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=ON \
    -DBUILD_CUDA_MODULE=OFF \
    -DBUILD_GUI=OFF \
    -DBUILD_TENSORFLOW_OPS=OFF \
    -DBUILD_PYTORCH_OPS=OFF \
    -DBUILD_UNIT_TESTS=ON \
    -DCMAKE_INSTALL_PREFIX=~/open3d_install \
    -DPYTHON_EXECUTABLE=$(which python) \
    -DENABLE_HEADLESS_RENDERING=ON \
    -DUSE_SYSTEM_GLEW=OFF \
    -DUSE_SYSTEM_GLFW=OFF \
    /Open3D

RUN make -j$(nproc)
# Install Open3D from the pypi repositories
RUN make install-pip-package -j$(nproc)
RUN pip install opencv-python-headless

 
RUN pip install gdown
RUN apt-get install unzip

RUN gdown https://drive.google.com/uc?id=19t4odd4K4uE-JoykV7RzhA6nbHR-AnNU
RUN unzip code.zip

COPY ./gripper_selection.py .
COPY ./pcd.txt .
COPY ./rgb_image.jpg .


CMD ["python3", "./gripper_selection.py"]


