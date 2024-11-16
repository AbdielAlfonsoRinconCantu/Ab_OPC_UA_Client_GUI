# OPC Test 1
# ver 0.14x

# Text widget <RETURN> line break Change_PLC_variable_path_text
# Change value of all datatypes
# Send to Query
# Update_labels function
# Button commands array
# UI terminal margins

import sv_ttk
from tkinter import font
from tkinter import *
from tkinter import ttk
import tkinter as tk
from asyncua import Client, Node, ua
import asyncio
print(f"Importing libraries ...")

print(f"Done")
print(f"\nInitializing OPC test ...")
Connection_status = False
print(f"Done")

# Change accordingly
PLC_url = "opc.tcp://HP-Omen-15-2016-Abdiel:4840"
PLC_variable_path = "0:Objects/2:DeviceSet/4:CODESYS Control Win V3 x64/3:Resources/4:Application/3:Programs/4:PLC_PRG/4:Bool_test"

# NodeId data type dictionary
NodeId_identifier_data_type_dictionary = {
    "1": "BOOL",
    "2": "SINT",
    "3": "USINT",
    "4": "INT",
    "5": "UINT",
    "6": "DINT",
    "7": "UDINT",
    "8": "LINT",
    # "8": "XINT",
    "9": "ULINT",
    # "9": "UXINT",
    "10": "REAL",
    "11": "LREAL",
    "12": "WSTRING",
    "3001": "BYTE",
    "3002": "WORD",
    "3003": "DWORD",
    "3004": "LWORD",
    # "3004": "XWORD",
    "3005": "TIME",
    "3006": "LTIME",
    "3013": "STRING",
}

# Array before sending to database
PLC_read_array = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]


def print_to_terminal(print_to_terminal_message):
    print(print_to_terminal_message)
    UI_terminal.insert(tk.END, print_to_terminal_message)
    UI_terminal.see(tk.END)
    UI_terminal.update_idletasks()


def PLC_read_array_shift():
    for i in range(8):
        PLC_read_array[1][i] = PLC_read_array[0][i]


