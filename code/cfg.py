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
import matplotlib.pyplot as plt

import redii_read as rr


def get_date():
    """ Get string with date.
        Used to make result directories.

        Returns:
        --------
        string with date.
    """

    date = datetime.datetime.now()
    return "{}{:02}{:02}".format(date.year, date.month, date.day)


DATE = get_date()

input_path = "../input/"
output_path = "../output/"
# code2reg_file_name = 'code2reg.txt'
# code2cntr_file_name = 'code2cntr.txt'
cntr_exio2globiom_file_name = "cntr_exio2globiom.txt"

file_name_base = "trial_simulation_redii_baseline.gdx"
file_name_scen = "trial_simulation_redii_scenario.gdx"

file_name_base_eu04 = "trial_simulation_redii_baseline_eu04.gdx"
file_name_scen_eu04 = "trial_simulation_redii_scenario_eu04.gdx"

file_name_base_eu28 = "trial_simulation_redii_baseline_eu28.gdx"
file_name_scen_eu28 = "trial_simulation_redii_scenario_eu28.gdx"

file_name_var_plot_eu28 = "var_plot_eu28.txt"


# file_name_nuts2_shp = "NUTS_RG_20M_2003_3035_LEVL_2.shp"
file_name_nuts2_shp = "EU_nuts_revisited"

file_name_nuts2_1999_2003 = 'nuts2_1999_2003.txt'
# file_name_globiom_out = "Runs_GLOBIOM_Bertram_10sept2020.gdx"

# TODO: change year to 2021.
t_gb_date = ('14jan2020', ("2021", "01", "14"))
# t_gb_base_date = ("output_REF_7sept2020", ("2020", "09", "07"))
# t_gb_scen_date = ("output_EUCO32_7sept2020", ("2020", "09", "07"))
file_name_globiom_out = "Runs_GLOBIOM_Bertram_{}.gdx".format(t_gb_date[0])
t_gb_base_date = "output_REF_{}".format(t_gb_date[0])
t_gb_scen_date = "output_EUCO32_{}".format(t_gb_date[0])

data_dir = "../../exiomod/"

# Define paths for input and output data.
DATA_DIR_PATH = "../../data/"
DATA_SHARE_DIR_PATH = DATA_DIR_PATH+"shared/"
# EXIOMOD_DIR_PATH = '20200805 gwhe/'
EB_IXI_FPA_3_3_2011_PROC_FILE_NAME_PATTERN = 'mrIOT_ixi_fpa_transactions_3.3_2011'
EB_IXI_FPA_3_3_2011_PROC_FILE_NAME = EB_IXI_FPA_3_3_2011_PROC_FILE_NAME_PATTERN+'.pkl'
EB_IXI_FPA_3_3_2011_PROC_FILE_PATH = EB_IXI_FPA_3_3_2011_PROC_FILE_NAME_PATTERN+'/'
EB_IXI_FPA_3_3_2011_PROC_DIR_PATH = DATA_DIR_PATH+EB_IXI_FPA_3_3_2011_PROC_FILE_PATH
T_EB_IXI_FPA_3_3_2011_PROC = (EB_IXI_FPA_3_3_2011_PROC_DIR_PATH,
                              EB_IXI_FPA_3_3_2011_PROC_FILE_NAME)

EB_PXP_ITA_3_3_2011_PROC_FILE_NAME_PATTERN = 'mrIOT_pxp_ita_transactions_3.3_2011'
EB_PXP_ITA_3_3_2011_PROC_FILE_NAME = EB_PXP_ITA_3_3_2011_PROC_FILE_NAME_PATTERN+'.pkl'
EB_PXP_ITA_3_3_2011_PROC_FILE_PATH = EB_PXP_ITA_3_3_2011_PROC_FILE_NAME_PATTERN+'/'
EB_PXP_ITA_3_3_2011_PROC_DIR_PATH = DATA_DIR_PATH+EB_PXP_ITA_3_3_2011_PROC_FILE_PATH
T_EB_PXP_ITA_3_3_2011_PROC = (EB_PXP_ITA_3_3_2011_PROC_DIR_PATH,
                              EB_PXP_ITA_3_3_2011_PROC_FILE_NAME)


EXIOMOD_DIR_PATH = "../../exiomod/"
GLOBIOM_DIR_PATH = "Runs_GLOBIOM/"
INPUT_DIR_PATH = "../input/"
OUTPUT_DIR_PATH = "../output/{}/".format(DATE)
RESULT_DIR_PATH = "{}result/".format(OUTPUT_DIR_PATH)
RESULT_TXT_DIR_PATH = "{}txt/".format(RESULT_DIR_PATH)
RESULT_XLSX_DIR_PATH = "{}xlsx/".format(RESULT_DIR_PATH)
RESULT_PNG_DIR_PATH = "{}png/".format(RESULT_DIR_PATH)
LOG_DIR_PATH = "{}log/".format(OUTPUT_DIR_PATH)

