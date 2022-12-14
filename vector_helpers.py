import numpy as np

def normalize(vector: np.ndarray):
    return vector / np.linalg.norm(vector)