# copy into container:
# docker cp metrics_uuid.csv cymap-timescale-1:/

import csv
from uuid import uuid4
import time

start = time.time()

infile = open("metrics.csv", 'r')
outfile = open("metrics_uuid.csv", 'w', newline='')

reader = csv.reader(infile)
writer = csv.writer(outfile)

for row in reader:
    writer.writerow([str(uuid4().hex)] + row)

infile.close()
outfile.close()

end = time.time()

print(f"Time taken: {end - start:.3f} seconds")
# time taken: 8.445 seconds
