from uuid import uuid1
import subprocess


class DlxProcessPool(object):
  pool = {}
  _instance = None

  def __new__(self):
    if self._instance is None:
      print('Creating instance')
      self._instance = super(DlxProcessPool, self).__new__(self)

    return self._instance

  def add(self, dlxProcess):
    id = str(uuid1())
    self.pool[id] = dlxProcess
    return id

  def get(self, dlxProcessId):
    if(dlxProcessId not in self.pool.keys()):
      return None
    return self.pool[dlxProcessId]

  def remove(self, dlxProcessId):
    del self.pool[dlxId]


class DlxProcess:
  proc = None

  def __init__(self):
    self.proc = subprocess.Popen("./bin/dlx.exe",
                                  stdin=subprocess.PIPE,
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

  def disassemble(self):
    self.proc.stdin.write('disassemble\n')
    return self._readStdout()

  def run(self):
    self.proc.stdin.write('run\n')
    return self._readStdout()

  def step(self):
    self.proc.stdin.write('step\n')
    return self._readStdout()

  def reset(self):
    self.proc.stdin.write('reset\n\n')
    return self._readStdout()

  def reset(self):
    self.proc.stdin.write('reset\n\n')
    return self._readStdout()

  def _readStdout(self):
    self.proc.stdout.readline()
    return self.proc.stdout.readline().rstrip("\n\r")
