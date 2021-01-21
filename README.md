# FDS

A Food Delivery System made using Python and Kivy

### Procedure to Run (On Ubuntu):

#### Download Python:

```
sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev \
```

#### Install Kivy using Software Packages (PPA):

```
# Install necessary system packages
sudo apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev
    
sudo add-apt-repository ppa:kivy-team/kivy-daily
sudo apt-get update
sudo apt-get install python3-kivy
```

Now, Kivy should run smoothly in your local machine but if you receive an error related to the clock event then, change the extension of all 
*.cpython-35m-x86_64-linux-gnu.so to *.so using the below code:

```
sudo find /usr/lib/python3/dist-packages/kivy -type f -name '*.cpython-35m-x86_64-linux-gnu.so' -print0 | xargs -0 \
    sudo rename 's/.cpython-35m-x86_64-linux-gnu.so$.so/'
```

Now, you can simply run the main.py file keeping all the other files in the same directory. 

