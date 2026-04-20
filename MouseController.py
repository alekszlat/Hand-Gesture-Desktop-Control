import subprocess

class MouseController:
    def __init__(self):
        pass
 
    def movemouse(self, x, y, sync=False, execute=True):
        '''Move the mouse to the specified (x, y) coordinates.'''
        command = ["xdotool", "mousemove"]
        
        if sync:
            command.append("--sync")

        command.extend([str(x), str(y)])
        
        if execute:
            subprocess.call(command)
        return command
