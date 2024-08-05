# voiVa

voiVa is an innovative application designed to convert written text and uploaded PDF documents into high-quality audio output. Built with Python 3.9, it leverages the power of FastSpeech and the Kivy framework to provide a seamless and interactive user experience.

## Installation
### The Project is tested on Ubuntu-20.04 with python3.9 installed.
To install voiVa, follow these steps:

1. Ensure you have Python 3.9 installed on your system.
On Ubuntu-20.04 use the following commands to install python3.9
**Update the package list:**
``` sudo apt update ```
**Install prerequisites:**
``` sudo apt install software-properties-common ```
**Add the deadsnakes PPA (which contains newer Python versions):**
``` sudo add-apt-repository ppa:deadsnakes/ppa ```
**Update the package list again:**
``` sudo apt update ```
**Install Python 3.9 and related packages:**
``` sudo apt install python3.9 python3.9-dev python3.9-distutils ```
**After running these commands, you should have pip installed for Python 3.9. You can verify the installation by running:**
``` python3.9 --version ```

***NOTE: Pip is not included by default with Python 3.9, but you can install it easily. Here are the steps to install pip for Python 3.9:***
**Download get-pip.py using curl:**
``` curl -O https://bootstrap.pypa.io/get-pip.py ```
**Install pip for Python 3.9:**
``` sudo python3.9 get-pip.py ```
**After running these commands, you should have pip installed for Python 3.9. You can verify the installation by running:**
``` pip3.9 --version ```

2. Clone the repository:

```git clone https://github.com/ugoMusk/voiVa.git```

3. Navigate to the project directory:

cd voiVa

4. Install the required dependencies:

pip install -r requirements.txt


## Features
- **Text Conversion**: Converts any input text to speech with natural-sounding voices.
- **PDF Support**: Upload and convert PDF files to audio to listen on the go.
- **Customizable Voices**: Choose from a variety of voices and languages.
- **Interactive UI**: Built with KivyMD for a modern and user-friendly interface.
- **Offline Capability**: Works offline, making it accessible anywhere, anytime.

## Authors
- **(ugoMusk)[https://github.com/ugoMusk]**