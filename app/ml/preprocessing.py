import numpy as np
def clean_features(rows):
    data = [[r.cpu_percent, r.memory_percent, r.disk_percent, r.process_count] for r in rows]
    return np.nan_to_num(np.asarray(data, dtype=float), nan=0.0, posinf=100.0, neginf=0.0)
