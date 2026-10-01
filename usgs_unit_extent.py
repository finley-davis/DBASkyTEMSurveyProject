#USGS Unit Extent Shapefiles Analysis
#here I am analyzing the aquifer unit extents in the Northern Atlantic Coastal Plain Region
#doc: https://www.sciencebase.gov/catalog/item/57df93b2e4b090825000fb55

import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

unit_dict = {
    'upch02': 'nacp_aq02upch_ext/nacp_aq02upch_ext.shp',
    'loch03': 'nacp_aq03loch_ext/nacp_aq03loch_ext.shp',
    'pipt04': 'nacp_aq04pipt_ext/nacp_aq04pipt_ext.shp'
}

class UnitExtent:
    def __init__(self, filepath):
        self.filepath = f'nacp_extent_polygon_files/{filepath}'

        self.load()

    def load(self):
        self.gdf = gpd.read_file(
            self.filepath
        )
        
    def summary(self):
        print('Summary:')
        print(self.gdf.info())

    def extent(self):
        print(self.gdf.bounds)

    def plot_extent(self):
        # Make sure data is in lat/lon so it lines up with PlateCarree
        gdf_geo = self.gdf if self.gdf.crs.to_epsg() == 4326 else self.gdf.to_crs(epsg=4326)

        # Compute area in a projected CRS (meters), but keep gdf_geo in 4326 for plotting
        gdf_m = self.gdf.to_crs(epsg=3857)
        gdf_geo["area_m2"] = gdf_m.geometry.area

        fig, ax = plt.subplots(
            figsize=(10, 10),
            subplot_kw={"projection": ccrs.PlateCarree()}
        )
        ax.set_extent([-80, -50, 20, 50], crs=ccrs.PlateCarree())

        ax.add_feature(cfeature.LAND, facecolor="lightgray")
        ax.add_feature(cfeature.OCEAN, facecolor="lightblue")
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)

        gdf_geo.plot(
            ax=ax,
            transform=ccrs.PlateCarree(),
            edgecolor="black",
            column="area_m2",
            legend=True,
            cmap="viridis"
        )

        gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="gray", alpha=0.5)
        gl.top_labels = False
        gl.right_labels = False

        plt.title("Unit Extents — North Atlantic")
        plt.show()


if __name__ == "__main__":
    shpfile = UnitExtent(unit_dict['upch02'])
    #shpfile.north_atlantic_map()
    shpfile.plot_extent()