# Files with characterization factors of footprints.
CQE_FILE_NAME = 'Q_emission.txt'
CQM_FILE_NAME = 'Q_material.txt'
CQR_FILE_NAME = 'Q_resource.txt'

LIST_OUTPUT_DIR_PATH = [
    RESULT_TXT_DIR_PATH,
    RESULT_XLSX_DIR_PATH,
    RESULT_PNG_DIR_PATH,
    LOG_DIR_PATH,
]

# Boolean to save processed EXIOBASE version for future uses.
SAVE_EB = True

# Define file names of log data.
LOG_FILE_NAME = "log.txt"

# Define log mode for first log.
log_mode = "w"

file_name_base = "trial_simulation_redii_baseline.gdx"
file_name_scen = "trial_simulation_redii_scenario.gdx"

var_name_va_q_new = "va_k_l_ntp_time_q"
var_name_va_p_new = "va_k_l_ntp_time_p"

var_name_va_q_old = "VA_time_q"
var_name_va_p_old = "VA_time_p"

var_name_y_time_q = "Y_time"
var_name_iu_t_time_q = "INTER_USE_T_time"
var_name_iu_dt_q = "INTER_USE_dt"

var_name_y_time_p = "Y_time_p"
var_name_iu_t_time_p = "INTER_USE_T_time_p"
var_name_iu_dt_time_p = "INTER_USE_dt_time_p"

var_name_k_time_q = "K_time"
var_name_l_time_q = "L_time"
var_name_ntp_time_q = "ntp_txd_ind_time"

var_name_k_time_p = "K_time_p"
var_name_l_time_p = "L_time_p"
var_name_ntp_time_p = "ntp_txd_ind_time_p"

var_name_piu_time = "PIU_time"
var_name_py_time = "PY_time"

var_name_pk_time = "PK_time"
var_name_pl_time = "PL_time"

var_name_emp = "Employment_EMP"

var_name_coprodb_time = "coprodB_time"

var_name_elec_biomass_waste_euco_change = "elec_biomass_waste_EUCO_change"
var_name_elec_iELCB_EUCO_change_2021_2030 = "elec_iELCB_EUCO_change_2021_2030"
var_name_elec_biomass_waste_euco = "elec_biomass_waste_euco"
var_name_elec_biomass_waste_euco_yr = "elec_biomass_waste_euco_yr"
var_name_elec_biomass_waste_euco_data = "elec_biomass_waste_euco_data"
var_name_elec_biomass_waste_euco_dta = "elec_biomass_waste_euco_dta"
var_name_coprod_b_non_norm_time = "coprodB_non_norm_time"
var_name_coprod_b_time = "coprodB_time"
var_name_exec_date = "exec_date"
var_name_exec_time = "exec_time"

var_name_ind_out = "Y_time_gwhe"
var_name_imp = "IMPORT_T_time_gwhe"

yr_start = 2011
yr_end = 2030

file_name_va_p_2030_base = "va_p_2030_base.txt"
file_name_va_p_2030_scen = "va_p_2030_scen.txt"
file_name_va_p_2030_delta = "va_p_2030_delta.txt"
file_name_va_p_2030_delta_r = "va_p_2030_delta_r.txt"

file_name_emp_2030_base = "emp_2030_base.txt"
file_name_emp_2030_scen = "emp_2030_scen.txt"
file_name_emp_2030_delta = "emp_2030_delta.txt"
file_name_emp_2030_delta_r = "emp_2030_delta_r.txt"

file_name_va_p_2030_base_ielcb_nuts2 = "va_p_2030_base_ielcb_nuts2.txt"
file_name_va_p_2030_scen_ielcb_nuts2 = "va_p_2030_scen_ielcb_nuts2.txt"
file_name_va_p_2030_delta_ielcb_nuts2 = "va_p_2030_delta_ielcb_nuts2.txt"
file_name_va_p_2030_delta_r_ielcb_nuts2 = "va_p_2030_delta_r_ielcb_nuts2.txt"

file_name_emp_2030_base_ielcb_nuts2 = "emp_2030_base_ielcb_nuts2.txt"
file_name_emp_2030_scen_ielcb_nuts2 = "emp_2030_scen_ielcb_nuts2.txt"
file_name_emp_2030_delta_ielcb_nuts2 = "emp_2030_delta_ielcb_nuts2.txt"
file_name_emp_2030_delta_r_ielcb_nuts2 = "emp_2030_delta_r_ielcb_nuts2.txt"

