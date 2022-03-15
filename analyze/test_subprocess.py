import subprocess, os
print("parent_process", os.getpid())
print("parent_group_process", os.getpgid(os.getpid()))
result = subprocess.run(["python3", "test_runtime.py"])
# result = subprocess.check_output(["python", "google_school_name.py", "uiuc"], preexec_fn=os.setsid)
# result = subprocess.check_output(["python", "google_school_name.py", "uiuc"], preexec_fn=os.setsid)