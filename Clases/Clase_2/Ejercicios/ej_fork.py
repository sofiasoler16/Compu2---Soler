import os

pid = os.fork()

if pid == 0:
    print("[HIJO] Mi PID es", os.getpid(), "Mi padre es", os.getppid())
else:
    print("[PADRE] Mi PID es", os.getpid(), "Creé un hijo con PID", pid)
