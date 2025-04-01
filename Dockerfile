# Run this with 
# docker build -t vggsfm-test .

FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel

# Download the repo
RUN git clone https://github.com/N-Demir/vggsfm.git

WORKDIR vggsfm

# Install vggsfm
RUN source install.sh
RUN python -m pip install -e .


