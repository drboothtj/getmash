'''
getmash utils for interfacing with the terminal
    functions:
        xxx
'''
import subprocess
from typing import List

def run_in_terminal(command: List[str], output=None):
    '''
    Convert a string into a command and run in the terminal.
        Aruments:
            command: list of strings containing the command for the terminal
        Returns:
            process: the process being run
    '''
    #logging.debug(command)
    try:
        stdout_target = open(output, "w") if output else subprocess.DEVNULL
        with subprocess.Popen(
            command, stdout=stdout_target, stderr=subprocess.PIPE
            ) as process:
            _, stderr =process.communicate()
            if stdout_target is not subprocess.DEVNULL:
                stdout_target.close()
            if process.returncode != 0:
                raise RuntimeError(
                    'Failed to run: ' + str(command)
                    + 'with the following error ' + str(stderr))
            return process
    except FileNotFoundError as error:
        raise Exception( #implement custom error
            'getmash could not find an executable, ' + ### implement executables
            'please ensure the correct paths to all executables are provided' ### maybe as config
            ) from error