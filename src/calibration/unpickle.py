import pickle

path = "data/calibration/galaxyA50/matrix.pkl"

with open(path, "rb") as f:
    loaded_floats = pickle.load(f)

print(loaded_floats)