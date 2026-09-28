#the goal of this class is to extract salinity values from netcdf
#i am going to match these up with 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

class SkyTEMSurvey:
    #group in this is allowing me to access a specific section of the AEM survey data, more specifically the inverted models
    def __init__(self, filepath, group = 'survey/inverted_models', engine = 'h5netcdf'):
        self.filepath = filepath
        self.group = group
        self.engine = engine
        self.ds = None

        #load data automatically
        self.load()

    #load ds
    def load(self):
        self.ds = xr.open_dataset(
            self.filepath,
            engine = self.engine,
            group = self.group,
            phony_dims = "access"
        )

    #summarize the ds, look inside
    def summary(self):
        print(self.ds.coords)
        print(self.ds.data_vars)

    #getting coord values
    def get_coord(self):
        return self.ds['lon'].values
    
    #get the depth values of prof
    def get_depth(self):
        return self.ds['layer_depth'].values

    #get the resistivity values w corresponding index
    def get_resistivity(self, index):
        return self.ds['RHO'].isel(index = index).values

    #this needs work
    def get_res_loc(self, index):
        return self.ds['RHO'].isel(index = index).values, self.get_coord(), self.get_depth()
    


if __name__ == '__main__':
    survey = SkyTEMSurvey("DelawareBay_SkyTEM_2022_v2.nc")
    #survey.summary()
    #print(survey.get_coord())
    print(survey.get_res_loc(1))
