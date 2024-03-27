import mido
import os
import time
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def get_midi_output():
    midi_output = None
    while not midi_output:
        try:
            outputs = mido.get_output_names()
            for x in outputs:
                print(f"{outputs.index(x)} {x}")
            select_output = input("Select midi output (#): ")
            midi_output = outputs[int(select_output)]
        except:
            print("Midi output cannot be found. Please try again.")
    return midi_output


def select_file():
    y = 0
    while y < 1:
        select_sysex = askopenfilename()
        try:
            if select_sysex.split(".")[1] != "syx":
                print("Please choose a sysex file (.syx)")
            else:
                y = 1
        except:
            quit()
    return select_sysex


# Opens GUI window to choose .syx file, sends file to chosen midi device
def send_sysex(output, syx_file_path, syx_filename):
    file = syx_file_path / syx_filename
    print(f"Sending file {syx_filename} to output {output}", end="...")
    port = mido.open_output(output)
    sysex = mido.read_syx_file(file)
    for z in sysex:
        port.send(z)
        print(".", end="")
    print("OK")


def get_dx7_patches():
    dx7_patch_path = Path("./dx7_patches/")
    files = os.listdir(dx7_patch_path)
    files_dict = {num: file for num, file in enumerate(files)}
    return files_dict


def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def print_menu_choices():
    patch_files = get_dx7_patches()
    print(f"{'='*25}Choose a patch file to send{'='*25}")
    for num, file in patch_files.items():
        print(f"{num} | {file}")
    print("M | Change MIDI Destination")
    print("Q | Quit\n")


def main_interaction_loop():
    output = get_midi_output()
    dx7_patch_path = Path("./dx7_patches/")

    patch_files = get_dx7_patches()

    user_input = ""
    while user_input.lower() != "q":
        print_menu_choices()
        user_input = input("Enter a number: ")
        letter_options = frozenset(["m", "q"])
        if user_input.lower() in letter_options:
            if user_input.lower() == "m":
                output = get_midi_output()
        else:
            try:
                selection = int(user_input)
                filename = patch_files[selection]
                file_to_send = dx7_patch_path / filename
                try:
                    send_sysex(output, dx7_patch_path, filename)
                except Exception as e:
                    print(f"OH NO! {e}")
            except (ValueError, KeyError):
                print("Try again. but with *reading* this time.")
        time.sleep(5)
        clear_terminal()
