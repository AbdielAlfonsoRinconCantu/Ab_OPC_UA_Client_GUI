# Ab's OPC UA Client GUI #
An OPC UA Client GUI to read and write tags.

<div align="center">
  <img src="Ab_OPC_UA_Client_GUI_img1.png" alt="Ab_OPC_UA_Client_GUI_img1.png" width="939" height="573">
</div>

# Before you install #
Make sure the following is installed:
- [Python 3](https://www.python.org/downloads/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)
- [sv_ttk](https://pypi.org/project/sv-ttk/)
- [asyncua](https://pypi.org/project/asyncua/)
- [asyncio](https://docs.python.org/3/library/asyncio.html)

# Installation #
With git:

    git clone https://github.com/AbdielAlfonsoRinconCantu/Ab_OPC_UA_Client_GUI.git

# Before using #
Edit `line 26` of `Ab_OPC_UA_Client_GUI.py` to your device's URL
```python
PLC_url = "opc.tcp://HP-Omen-15-2016-Abdiel:4840"
```
    
# Usage #
Run:

    python OPC_test_148.py
Use the buttons on the GUI to read or write tags with the specified path in `Select variable`
