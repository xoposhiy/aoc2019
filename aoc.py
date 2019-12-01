def readInts(fn):
  with open(fn) as f:
    return list(map(int, f.readlines()))
