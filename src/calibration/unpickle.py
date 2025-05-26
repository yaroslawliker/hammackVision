import pickle

path = "data/calibration/galaxyA50_4032/matrix.pkl"

with open(path, "rb") as f:
    loaded_floats = pickle.load(f)

print(loaded_floats)