async def asyncio_main(
    Toggle_button_command,
    Set_true_button_command,
    Set_false_button_command,
    Change_PLC_variable_button_command,
    Print_list_button_command,
    Set_value_button_command,
    Write_new_value_command,
    New_value,
):
    global Data_value
    global Browse_name
    global Data_type

    UI_terminal.configure(state="normal")

    print_to_terminal(f"\nConnecting to {PLC_url} ...")

    try:
        async with Client(url=PLC_url) as client:
            print_to_terminal(f"\nConnection successful")

            Connection_status = True

            print_to_terminal(f"\nReading variable ...")

            try:

                PLC_variable = await client.nodes.root.get_child(f"{PLC_variable_path}")

                PLC_read_array_shift()

                if Write_new_value_command:
                    print_to_terminal(f"\nWriting {New_value.Value.Value} to {Browse_name.Name} ...")
                    await PLC_variable.write_value(New_value)

                Browse_name = await PLC_variable.read_browse_name()
                PLC_read_array[0][0] = Browse_name.Name

                browse_name_label.config(
                    text=f"Browse Name: {Browse_name.Name}")

                Data_value = await PLC_variable.read_data_value()
                PLC_read_array[0][1] = Data_value.Value.Value

                data_value_label.config(
                    text=f"Data value: {Data_value.Value.Value}")

                Data_type = await PLC_variable.read_data_type()
                PLC_read_array[0][2] = NodeId_identifier_data_type_dictionary[str(
                    Data_type.Identifier)]

                data_type_label.config(
                    text=f"Data type: {NodeId_identifier_data_type_dictionary[str(Data_type.Identifier)]}")

                print_to_terminal(f"\nList: {PLC_read_array}")

            except:
                print_to_terminal(f"\nFailed to read the variable")

            # Pop-up window buttons

            if Change_PLC_variable_button_command:

                def Accept_button_function():
                    global PLC_variable_path
                    PLC_variable_path = PLC_variable_path_text.get(
                        "1.0", tk.END).strip()

                    UI_terminal.configure(state="normal")

                    print_to_terminal(f"\nNew PLC variable path: {
                        PLC_variable_path}")

                    UI_terminal.configure(state="disabled")

                    asyncio.run(asyncio_main(Toggle_button_command, Set_true_button_command,
                                Set_false_button_command, FALSE, Print_list_button_command, Set_value_button_command, Write_new_value_command, New_value))

                    Change_PLC_variable_window.destroy()

                def Cancel_button_function():
                    Change_PLC_variable_window.destroy()

                Change_PLC_variable_window_Regular_font = font.Font(
                    family="Segoe UI", size=14
                )
                Change_PLC_variable_window_Bold_font = font.Font(
                    family="Segoe UI", size=14, weight="bold"
                )

                Change_PLC_variable_window = Toplevel(root)
                Change_PLC_variable_window.title("Select variable window")

                Current_PLC_variable_path_label = ttk.Label(
                    Change_PLC_variable_window,
                    text=f"Current PLC variable path:",
                    font=Change_PLC_variable_window_Bold_font,
                )
                Current_PLC_variable_path_label.pack(
                    anchor=tk.W,
                    padx=10,
                    pady=10,
                )

                Current_PLC_variable_path_label = ttk.Label(
                    Change_PLC_variable_window,
                    text=f"{PLC_variable_path}",
                    font=Change_PLC_variable_window_Regular_font,
                )

                Current_PLC_variable_path_label.pack(
                    anchor=tk.W,
                    padx=10,
                    pady=10,
                )

                New_PLC_variable_path_label = ttk.Label(
                    Change_PLC_variable_window,
                    text=f"New PLC variable path: ",
                    font=Change_PLC_variable_window_Bold_font,
                )
                New_PLC_variable_path_label.pack(
                    anchor=tk.W,
                    padx=10,
                    pady=10,
                )

                PLC_variable_path_text = tk.Text(
                    Change_PLC_variable_window,
                    font=Change_PLC_variable_window_Regular_font,
                    height=1,
                    width=120,
                    background="#282828",
                    spacing1=4,
                    spacing3=4,
                )
                PLC_variable_path_text.pack(
                    anchor=tk.E, expand=True, padx=10, pady=10)
                PLC_variable_path_text.insert(tk.END, f"{PLC_variable_path}")

                button_frame = ttk.Frame(Change_PLC_variable_window)
                button_frame.pack(padx=10, pady=10, anchor=tk.CENTER)

                Accept_button = ttk.Button(
                    button_frame, text="Accept", command=lambda: Accept_button_function()
                )
                Change_PLC_variable_window.bind(
                    "<Return>", lambda event: Accept_button_function()
                )
                Accept_button.pack(side=tk.LEFT, padx=5)

                Cancel_button = ttk.Button(
                    button_frame, text="Cancel", command=lambda: Cancel_button_function()
                )
                Cancel_button.pack(side=tk.LEFT, padx=5)

            if Set_value_button_command:

                def Accept_button_function():
                    global Data_value
                    UI_terminal.configure(state="normal")
                    New_value = New_value_text.get(1.0, tk.END).strip()

                    if isinstance(Data_value.Value.Value, bool):
                        if New_value == 'True' or New_value == 'true':
                            New_value = True
                        elif New_value == 'False' or New_value == 'false':
                            New_value = False
                        else:
                            print_to_terminal(f"\nInavlid input")
                    elif Data_type.Identifier == 3001:
                        New_value = ua.DataValue(ua.Variant(
                            int(New_value), ua.VariantType.Byte))
                    elif Data_type.Identifier == ua.ObjectIds.Int32:
                        New_value = ua.DataValue(ua.Variant(
                            int(New_value), ua.VariantType.Int32))
                    elif Data_type.Identifier == 3003:
                        New_value = ua.DataValue(ua.Variant(
                            int(New_value), ua.VariantType.UInt32))
                    elif Data_type.Identifier == ua.ObjectIds.Int16:
                        New_value = ua.DataValue(ua.Variant(
                            int(New_value), ua.VariantType.Int16))
                    elif Data_type.Identifier == ua.ObjectIds.Int64:
                        New_value = ua.DataValue(ua.Variant(
                            int(New_value), ua.VariantType.Int64))
                    elif Data_type.Identifier == ua.ObjectIds.Double:
                        New_value = ua.DataValue(ua.Variant(
                            float(New_value), ua.VariantType.Double))
                    elif Data_type.Identifier == ua.ObjectIds.Int64:
                        New_value = ua.DataValue(ua.Variant(
                            int(New_value), ua.VariantType.Int64))
                    elif Data_type.Identifier == ua.ObjectIds.UInt64:
                        New_value = ua.DataValue(ua.Variant(
                            int(New_value), ua.VariantType.UInt64))
                    elif Data_type.Identifier == ua.ObjectIds.Float:
                        New_value = ua.DataValue(ua.Variant(
                            float(New_value), ua.VariantType.Float))
                    elif Data_type.Identifier == ua.ObjectIds.SByte:
                        New_value = ua.DataValue(ua.Variant(
                            int(New_value), ua.VariantType.SByte))
                    elif Data_type.Identifier == 3013:
                        New_value = ua.DataValue(ua.Variant(
                            str(New_value), ua.VariantType.String))
                    elif Data_type.Identifier == ua.ObjectIds.UInt16:
                        New_value = ua.DataValue(ua.Variant(
                            int(New_value), ua.VariantType.UInt16))
                    else:
                        print_to_terminal(f"\nUnsupported data type")

                    UI_terminal.configure(state="disabled")

                    asyncio.run(asyncio_main(Toggle_button_command, Set_true_button_command, Set_false_button_command,
                                Change_PLC_variable_button_command, Print_list_button_command, FALSE, TRUE, New_value))

                    Set_value_window.destroy()

                def Cancel_button_function():
                    Write_new_value_command = False
                    Set_value_window.destroy()

                Set_value_window_Regular_font = font.Font(
                    family="Segoe UI", size=14
                )
                Set_value_window_Bold_font = font.Font(
                    family="Segoe UI", size=14, weight="bold"
                )

                Set_value_window = Toplevel(root)
                Set_value_window.title("Set value window")

                Current_value_label = ttk.Label(
                    Set_value_window,
                    text=f"Current value:",
                    font=Set_value_window_Bold_font,
                )
                Current_value_label.pack(
                    anchor=tk.W,
                    padx=10,
                    pady=10,
                )

                Current_value_label = ttk.Label(
                    Set_value_window,
                    text=f"{Data_value.Value.Value}",
                    font=Set_value_window_Regular_font,
                )
                Current_value_label.pack(
                    anchor=tk.W,
                    padx=10,
                    pady=10,
                )

                New_value_label = ttk.Label(
                    Set_value_window,
                    text=f"New value: ",
                    font=Set_value_window_Bold_font,
                )
                New_value_label.pack(
                    anchor=tk.W,
                    padx=10,
                    pady=10,
                )

                New_value_text = tk.Text(
                    Set_value_window,
                    font=Set_value_window_Regular_font,
                    height=1,
                    width=30,
                    background="#282828",
                    spacing1=4,
                    spacing3=4,
                )
                New_value_text.pack(
                    anchor=tk.E, expand=True, padx=10, pady=10)
                New_value_text.insert(tk.END, f"{Data_value.Value.Value}")

                button_frame = ttk.Frame(Set_value_window)
                button_frame.pack(padx=10, pady=10, anchor=tk.CENTER)

                Accept_button = ttk.Button(
                    button_frame, text="Accept", command=lambda: Accept_button_function()
                )
                Set_value_window.bind(
                    "<Return>", lambda event: Accept_button_function()
                )
                Accept_button.pack(side=tk.LEFT, padx=5)

                Cancel_button = ttk.Button(
                    button_frame, text="Cancel", command=lambda: Cancel_button_function()
                )
                Cancel_button.pack(side=tk.LEFT, padx=5)

            if Print_list_button_command:
                print_to_terminal(f"\nList: {PLC_read_array}")

            # Data value changer buttons

            if Toggle_button_command:
                try:
                    if Data_value.Value.Value == True:
                        print_to_terminal(
                            f"\nSetting value of {
                                Browse_name.Name} to {False} ..."
                        )
                        await PLC_variable.write_value(False)

                        Data_value = await PLC_variable.read_data_value()
                        PLC_read_array[0][1] = Data_value.Value.Value
                        data_value_label.config(
                            text=f"Data value: {Data_value.Value.Value}")

                        print_to_terminal(f"\nValue change successful")
                    else:
                        print_to_terminal(
                            f"\nSetting value of {
                                Browse_name.Name} to {True} ..."
                        )
                        await PLC_variable.write_value(True)

                        Data_value = await PLC_variable.read_data_value()
                        PLC_read_array[0][1] = Data_value.Value.Value
                        data_value_label.config(
                            text=f"Data value: {Data_value.Value.Value}")

                        print_to_terminal(f"\nValue change successful")
                except:
                    print_to_terminal(
                        f"\nFailed to toggle value of {Browse_name.Name}"
                    )

            if Set_true_button_command:
                try:
                    print_to_terminal(f"\nSetting value of {
                        Browse_name.Name} to {True} ...")

                    await PLC_variable.write_value(True)

                    Data_value = await PLC_variable.read_data_value()
                    PLC_read_array[0][1] = Data_value.Value.Value
                    data_value_label.config(
                        text=f"Data value: {Data_value.Value.Value}")

                    print_to_terminal(f"\nValue set successful")
                except:
                    print_to_terminal(
                        f"\nFailed to set value of {
                            Browse_name.Name} to {True} ..."
                    )

            if Set_false_button_command:
                try:
                    print_to_terminal(f"\nSetting value of {
                        Browse_name.Name} to {False} ...")

                    await PLC_variable.write_value(False)

                    Data_value = await PLC_variable.read_data_value()
                    PLC_read_array[0][1] = Data_value.Value.Value
                    data_value_label.config(
                        text=f"Data value: {Data_value.Value.Value}")

                    print_to_terminal(f"\nValue set successful")
                except:
                    print_to_terminal(
                        f"\nFailed to set value of {
                            Browse_name.Name} to {False} ..."
                    )
    except:
        print_to_terminal(f"\nFailed to connect to {PLC_url}")

    UI_terminal.configure(state="disabled")

