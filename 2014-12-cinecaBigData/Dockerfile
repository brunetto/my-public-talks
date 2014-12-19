FROM ubuntu:14.04

MAINTAINER brunetto ziosi <brunetto.ziosi@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

ENV STARLAB_DOWNLOAD ***

# This has to be set by hand and MUST be the same of the host
ENV CUDA_DRIVER 340.46
ENV CUDA_INSTALL http://us.download.nvidia.com/XFree86/Linux-x86_64/${CUDA_DRIVER}/NVIDIA-Linux-x86_64-${CUDA_DRIVER}.run
ENV CUDA_TOOLKIT cuda_6.0.37_linux_32.run
ENV CUDA_TOOLKIT_DOWNLOAD http://developer.download.nvidia.com/compute/cuda/6_0/rel/installers/$CUDA_TOOLKIT

# Update and install minimal.
RUN apt-get update --quiet && apt-get install --yes \
            --no-install-recommends --no-install-suggests \
       build-essential module-init-tools wget 

# Clean up packages.
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install CUDA.
RUN wget $CUDA_INSTALL -P /tmp --no-verbose \
      && chmod +x /tmp/NVIDIA-Linux-x86_64-${CUDA_DRIVER}.run \
      && /tmp/NVIDIA-Linux-x86_64-${CUDA_DRIVER}.run -s -N --no-kernel-module \
      && rm -rf /tmp/*

RUN wget CUDA_TOOLKIT_DOWNLOAD && chmod +x CUDA_TOOLKIT
RUN ./CUDA_TOOLKIT -toolkit -toolkitpath=/usr/local/cuda -samples -samplespath=/usr/local/cuda -silent -override
RUN rm cuda_6.0.37_linux_64.run

# Install StarLab

wget $STARLAB_DOWNLOAD
RUN tar -xvf starlabDockerGPU.tar.gz && rm starlabDockerGPU.tar.gz 
RUN cd starlab/sapporo/ && make && bash compile.sh && cd ../../
RUN cd starlab/starlab/ && ./configure --with-f77=no && make && make install && cd ../../
RUN mv starlab/starlab/usr/bin starlab/bin && rm -rf starlab/starlab

# Default command.
ENTRYPOINT ["/bin/bash"]

