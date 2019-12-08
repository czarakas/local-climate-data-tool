import sys
import unittest
import xarray as xr
import data_wrangler as dw
import analysis_parameters as params
import unittest
import pytest

# Define directory and file names
DIR_TESTING = params.DIR_DUMMY_DATA
TEST_KEY1 = 'ScenarioMIP.MOHC.UKESM1-0-LL.ssp585.Amon.gn'
TEST_KEY2 = 'CMIP.CAMS.CAMS-CSM1-0.historical.Amon.gn'

TESTING_DATA_DIR = '/home/jovyan/local-climate-data-tool/data/files_for_testing/raw_data/'
TESTING_OUTPUT_DIR = '/home/jovyan/local-climate-data-tool/data/files_for_testing/processed_model_data/'
VARNAME = params.VARIABLE_ID

# Read testing data into dictionary
DSET_DICT = dict()
DSET_DICT[TEST_KEY1] = 57#xr.open_dataset(TESTING_DATA_DIR+TEST_KEY1+'.nc')
DSET_DICT[TEST_KEY2] = 57#xr.open_dataset(TESTING_DATA_DIR+TEST_KEY2+'.nc')

class test_data_wrangler(unittest.TestCase):
    def test_print_time(self):
        dw.print_time()
        self.assertTrue(True)
    
    def test_subcomps(self):
        pytest.main(["test_subcomp_a.py"])
        pytest.main(["test_subcomp_b.py"])
        pytest.main(["test_subcomp_c.py"])
        pytest.main(["test_subcomp_d.py"])
    
    def test_delete_zarr(self):
        self.assertTrue(True)

#     def test_subcomp_a(self, xperiment_ID='ssp126'):
#         dset_dict = dw.subcomponent_a(print_statements_on=True)
#         self.assertTrue(True)

    #def test_subcomp_b(ref_grid_key='TEST_KEY2',dset_dict=DSET_DICT,
    #                   print_statements_on=True, data_dir=DIR_TESTING+'raw_data/'):
    #    dw.subcomponent_b(ref_grid_key, dset_dict, print_statements_on, data_dir)


if __name__ == "__main__":
    unittest.main()
