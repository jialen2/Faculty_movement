import os, time
print(30)
print("child_process", os.getpid())
print("child_group_process", os.getpgid(os.getpid()))
time.sleep(50)