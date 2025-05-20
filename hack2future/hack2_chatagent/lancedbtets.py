import lancedb

import pandas as pd

uri = "data/lancedb"
db = lancedb.connect(uri)

data = pd.DataFrame({
   "vector": [[1.1, 1.2], [0.2, 1.8]],
    "lat": [45.5, 40.1],
  "long": [-122.7, -74.1]
 })

table = db.create_table("docling", data=data, mode="overwrite")

 