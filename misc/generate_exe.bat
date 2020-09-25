REM removing generated files before new generation
rmdir /s /q build
rmdir /s /q dist
del /s /q FPGA_Tools.spec
del /s /q "..\runnable exe\FPGA_Tools.exe"

REM generating new exe
pyinstaller --onefile --noconsole --clean ..\src\FPGA_Tools.py

REM copying generated exe to runnable exe folder
copy "dist\FPGA_Tools.exe" "..\Runnable exe\FPGA_Tools.exe"