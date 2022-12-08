import numpy as np
from typing import List

def print_table(columns: List[str], data: np.ndarray, padding=20):
  print(" |".join([k.rjust(padding) for k in columns]))
  print("|".join(["".rjust(padding + 1, "-") for k in columns]))

  indices = np.array(list(np.ndindex(data.shape[0:-1])))
  data = data.reshape((-1, data.shape[-1]))
  combined = np.concatenate((indices, data), axis=1)

  for i in range(combined.shape[0]):
    print(" |".join([str(x).rjust(padding) for x in combined[i, :]]))
