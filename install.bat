@echo off

rem install python venv
pip install virtualenv

set /P INSTALLDIR=Input the path to the directory where you want to install the Virtual Assistant: %=%
echo Installing Python Virtual Assistant to: %INSTALLDIR%

rem setup venv in install directory
virtualenv "%INSTALLDIR%\venv"

rem copy source files
md "%INSTALLDIR%\Assistant"
xcopy "%CD%\Assistant" "%INSTALLDIR%\Assistant" /E/H

rem activate venv and install pip packages
call "%INSTALLDIR%\venv\Scripts\activate"
pip install pafy python-vlc requests youtube-dl mwparserfromhell SpeechRecognition pyttsx3
pip install PyAudio-0.2.11-cp38-cp38-win_amd64.whl

rem run setup
cd /D "%INSTALLDIR%\Src"
set /P INPUT=Input the path to your VLC install directory: %=%
echo vlc_path = r"%INPUT%"> "%INSTALLDIR%\Assistant\Config\env_vars.py"
set /P INPUT=Input your YouTube Data API key: %=%
echo api_key = "%INPUT%">> "%INSTALLDIR%\Assistant\Config\env_vars.py"

echo initializing setup... 
set /P INPUT=Input the wakeword that you want the assistant to respond to: %=%
echo wakeword = "%INPUT%">> "%INSTALLDIR%\Assistant\Config\env_vars.py"
set /P INPUT=Input the energy threshhold for voice recognition (the more sensitive your microphone the higher the threshhold should be): %=%
echo voice_recognition_energy_threshhold = %INPUT%>> "%INSTALLDIR%\Assistant\Config\env_vars.py"
set /P INPUT=Do you want to enable dynamic energy threshhold calibration? (y/n): %=%
If %INPUT%==y (echo voice_recognition_dynamic_energy_threshhold = True>> "%INSTALLDIR%\Assistant\Config\env_vars.py")
If %INPUT%==n (echo voice_recognition_dynamic_energy_threshhold = False>> "%INSTALLDIR%\Assistant\Config\env_vars.py")

rem create start script
echo creating start script...
echo @echo off> "%INSTALLDIR%\start.bat"
echo call "%INSTALLDIR%\venv\Scripts\activate">> "%INSTALLDIR%\start.bat"
echo "%INSTALLDIR%\Assistant\assistant.py">> "%INSTALLDIR%\start.bat"

rem setup complete
echo installation complete!
echo you can now delete the stuff you downloaded from github and enjoy your new virtual assistant!

pause
