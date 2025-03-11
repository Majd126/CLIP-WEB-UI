@echo off
REM Ask the user for the folder path
set /p folder_path="Enter the path to the folder containing images: "

REM Check if the folder exists
if not exist "%folder_path%" (
    echo Folder does not exist: %folder_path%
    pause
    exit /b
)

REM Delete existing images in static/images/
echo Deleting existing images in static/images/...
if exist "static\images" (
    del /q "static\images\*.*"
) else (
    mkdir "static\images"
)

REM Copy only image files to static/images/
echo Copying image files from %folder_path% to static/images/...
for %%f in ("%folder_path%\*.jpg" "%folder_path%\*.jpeg" "%folder_path%\*.png" "%folder_path%\*.gif" "%folder_path%\*.bmp" "%folder_path%\*.tiff" "%folder_path%\*.webp" "%folder_path%\*.heic") do (
    copy "%%f" "static\images\"
)

REM Run the preprocess.py script
echo Running preprocess.py to generate embeddings...
python preprocess.py

echo Done!
pause