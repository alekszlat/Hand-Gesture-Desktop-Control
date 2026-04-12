import subprocess

def mousemove(*, x, y, sync=False, execute=True):
    command = ["xdotool", "mousemove"]

    if sync:
        command.append("--sync")

    command.extend([str(x), str(y)])

    if execute:
        subprocess.call(command)

    return command


def mouseclick(*, button=1, sync=False, execute=True):
    command = ["xdotool", "click"]

    if sync:
        command.append("--sync")

    command.append(str(button))

    if execute:
        subprocess.call(command)

    return command

def mousegrab(*, sync=False, execute=True):
    command = ["xdotool", "mousedown"]

    if sync:
        command.append("--sync")

    command.append("1")

    if execute:
        subprocess.call(command)

    return command

def mouserelease(*, sync=False, execute=True):
    command = ["xdotool", "mouseup"]

    if sync:
        command.append("--sync")

    command.append("1")

    if execute:
        subprocess.call(command)

    return command

def press_Esc(*, sync=False, execute=True):
    command = ["xdotool", "key"]

    if sync:
        command.append("--sync")

    command.append("Escape")

    if execute:
        subprocess.call(command)

    return command