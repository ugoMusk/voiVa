# voiVa

voiVa is an innovative application designed to convert written text and uploaded PDF documents into high-quality audio output. Built with Python 3.9, it leverages the power of FastSpeech and the Kivy framework to provide a seamless and interactive user experience.

## Installation
To install voiVa, follow these steps:

1. Ensure you have Python 3.9 installed on your system.
On Ubuntu use the following commands to install python3.9
``` sudo add-apt-repository ppa:deadsnakes/ppa ```
``` sudo apt update -y ```
``` sudo apt-get install build-essential ```
``` sudo apt-get install python3.9-distutils ```
``` sudo apt install python3.9 python3.9-dev ```

Python 3.9 is now installed, but may not be the default version on your machine. So ensure you use the command ```python3.9``` each time you want to run the program, or follow the steps below to set python3.9 as the default python version for your environment.

(a) Check your python version with the command:
``` python3 -V ```
This will output your current version of python. For example: [Python 3.8.10]. Make a note of your current version for the next step

(b) Enter the following command, but replace “/usr/bin/python3.8” with your current version if it is different. (for example use “/usr/bin/python3.10” if you got 3.10 from step (a))
``` sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 ```
the '1' at the end is just a priority number that set origi0bnal default version as option one

(c) Set python3.9 as option two with the command:

``` sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 2 ```

(d) Finally, check your available versions:
``` sudo update-alternatives --config python3 ```
Press enter to confirm python3.9, or move the asterik up and down to select a specific version.
Then check the python3 version you selected as default with the command ```python3 -V```

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
- **ugoMusk**