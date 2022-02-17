import sys
try:
    assert False, "Python version must be 3"
except Exception as e:
    print(type(e).__name__)
assert False
print("hellp")