# run & UI

if __name__ == "__main__":

    def Read_PLC_variable_button_function():
        asyncio.run(
            asyncio_main(
                Toggle_button_command,
                Set_true_button_command,
                Set_false_button_command,
                Change_PLC_variable_button_command,
                Print_list_button_command,
                Set_value_command,
                Write_new_value_command,
                New_value,
            )
        )

    def Toggle_button_function():
        Toggle_button_command = TRUE
        asyncio.run(
            asyncio_main(
                Toggle_button_command,
                Set_true_button_command,
                Set_false_button_command,
                Change_PLC_variable_button_command,
                Print_list_button_command,
                Set_value_command,
                Write_new_value_command,
                New_value,
            )
        )
        Toggle_button_command = FALSE

    def Set_true_button_function():
        Set_true_button_command = TRUE
        asyncio.run(
            asyncio_main(
                Toggle_button_command,
                Set_true_button_command,
                Set_false_button_command,
                Change_PLC_variable_button_command,
                Print_list_button_command,
                Set_value_command,
                Write_new_value_command,
                New_value,
            )
        )
        Set_true_button_command = FALSE

    def Set_false_button_function():
        Set_false_button_command = TRUE
        asyncio.run(
            asyncio_main(
                Toggle_button_command,
                Set_true_button_command,
                Set_false_button_command,
                Change_PLC_variable_button_command,
                Print_list_button_command,
                Set_value_command,
                Write_new_value_command,
                New_value,
            )
        )
        Set_false_button_command = FALSE

    def Change_PLC_variable_button_function():
        Change_PLC_variable_button_command = TRUE
        asyncio.run(
            asyncio_main(
                Toggle_button_command,
                Set_true_button_command,
                Set_false_button_command,
                Change_PLC_variable_button_command,
                Print_list_button_command,
                Set_value_command,
                Write_new_value_command,
                New_value,
            )
        )
        Change_PLC_variable_button_command = FALSE

    def Print_list_button_function():
        Print_list_button_command = TRUE
        asyncio.run(
            asyncio_main(
                Toggle_button_command,
                Set_true_button_command,
                Set_false_button_command,
                Change_PLC_variable_button_command,
                Print_list_button_command,
                Set_value_command,
                Write_new_value_command,
                New_value,
            )
        )
        Print_list_button_command = FALSE

    def Set_value_button_function():
        Set_value_command = TRUE
        asyncio.run(
            asyncio_main(
                Toggle_button_command,
                Set_true_button_command,
                Set_false_button_command,
                Change_PLC_variable_button_command,
                Print_list_button_command,
                Set_value_command,
                Write_new_value_command,
                New_value,
            )
        )
        Set_value_command = FALSE

    def Exit_button_function():
        print(f"\nExiting OPC test ...\n")
        root.destroy()

    if Connection_status == False:
        Browse_name = type("BrowseName", (), {"Name": "UNKNOWN"})
        Data_value = type(
            "DataValue", (), {"Value": type("Value", (), {"Value": "UNKNOWN"})}
        )
        Data_type = type("DataType", (), {"Identifier": "UNKNOWN"})
        Toggle_button_command = FALSE
        Set_true_button_command = FALSE
        Set_false_button_command = FALSE
        Change_PLC_variable_button_command = FALSE
        Print_list_button_command = FALSE
        Set_value_command = FALSE
        Write_new_value_command = FALSE
        New_value = 0

    root = tk.Tk()
    root.title("OPC Test 0.14x")

    Regular_font = font.Font(family="Segoe UI", size=16)
    Terminal_font = font.Font(family="Couier New", size=11)

    browse_name_label = ttk.Label(
        root, text=f"Browse Name: {Browse_name.Name}", font=Regular_font
    )
    browse_name_label.pack(
        anchor=tk.W,
        padx=10,
        pady=10,
    )

    data_value_label = ttk.Label(
        root, text=f"Data Value: {Data_value.Value.Value}", font=Regular_font
    )
    data_value_label.pack(
        anchor=tk.W,
        padx=10,
        pady=10,
    )

    data_type_label = ttk.Label(
        root, text=f"Data type: {Data_type.Identifier}", font=Regular_font
    )
    data_type_label.pack(
        anchor=tk.W,
        padx=10,
        pady=10,
    )

    UI_terminal = tk.Text(root, state="disabled", font=Terminal_font, width=150)
    UI_terminal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    Read_PLC_variable_button = ttk.Button(
        root, text="Read", command=lambda: Read_PLC_variable_button_function()
    )
    Read_PLC_variable_button.pack(
        side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    Toggle_button = ttk.Button(
        root, text="Toggle", command=lambda: Toggle_button_function()
    )
    Toggle_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    Set_true_button = ttk.Button(
        root, text="Set True", command=lambda: Set_true_button_function()
    )
    Set_true_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    Set_false_button = ttk.Button(
        root, text="Set False", command=lambda: Set_false_button_function()
    )
    Set_false_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    Set_value_button = ttk.Button(
        root,
        text="Set value",
        command=lambda: Set_value_button_function(),
    )
    Set_value_button.pack(
        side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    Change_PLC_variable_button = ttk.Button(
        root,
        text="Select variable",
        command=lambda: Change_PLC_variable_button_function(),
    )
    Change_PLC_variable_button.pack(
        side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    Print_matrix_button = ttk.Button(
        root,
        text="List",
        command=lambda: Print_list_button_function(),
    )
    Print_matrix_button.pack(
        side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    Exit_button = ttk.Button(
        root, text="Exit", command=lambda: Exit_button_function())
    Exit_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    sv_ttk.set_theme("dark")

    root.mainloop()
