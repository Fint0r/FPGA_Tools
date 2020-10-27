# FPGA Tools
University project to support FPGA development for Nexys 4 and Nexys 4 DDR development boards.

Project supports:
  - TestBench generation
  - Constraint generation

Controls:
 - **File -> Browse:** Search for your source VHDL file. Will be used for signal names and the base for the generation.
 - **File -> Import Pinout:** Custom port list can be imported.
 - **Generate -> TestBench:** Click if you want to generate testbench for your project.
 - **Generate -> Constraint:** Click if you want to generate constraints for your project. Double check your Signal - I/O bindings.
 - **Switch between Nexys4 and Nexys4 DDR** with radio buttons.
 - You can choose to **use onboard 100 MHz clock**.
![Picture of GUI](https://github.com/Fint0r/FPGA_Tools/blob/master/misc/doc/sw_gui.jpg?raw=true "Picture of the SW")

## Installation
Download and run the executable from [here](https://github.com/Fint0r/FPGA_Tools/releases).

## Custom port list format
Custom pinout (port list) can be added to the software. You can browse your JSON file with File -> Import Pinout.
Custom port list should be edited according to the following example.
```javascript
{
   "Name":"Name of your config", // Shall include a name
   "Switch":{   // Every pin shall be organized into groups
      "SW0":"J15",  // Key: functionality, Value: IC pin name
      "SW1":"J16",
      "SW2":"J17",
      "SW3":"J18"
   },
   "LED":{
      "LED0":"H17",
      "LED1":"H18",
      "LED2":"H19",
      "LED3":"H20"
   },
   "Button":{
      "BTN0":"U01",
      "BTN1":"U02",
      "BTN2":"U03"
   },
    "CLK, Reset":{
      "Clock":"E3",
      "Reset":"R12" 
   }
}
```

## Using as library
You can download files as python library via pip install: "pip install fpgatools".

```python
import fpgatools.FPGA_Tools as ft

ft.showwindow()
```

https://pypi.org/project/fpgatools/

## Build your own executable
### Windows
Exe generation can be run with misc/generate_exe.bat.

### Linux
You can generate the executable by running the misc/generate_linux.sh script. Which creates a python virtual environment, installs the required python packages and builds FPGA Tools.
#### Requirements:
##### Debian (Tested on Ubuntu 20.04 LTS):
- `python3`
- `python3-venv` (for python virtual environment)
- `libxcb-xinerama0` (if your de uses wayland you need this)

##### Arch (Tested on Manjaro 20.1.2):
- `python3`
- `glibc` (for pyinstaller)
- `binutils` (for pyinstaller)


## Misc
Generated GUI design can be found in misc/gui_design.ui. Created with QT Designer.
Few popular antivirus software alerts useres about virus in exe. Its false positive alert, because the exe is unsigned (not certificated) [more about signing EXE](https://stackoverflow.com/questions/252226/signing-a-windows-exe-file?noredirect=1&lq=1). [VirusTotal report](https://www.virustotal.com/gui/file/15d41d4d85b69bdeec66af8920b53919d32ba3c486c09b2b85eca7ae09223686/detection)
If you would like to generate your own "virus free" exe you can use [generate_exe.bat](https://github.com/Fint0r/FPGA_Tools/blob/master/misc/generate_exe.bat), in this case you need all of the dependencies installed for your python.

### Feel free to contact us if you have any question.
