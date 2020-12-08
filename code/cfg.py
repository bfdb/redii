# -*- coding: utf-8 -*-
""" Configuration module for paper on
    global employment and GDP impact of Renewable Energy Directive II
    Copyright (C) 2020

    Bertram F. de Boer
    Faculty of Science
    Institute of Environmental Sciences (CML)
    Department of Industrial Ecology
    Einsteinweg 2
    2333 CC Leiden
    The Netherlands

    +31 (0)71 527 1478
    b.f.de.boer@cml.leidenuniv.nl

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import csv
import datetime


def get_date():
    """ Get string with date.
        Used to make result directories.

        Returns:
        --------
        string with date.
    """

    date = datetime.datetime.now()
    return '{}{:02}{:02}'.format(date.year, date.month, date.day)

DATE = get_date()

input_path = '../input/'
output_path = '../output/'
# code2reg_file_name = 'code2reg.txt'
# code2cntr_file_name = 'code2cntr.txt'
cntr_exio2globiom_file_name = 'cntr_exio2globiom.txt'

file_name_base = 'trial_simulation_redii_baseline.gdx'
file_name_scen = 'trial_simulation_redii_scenario.gdx'

file_name_base_eu28 = 'trial_simulation_redii_baseline_eu28.gdx'
file_name_scen_eu28 = 'trial_simulation_redii_scenario_eu28.gdx'

file_name_var_plot_eu28 = 'var_plot_eu28.txt'

file_name_globiom_out = 'Runs_GLOBIOM_Bertram_10sept2020.gdx'

data_dir = '../../exiomod/'

# Define paths for input and output data.
DATA_DIR_PATH = '../../data/shared/'
EXIOMOD_DIR_PATH = '20200805 gwhe/'
GLOBIOM_DIR_PATH = 'Runs_GLOBIOM_Bertram_10sept2020/'
INPUT_DIR_PATH = '../input/'
OUTPUT_DIR_PATH = '../output/{}/'.format(DATE)
RESULT_DIR_PATH = '{}result/'.format(OUTPUT_DIR_PATH)
RESULT_TXT_DIR_PATH = '{}txt/'.format(RESULT_DIR_PATH)
RESULT_PNG_DIR_PATH = '{}png/'.format(RESULT_DIR_PATH)
LOG_DIR_PATH = '{}log/'.format(OUTPUT_DIR_PATH)

LIST_OUTPUT_DIR_PATH = [RESULT_TXT_DIR_PATH,
                        RESULT_PNG_DIR_PATH,
                        LOG_DIR_PATH]

# Define file names of log data.
LOG_FILE_NAME = 'log.txt'

# Define log mode for first log.
log_mode = 'w'

file_name_base = 'trial_simulation_redii_baseline.gdx'
file_name_scen = 'trial_simulation_redii_scenario.gdx'

var_name_va_q_new = 'va_k_l_ntp_time_q'
var_name_va_p_new = 'va_k_l_ntp_time_p'

var_name_va_q_old = 'VA_time_q'
var_name_va_p_old = 'VA_time_p'

var_name_y_time_q = 'Y_time'
var_name_iu_t_time_q = 'INTER_USE_T_time'
var_name_iu_dt_q = 'INTER_USE_dt'

var_name_y_time_p = 'Y_time_p'
var_name_iu_t_time_p = 'INTER_USE_T_time_p'
var_name_iu_dt_time_p = 'INTER_USE_dt_time_p'

var_name_k_time_q = 'K_time'
var_name_l_time_q = 'L_time'
var_name_ntp_time_q = 'ntp_txd_ind_time'

var_name_k_time_p = 'K_time_p'
var_name_l_time_p = 'L_time_p'
var_name_ntp_time_p = 'ntp_txd_ind_time_p'

var_name_piu_time = 'PIU_time'
var_name_py_time = 'PY_time'

var_name_pk_time = 'PK_time'
var_name_pl_time = 'PL_time'

var_name_elec_biomass_waste_euco_change = 'elec_biomass_waste_EUCO_change'
var_name_elec_iELCB_EUCO_change_2021_2030 = 'elec_iELCB_EUCO_change_2021_2030'
var_name_elec_biomass_waste_euco = 'elec_biomass_waste_euco'
var_name_elec_biomass_waste_euco_yr = 'elec_biomass_waste_euco_yr'
var_name_elec_biomass_waste_euco_data = 'elec_biomass_waste_euco_data'
var_name_elec_biomass_waste_euco_dta = 'elec_biomass_waste_euco_dta'
var_name_coprod_b_non_norm_time = 'coprodB_non_norm_time'
var_name_coprod_b_time = 'coprodB_time'

var_name_ind_out = 'Y_time_gwhe'
var_name_imp = 'IMPORT_T_time_gwhe'

yr_start = 2011
yr_end = 2030

data_dir = '../../exiomod/'

# Read region correspondence.
with open(INPUT_DIR_PATH + cntr_exio2globiom_file_name, 'r') as read_file:
    csv_file = csv.reader(read_file, delimiter='\t')
    d_cntr_globiom2exio = {}
    for row in csv_file:
        cntr_exio, cntr_globiom = row
        d_cntr_globiom2exio[cntr_globiom] = cntr_exio