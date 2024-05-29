FROM python:3.9-slim-bullseye
LABEL MAINTAINER="Spyros Baltsas <mymail@sbaltsas.xyz>"
LABEL VERSION="1.1"
WORKDIR /app
COPY . .
ARG DEBIAN_FRONTEND=noninteractive
RUN mkdir -p /output /data
RUN apt-get update && apt-get install -y openjdk-17-jdk-headless unzip wget git coreutils && rm -rf /var/lib/apt/lists/* && apt-get clean
RUN wget --output-document=android-sdk.zip https://dl.google.com/android/repository/commandlinetools-linux-7583922_latest.zip
RUN unzip -q android-sdk.zip -d android-sdk && rm android-sdk.zip
ENV ANDROID_SDK_ROOT="/app/android-sdk"
ENV PATH="$PATH:$ANDROID_SDK_ROOT/tools/bin:$ANDROID_SDK_ROOT/platform-tools"
RUN yes | android-sdk/cmdline-tools/bin/sdkmanager  --sdk_root=$ANDROID_SDK_ROOT "platforms;android-30" "build-tools;30.0.3"
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "-u","main.py"]
