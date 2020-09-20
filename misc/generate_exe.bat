REM removing generated files before new generation
rmdir /s /q build
rmdir /s /q dist
del /s /q "FPGA_Tools.spec"

REM generating new exe
pyinstaller --onefile --noconsole --name FPGA_Tools ..\src\qqq.py

REM copying generated exe to runnable exe folder
copy "dist\FPGA_Tools.exe" "..\Runnable exe\FPGA_Tools.exe"
pause