file_name_prod_nuts2_2030_base = "p_n2_2030_base.txt"
file_name_prod_nuts2_2030_scen = "p_n2_2030_scen.txt"
file_name_prod_nuts2_2030_delta = "p_n2_2030_delta.txt"
file_name_prod_nuts2_2030_delta_r = "p_n2_2030_delta_r.txt"

file_name_prod_nuts2_2030_base_s_bm_cntr = "p_n2_2030_base_s_bm_cntr.txt"
file_name_prod_nuts2_2030_scen_s_bm_cntr = "p_n2_2030_scen_s_bm_cntr.txt"
file_name_prod_nuts2_2030_delta_s_bm_cntr = "p_n2_2030_delta_s_bm_cntr.txt"
file_name_prod_nuts2_2030_delta_r_s_bm_cntr = "p_n2_2030_delta_r_s_bm_cntr.txt"

file_name_va_p_2030_base_ielcb_cntr_eu = "va_p_2030_base_ielcb_cntr_eu.txt"
file_name_va_p_2030_scen_ielcb_cntr_eu = "va_p_2030_scen_ielcb_cntr_eu.txt"
file_name_va_p_2030_delta_ielcb_cntr_eu = "va_p_2030_delta_ielcb_cntr_eu.txt"
file_name_va_p_2030_delta_r_ielcb_cntr_eu = "va_p_2030_delta_r_ielcb_cntr_eu.txt"

file_name_excel_full = "output_full.xlsx"
file_name_excel_delta_r = "output_delta_r.xlsx"
file_name_excel_base_na_data = 'base_na_data.xlsx'
data_dir = "../../exiomod/"

# Read execution date and time.
t_em_base_datetime = rr.read_exec_datetime(
    DATA_SHARE_DIR_PATH + EXIOMOD_DIR_PATH + file_name_base_eu28
)

t_em_scen_datetime = rr.read_exec_datetime(
    DATA_SHARE_DIR_PATH + EXIOMOD_DIR_PATH + file_name_scen_eu28
)

# Read region correspondence.
with open(INPUT_DIR_PATH + cntr_exio2globiom_file_name, "r") as read_file:
    csv_file = csv.reader(read_file, delimiter="\t")
    d_cntr_globiom2exio = {}
    d_cntr_exio2globiom = {}
    for row in csv_file:
        cntr_exio, cntr_globiom = row
        d_cntr_globiom2exio[cntr_globiom] = cntr_exio
        d_cntr_exio2globiom[cntr_exio] = cntr_globiom

l_eu04 = ["EUN", "EUE", "EUS", "EUW"]

l_eu28 = [
    "EU28_AT",
    "EU28_BE",
    "EU28_BG",
    "EU28_CY",
    "EU28_CZ",
    "EU28_DE",
    "EU28_DK",
    "EU28_EE",
    "EU28_ES",
    "EU28_FI",
    "EU28_FR",
    "EU28_GB",
    "EU28_GR",
    "EU28_HR",
    "EU28_HU",
    "EU28_IE",
    "EU28_IT",
    "EU28_LT",
    "EU28_LU",
    "EU28_LV",
    "EU28_MT",
    "EU28_NL",
    "EU28_PL",
    "EU28_PT",
    "EU28_RO",
    "EU28_SE",
    "EU28_SI",
    "EU28_SK",
]

l_eu28_eb = ['AT',
             'BE',
             'BG',
             'CY',
             'CZ',
             'DE',
             'DK',
             'EE',
             'ES',
             'FI',
             'FR',
             'GB',
             'GR',
             'HR',
             'HU',
             'IE',
             'IT',
             'LT',
             'LU',
             'LV',
             'MT',
             'NL',
             'PL',
             'PT',
             'RO',
             'SE',
             'SI',
             'SK']

l_eu28exuk_eb = ['AT',
                 'BE',
                 'BG',
                 'CY',
                 'CZ',
                 'DE',
                 'DK',
                 'EE',
                 'ES',
                 'FI',
                 'FR',
                 'GR',
                 'HR',
                 'HU',
                 'IE',
                 'IT',
                 'LT',
                 'LU',
                 'LV',
                 'MT',
                 'NL',
                 'PL',
                 'PT',
                 'RO',
                 'SE',
                 'SI',
                 'SK']

dpi = 220
font_size = 7.0
plt.rcParams['mathtext.default'] = 'regular'
plt.rcParams['font.size'] = font_size
plt.rcParams['axes.titlesize'] = font_size
plt.rcParams['font.sans-serif'] = 'Arial'
