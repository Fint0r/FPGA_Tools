# FPGA Tools
University project to support FPGA development for Nexys 4 and Nexys 4 DDR development boards.

Project supports:
  - TestBench generation
  - Constraint generation

Controls:
 - **Browse:** Search for your source VHDL file. Will be used for signal names and the base for the generation.
 - **Generat TestBench:** Click if you want to generate testbench for your project.
 - **Generate Constraint:** Click if you want to generate constraints for your project. Double check your Signal - I/O bindings.
 - **Switch between Nexys4 and Nexys4 DDR** with radio buttons
 - You can choose to **use onboard 100 MHz clock**
![Picture of GUI](https://github.com/Fint0r/FPGA_Tools/blob/master/misc/doc/sw_gui.jpg?raw=true "Picture of the SW")

## Using as library
You can download files as python library via pip install: "pip install fpgatools".

```python
import fpgatools.FPGA_Tools as ft

ft.showwindow()
```

https://pypi.org/project/fpgatools/
## Windows

Runnable exe can be found under "Runnable exe" folder.\
Exe generation can be run with misc/generate_exe.bat.

## Linux

Executable can be found in "Runnable exe" folder.\
You can generate the executable by running the misc/generate_linux.sh script.

INFO: Be sure libxcb installed. If not install with: "sudo apt-get install libxcb-xinerama0".
## Misc
Generated GUI design can be found in misc/gui_design.ui. Created with QT Designer.
Few popular antivirus software alerts useres about virus in exe. Its false positive alert, because the exe is unsigned (not certificated) [more about signing EXE](https://stackoverflow.com/questions/252226/signing-a-windows-exe-file?noredirect=1&lq=1). [VirusTotal report](https://www.virustotal.com/gui/file/15d41d4d85b69bdeec66af8920b53919d32ba3c486c09b2b85eca7ae09223686/detection)
If you would like to generate your own "virus free" exe you can use [generate_exe.bat](https://github.com/Fint0r/FPGA_Tools/blob/master/misc/generate_exe.bat), in this case you need all of the dependencies installed for your python.

### Feel free to contact us if you have any question.
