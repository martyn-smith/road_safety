"""

"""
from io import BytesIO
from zipfile import ZipFile
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

###############################################################################
""" Sources """

root_url = "https://data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-safety-data"
key_filename = "Road-Accident-Safety-Data-Guide.xls"

LA_boundaries_url = "https://geoportal.statistics.gov.uk/datasets/"
LA_boundaries_filename = "./LA_boundaries/LA_boundaries.shp"

population_url = "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland"
population_filepaths = {"2017" : "mid2017/ukmidyearestimates2017finalversion.xls"}

zip_filenames = {"test" : "testdata.zip",
                 "2016" : "dftRoadSafety_Accidents_2016.zip",
                 "2017" : "dftRoadSafetyData_Accidents_2017.zip",
                 "LA_boundaries" : "LA_boundaries.zip"
}

raw_data_urls = {"2016" :  "http://data.dft.gov.uk/road-accidents-safety-data/" 
                         + zip_filenames["2016"],
                 "2017" : "http://data.dft.gov.uk.s3.amazonaws.com/road-accidents-safety-data/" 
                         + zip_filenames["2017"]
}

csv_filenames = {"test" : "accidents.csv",
                 "2016" : "dftRoadSafety_Accidents_2016.csv",
                 "2017" : "Acc.csv"
}
###############################################################################

local_authorities = pd.read_excel(key_filename, sheet_name="Local Authority (District)")
shapes = gpd.read_file(LA_boundaries_filename)

def get_RTCs(year):
    zip_data = zip_filenames["2016"]
    with ZipFile(zip_data) as z:
        with z.open(csv_filenames[year]) as f:
            accidents = pd.read_csv(f)
            fatals = accidents[accidents["Accident_Severity"] == 1]
            serious = accidents[accidents["Accident_Severity"] == 2]
            slight = accidents[accidents["Accident_Severity"] == 3]
    return (accidents, fatals, serious, slight)
# web_data from DfT could be obtained directy:
# requests.get(raw_data_urls[year]) followed by using BytesIO(dft_data.content)
# but high latency.

def plot_RTCs(year, accidents, fatals, serious, slight):
    #scatterplot
    fig1 = fatals.plot.scatter(x="Longitude", y="Latitude", s=1, color="black", 
                               alpha=0.5, label="fatals")
    serious.plot.scatter(x="Longitude", y="Latitude", s=1, color="red", 
                        alpha=0.2, label="serious", ax=fig1)
    slight.plot.scatter(x="Longitude", y="Latitude", s=1, color="blue", 
                        alpha=0.01, label="slight", ax=fig1)
    fig1.set_title(f"RTCs in the UK, {year}")

    #heatmap by hexbinning.  Bit of fun but not that useful really.
    fig2 = accidents.plot.hexbin(x="Longitude", y="Latitude", gridsize=50, bins="log", mincnt=1,
                                cmap="inferno_r")
    plt.show()

def plot_RTCs_by_LA(year, accidents):
    #sum the number of RTCs in each local authority.  We only have 2015 data, unfortunately,
    #and some LAs don't match up, leading to some NaN's.
    local_authorities["RTCs"] = pd.Series([
        len(accidents[accidents["Local_Authority_(District)"] == row]) 
        for row in local_authorities["code"]])
    shapes = pd.merge(shapes, local_authorities, left_on="lad15nm", right_on="label",
                                how="inner")
    shapes.plot(column="RTCs", cmap="inferno_r")
    plt.show()

if __name__ == "__main__":
    year = "2016" #a fine year.
    