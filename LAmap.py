import shapefile
import matplotlib.pyplot as plt
#from crashmap import zip_filenames
from zipfile import ZipFile
import geopandas as gpd
import pandas as pd
from crashmap import local_authorities as src2

src1 = gpd.read_file("./LA_boundaries/LA_boundaries.shp")
#src2 = pd.read_excel(key_filename, sheet_name="Local Authority (District)")
LAs = pd.merge(src1, src2, left_on="lad15nm", right_on="label", how="inner")
breakpoint()

src1.plot()
plt.show()
#with ZipFile("LA_boundaries.zip") as z:
    #sf = shapefile.Reader("LA_boundaries")

#for s in sf:
#    s.shape.points