import rasterio
import numpy as np

def load_elevation_data(tiff_path):
    try:
        with rasterio.open(tiff_path) as dataset:
            elevation_data = dataset.read(1)  # Read the first band
            elevation_data = elevation_data.astype(np.float32)
            no_data_value = dataset.nodata
            if no_data_value is not None:
                elevation_data[elevation_data == no_data_value] = np.nan
            else:
                elevation_data[np.isnan(elevation_data)] = 0
            return elevation_data
    except Exception as e:
        print(f"Error loading elevation data: {e}")
        return None
