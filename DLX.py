import subprocess

class DLX:
    def __init__(self):
        self.proc = subprocess.Popen("./bin/dlx.exe",
                        stdin =subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        bufsize=1)
    def __del__(self): 
        self.proc.kill()

    def load(self, filePath):
        self.proc.stdin.write('load ' + filePath + '\n')
        return self._readStdout()

    def trace(self):
        self.proc.stdin.write('trace\n')
        return self.proc.stdout.readline().rstrip("\n\r")

    def inspect(self):
        self.proc.stdin.write('inspect\n')
        return self._readStdout()

    def run(self):
        self.proc.stdin.write('run\n')
        return self._readStdout()

    def step(self):
        self.proc.stdin.write('step\n')
        return self._readStdout()

    def _readStdout(self):
        self.proc.stdout.readline()
        return self.proc.stdout.readline().rstrip("\n\r")

