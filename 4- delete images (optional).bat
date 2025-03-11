REM Delete existing images in static/images/
echo Deleting existing images in static/images/...
if exist "static\images" (
    del /q "static\images\*.*"
) else (
    mkdir "static\images"
)