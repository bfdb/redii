# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:08:15 2020

@author: bfdeboer
"""

import csv
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import operator
import pandas as pd
import seaborn as sns

# import xlsxwriter as xw
import xlwings as xw

import cfg
import utils as ut
import redii_read as rr
import redii_calc as rc
import redii_write as rw

plot = False

wb_full = rw.create_wb()
wb_delta_r = rw.create_wb()
wb_base_na_data = rw.create_wb()
"""
Parse value added from EXIOMOD.
"""
# Read value added in prices from baseline and EUCO3232.5.
df_va_p_2030_base = rr.read_va_yr(
    cfg.DATA_SHARE_DIR_PATH + cfg.EXIOMOD_DIR_PATH + cfg.file_name_base_eu28,
    cfg.var_name_va_p_new,
    cfg.yr_end,
)

df_va_p_2030_scen = rr.read_va_yr(
    cfg.DATA_SHARE_DIR_PATH + cfg.EXIOMOD_DIR_PATH + cfg.file_name_scen_eu28,
    cfg.var_name_va_p_new,
    cfg.yr_end,
)

# Calculate relative difference between baseline and EUCO3232.5 scenario.
df_va_p_2030_delta = df_va_p_2030_scen - df_va_p_2030_base
df_va_p_2030_delta_r = df_va_p_2030_scen / df_va_p_2030_base - 1

rw.write_var(df_va_p_2030_base, cfg.file_name_va_p_2030_base)

rw.write_var(df_va_p_2030_scen, cfg.file_name_va_p_2030_scen)

rw.write_var(df_va_p_2030_delta, cfg.file_name_va_p_2030_delta)

rw.write_var(df_va_p_2030_delta_r, cfg.file_name_va_p_2030_delta_r)


rw.write_var_excel(df_va_p_2030_base,
                   cfg.file_name_va_p_2030_base[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_va_p_2030_scen,
                   cfg.file_name_va_p_2030_scen[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_va_p_2030_delta,
                   cfg.file_name_va_p_2030_delta[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_va_p_2030_delta_r,
                   cfg.file_name_va_p_2030_delta_r[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_va_p_2030_delta_r,
                   cfg.file_name_va_p_2030_delta_r[:-4],
                   wb_delta_r,
                   unstack=1)

# Sum value added per country.
df_va_p_2030_cntr_base = df_va_p_2030_base.sum(level=0)
df_va_p_2030_cntr_scen = df_va_p_2030_scen.sum(level=0)

df_va_p_2030_cntr_delta = df_va_p_2030_cntr_scen - df_va_p_2030_cntr_base
df_va_p_2030_cntr_delta_r = df_va_p_2030_cntr_scen / df_va_p_2030_cntr_base - 1

# Get value added for biomass electricity industry of EU member states.
df_va_p_2030_base_ielcb = df_va_p_2030_base[:, "iELCB"]
df_va_p_2030_scen_ielcb = df_va_p_2030_scen[:, "iELCB"]
df_va_p_2030_delta_ielcb = df_va_p_2030_delta[:, "iELCB"]
df_va_p_2030_delta_r_ielcb = df_va_p_2030_delta_r[:, "iELCB"]

df_va_p_2030_base_ielcb_cntr_eu = rc.va_ind_cntr_eu(df_va_p_2030_base, "iELCB")

df_va_p_2030_scen_ielcb_cntr_eu = rc.va_ind_cntr_eu(df_va_p_2030_scen, "iELCB")

df_va_p_2030_delta_ielcb_cntr_eu = rc.va_ind_cntr_eu(df_va_p_2030_delta, "iELCB")

df_va_p_2030_delta_r_ielcb_cntr_eu = rc.va_ind_cntr_eu(df_va_p_2030_delta_r, "iELCB")


rw.write_va_ielcb_eu(
    df_va_p_2030_base_ielcb_cntr_eu, cfg.file_name_va_p_2030_base_ielcb_cntr_eu
)

rw.write_va_ielcb_eu(
    df_va_p_2030_scen_ielcb_cntr_eu, cfg.file_name_va_p_2030_scen_ielcb_cntr_eu
)

rw.write_va_ielcb_eu(
    df_va_p_2030_delta_ielcb_cntr_eu, cfg.file_name_va_p_2030_delta_ielcb_cntr_eu
)

rw.write_va_ielcb_eu(
    df_va_p_2030_delta_r_ielcb_cntr_eu, cfg.file_name_va_p_2030_delta_r_ielcb_cntr_eu
)

"""
Parse employment from EXIOMOD.
"""
# Read industry output in prices from baseline and EUCO3232.5.
df_y_p_2030_base = rr.read_va_yr(
    cfg.DATA_SHARE_DIR_PATH + cfg.EXIOMOD_DIR_PATH + cfg.file_name_base_eu28,
    cfg.var_name_y_time_p,
    cfg.yr_end,
)

df_y_p_2030_scen = rr.read_va_yr(
    cfg.DATA_SHARE_DIR_PATH + cfg.EXIOMOD_DIR_PATH + cfg.file_name_scen_eu28,
    cfg.var_name_y_time_p,
    cfg.yr_end,
)

df_y_p_2030_delta = df_y_p_2030_scen - df_y_p_2030_base
df_y_p_2030_delta_r = df_y_p_2030_scen / df_y_p_2030_base - 1


rw.write_var_excel(df_y_p_2030_base,
                   cfg.file_name_y_p_2030_base[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_y_p_2030_scen,
                   cfg.file_name_y_p_2030_scen[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_y_p_2030_delta,
                   cfg.file_name_y_p_2030_delta[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_y_p_2030_delta_r,
                   cfg.file_name_y_p_2030_delta_r[:-4],
                   wb_full,
                   unstack=1)

df_y_q_2030_base = rr.read_va_yr(
    cfg.DATA_SHARE_DIR_PATH + cfg.EXIOMOD_DIR_PATH + cfg.file_name_base_eu28,
    cfg.var_name_y_time_q,
    cfg.yr_end,
)

df_y_q_2030_scen = rr.read_va_yr(
    cfg.DATA_SHARE_DIR_PATH + cfg.EXIOMOD_DIR_PATH + cfg.file_name_scen_eu28,
    cfg.var_name_y_time_q,
    cfg.yr_end,
)

df_y_q_2030_delta = df_y_q_2030_scen - df_y_q_2030_base
df_y_q_2030_delta_r = df_y_q_2030_scen / df_y_q_2030_base - 1

rw.write_var_excel(df_y_q_2030_base,
                   cfg.file_name_y_q_2030_base[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_y_q_2030_scen,
                   cfg.file_name_y_q_2030_scen[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_y_q_2030_delta,
                   cfg.file_name_y_q_2030_delta[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_y_q_2030_delta_r,
                   cfg.file_name_y_q_2030_delta_r[:-4],
                   wb_full,
                   unstack=1)

# Get 2011 coefficients of employment satellite account.
df_emp_c = rr.get_emp_c()

df_emp_2030_base = df_emp_c * df_y_p_2030_base
df_emp_2030_scen = df_emp_c * df_y_p_2030_scen

df_emp_2030_delta = df_emp_2030_scen - df_emp_2030_base
df_emp_2030_delta_r = df_emp_2030_scen / df_emp_2030_base - 1

rw.write_var(df_emp_2030_base, cfg.file_name_emp_2030_base)

rw.write_var(df_emp_2030_scen, cfg.file_name_emp_2030_scen)

rw.write_var(df_emp_2030_delta, cfg.file_name_emp_2030_delta)

rw.write_var(df_emp_2030_delta_r, cfg.file_name_emp_2030_delta_r)

rw.write_var_excel(df_emp_2030_base,
                   cfg.file_name_emp_2030_base[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_emp_2030_scen,
                   cfg.file_name_emp_2030_scen[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_emp_2030_delta,
                   cfg.file_name_emp_2030_delta[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_emp_2030_delta_r,
                   cfg.file_name_emp_2030_delta_r[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_emp_2030_delta_r,
                   cfg.file_name_emp_2030_delta_r[:-4],
                   wb_delta_r,
                   unstack=1)

"""
Parse biomass productivity from GLOBIOM.
"""
# Read biomass productivity from baseline and EUCO3232.5
df_out_nuts2 = rr.read_gdx(
    cfg.DATA_SHARE_DIR_PATH + cfg.GLOBIOM_DIR_PATH + cfg.file_name_globiom_out,
    "OUTPUT_NUTS2")

i_slice_base = pd.IndexSlice[
    cfg.t_gb_base_date,
    "PROD",
    "1000 t",
    :,
    :,
    ["SW_Biomass", "IP_Biomass", "PW_Biomass"],
    "SSP2",
    "REFERENCE",
    "REFERENCE",
    "2030",
]

df_prod_nuts2_2030_base_na = df_out_nuts2.loc[i_slice_base]
df_prod_nuts2_2030_base_na = df_prod_nuts2_2030_base_na.droplevel([0, 1, 2, 6, 7, 8, 9])

i_slice_scen = pd.IndexSlice[
    cfg.t_gb_scen_date,
    "PROD",
    "1000 t",
    :,
    :,
    ["SW_Biomass", "IP_Biomass", "PW_Biomass"],
    "SSP2",
    "REFERENCE",
    "EUCO32",
    "2030",
]


df_prod_nuts2_2030_scen = df_out_nuts2.loc[i_slice_scen]
df_prod_nuts2_2030_scen = df_prod_nuts2_2030_scen.droplevel([0, 1, 2, 6, 7, 8, 9])

# Fill missing values in baseline.
df_prod_nuts2_2030_base, df_base_na_scen_data = rr.fill_base(
    df_prod_nuts2_2030_base_na, df_prod_nuts2_2030_scen, fill_na_val=0
)

df_prod_nuts2_2030_base, df_prod_nuts2_2030_scen = rr.harmonize_col_order(
    df_prod_nuts2_2030_base,
    df_prod_nuts2_2030_scen)


###
# Investigate missing baseline data.
df_base_na_scen_data_u = df_base_na_scen_data.unstack()

df_prod_nuts2_2030_scen_u = df_prod_nuts2_2030_scen.unstack()
df_base_na_scen_data_full_u = (
    df_prod_nuts2_2030_scen_u.loc[df_base_na_scen_data_u.index])

df_prod_nuts2_2030_base_u = df_prod_nuts2_2030_base.unstack()

df_base_na_base_data_u = df_prod_nuts2_2030_base_u.loc[df_base_na_scen_data_u.index]

df_prod_nuts2_2030_base_u = df_prod_nuts2_2030_scen

rw.write_var_excel(df_base_na_base_data_u,
                   'base_na_base_data',
                   wb_base_na_data,
                   unstack=0)

rw.write_var_excel(df_base_na_scen_data_full_u,
                   'base_na_scen_data_full_u',
                   wb_base_na_data,
                   unstack=0)
###


df_prod_nuts2_2030_delta = df_prod_nuts2_2030_scen - df_prod_nuts2_2030_base
df_prod_nuts2_2030_delta_r = df_prod_nuts2_2030_scen / df_prod_nuts2_2030_base - 1

rw.write_var_excel(df_prod_nuts2_2030_base,
                   cfg.file_name_prod_nuts2_2030_base[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_prod_nuts2_2030_scen,
                   cfg.file_name_prod_nuts2_2030_scen[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_prod_nuts2_2030_delta,
                   cfg.file_name_prod_nuts2_2030_delta[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_prod_nuts2_2030_delta_r,
                   cfg.file_name_prod_nuts2_2030_delta_r[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_prod_nuts2_2030_delta_r,
                   cfg.file_name_prod_nuts2_2030_delta_r[:-4],
                   wb_delta_r,
                   unstack=1)

# Sum over biomass.
df_prod_nuts2_2030_base_s_bm = df_prod_nuts2_2030_base.sum(level=[0, 1])
df_prod_nuts2_2030_scen_s_bm = df_prod_nuts2_2030_scen.sum(level=[0, 1])
df_prod_nuts2_2030_delta_s_bm = (
    df_prod_nuts2_2030_scen_s_bm - df_prod_nuts2_2030_base_s_bm
)
df_prod_nuts2_2030_delta_r_s_bm = (
    df_prod_nuts2_2030_scen_s_bm / df_prod_nuts2_2030_base_s_bm
) - 1

# Sum over NUTS-2 regions.
df_prod_nuts2_2030_base_s_bm_cntr = df_prod_nuts2_2030_base_s_bm.sum(level=0)
df_prod_nuts2_2030_scen_s_bm_cntr = df_prod_nuts2_2030_scen_s_bm.sum(level=0)

df_prod_nuts2_2030_delta_s_bm_cntr = (
    df_prod_nuts2_2030_scen_s_bm_cntr - df_prod_nuts2_2030_base_s_bm_cntr
)

df_prod_nuts2_2030_delta_r_s_bm_cntr = (
    df_prod_nuts2_2030_scen_s_bm_cntr / df_prod_nuts2_2030_base_s_bm_cntr
) - 1

rw.write_prod_bm_cntr(
    df_prod_nuts2_2030_base_s_bm_cntr, cfg.file_name_prod_nuts2_2030_base_s_bm_cntr
)

rw.write_prod_bm_cntr(
    df_prod_nuts2_2030_scen_s_bm_cntr, cfg.file_name_prod_nuts2_2030_scen_s_bm_cntr
)

rw.write_prod_bm_cntr(
    df_prod_nuts2_2030_delta_s_bm_cntr, cfg.file_name_prod_nuts2_2030_delta_s_bm_cntr
)

rw.write_prod_bm_cntr(
    df_prod_nuts2_2030_delta_r_s_bm_cntr,
    cfg.file_name_prod_nuts2_2030_delta_r_s_bm_cntr,
)


rw.write_var_excel(df_prod_nuts2_2030_base_s_bm_cntr,
                   cfg.file_name_prod_nuts2_2030_base_s_bm_cntr[:-4],
                   wb_full,
                   unstack=0)

rw.write_var_excel(df_prod_nuts2_2030_scen_s_bm_cntr,
                   cfg.file_name_prod_nuts2_2030_scen_s_bm_cntr[:-4],
                   wb_full,
                   unstack=0)

rw.write_var_excel(df_prod_nuts2_2030_delta_s_bm_cntr,
                   cfg.file_name_prod_nuts2_2030_delta_s_bm_cntr[:-4],
                   wb_full,
                   unstack=0)

rw.write_var_excel(df_prod_nuts2_2030_delta_r_s_bm_cntr,
                   cfg.file_name_prod_nuts2_2030_delta_r_s_bm_cntr[:-4],
                   wb_full,
                   unstack=0)

rw.write_var_excel(df_prod_nuts2_2030_delta_r_s_bm_cntr,
                   cfg.file_name_prod_nuts2_2030_delta_r_s_bm_cntr[:-4],
                   wb_delta_r,
                   unstack=0)

# For each EU28 country,
# Calc fraction of biomass prod per nuts2 region in base.
df_prod_nuts2_2030_base_s_bm_r = rc.calc_d_cntr_nuts2_r(df_prod_nuts2_2030_base_s_bm)

# For each EU28 country,
# calc fraction of biomassm prod per nuts2 region in scen
df_prod_nuts2_2030_scen_s_bm_r = rc.calc_d_cntr_nuts2_r(df_prod_nuts2_2030_scen_s_bm)

###
# Get all biomass
i_slice_base_bm_all = pd.IndexSlice[
    cfg.t_gb_base_date,
    "PROD",
    "1000 t",
    :,
    :,
    :,
    "SSP2",
    "REFERENCE",
    "REFERENCE",
    "2030",
]

df_prod_nuts2_2030_base_bm_all_na = df_out_nuts2.loc[i_slice_base_bm_all]

i_slice_scen_bm_all = pd.IndexSlice[
    cfg.t_gb_scen_date,
    "PROD",
    "1000 t",
    :,
    :,
    :,
    "SSP2",
    "REFERENCE",
    "EUCO32",
    "2030",
]

df_prod_nuts2_2030_scen_bm_all = df_out_nuts2.loc[i_slice_scen_bm_all]

# Fill missing values in baseline.
df_prod_nuts2_2030_base_bm_all, df_base_na_scen_bm_all_data = rr.fill_base(
    df_prod_nuts2_2030_base_bm_all_na, df_prod_nuts2_2030_scen_bm_all, fill_na_val=0
)

df_prod_nuts2_2030_base_bm_all, df_prod_nuts2_2030_scen_bm_all = rr.harmonize_col_order(
    df_prod_nuts2_2030_base_bm_all,
    df_prod_nuts2_2030_scen_bm_all)


df_prod_nuts2_2030_base_bm_all_cntr = (
    df_prod_nuts2_2030_base_bm_all.sum(level=[0, 2]))
df_prod_nuts2_2030_scen_bm_all_cntr = (
    df_prod_nuts2_2030_scen_bm_all.sum(level=[0, 2]))

df_prod_nuts2_2030_delta_bm_all_cntr = (
    df_prod_nuts2_2030_scen_bm_all_cntr - df_prod_nuts2_2030_base_bm_all_cntr)
df_prod_nuts2_2030_delta_r_bm_all_cntr = (
    df_prod_nuts2_2030_scen_bm_all_cntr / df_prod_nuts2_2030_base_bm_all_cntr - 1)

df_prod_nuts2_2030_delta_r_bm_all_cntr.replace([np.inf, -np.inf], np.nan, inplace=True)
# df_prod_nuts2_2030_delta_bm_all_cntr = (
#     df_prod_nuts2_2030_delta_bm_all.sum(level=[0, 2]))
# df_prod_nuts2_2030_delta_r_bm_all_cntr = (
#     df_prod_nuts2_2030_delta_r_bm_all.sum(level=[0, 2]))

rw.write_var_excel(df_prod_nuts2_2030_base_bm_all_cntr,
                   cfg.file_name_prod_nuts2_2030_base_bm_all[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_prod_nuts2_2030_scen_bm_all_cntr,
                   cfg.file_name_prod_nuts2_2030_scen_bm_all[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_prod_nuts2_2030_delta_bm_all_cntr,
                   cfg.file_name_prod_nuts2_2030_delta_bm_all[:-4],
                   wb_full,
                   unstack=1)

rw.write_var_excel(df_prod_nuts2_2030_delta_r_bm_all_cntr,
                   cfg.file_name_prod_nuts2_2030_delta_r_bm_all[:-4],
                   wb_full,
                   unstack=1)
"""
Disaggregate value added to NUTS-2.
"""

# For each EU28 country,
# disagg value added over nuts2 acc to bm prod frac in base
df_va_p_2030_base_ielcb_nuts2 = rc.calc_d_cntr_nuts2_ielcb(
    df_va_p_2030_base, df_prod_nuts2_2030_base_s_bm_r
)

# For each EU28 country,
# disagg value added over nuts2 acc to bm prod frac in scen
df_va_p_2030_scen_ielcb_nuts2 = rc.calc_d_cntr_nuts2_ielcb(
    df_va_p_2030_scen, df_prod_nuts2_2030_scen_s_bm_r
)

df_va_p_2030_delta_ielcb_nuts2 = (
    df_va_p_2030_scen_ielcb_nuts2 - df_va_p_2030_base_ielcb_nuts2
)

df_va_p_2030_delta_r_ielcb_nuts2 = (
    df_va_p_2030_scen_ielcb_nuts2 / df_va_p_2030_base_ielcb_nuts2
) - 1

rw.write_var_nuts2(
    df_va_p_2030_scen_ielcb_nuts2, cfg.file_name_va_p_2030_scen_ielcb_nuts2
)

rw.write_var_nuts2(
    df_va_p_2030_base_ielcb_nuts2, cfg.file_name_va_p_2030_base_ielcb_nuts2
)

rw.write_var_nuts2(
    df_va_p_2030_delta_ielcb_nuts2, cfg.file_name_va_p_2030_delta_ielcb_nuts2
)

rw.write_var_nuts2(
    df_va_p_2030_delta_r_ielcb_nuts2, cfg.file_name_va_p_2030_delta_r_ielcb_nuts2
)


rw.write_var_excel(df_va_p_2030_base_ielcb_nuts2,
                   cfg.file_name_va_p_2030_base_ielcb_nuts2[:-4],
                   wb_full,
                   unstack=0)

rw.write_var_excel(df_va_p_2030_scen_ielcb_nuts2,
                   cfg.file_name_va_p_2030_scen_ielcb_nuts2[:-4],
                   wb_full,
                   unstack=0)

rw.write_var_excel(df_va_p_2030_delta_ielcb_nuts2,
                   cfg.file_name_va_p_2030_delta_ielcb_nuts2[:-4],
                   wb_full,
                   unstack=0)

rw.write_var_excel(df_va_p_2030_delta_r_ielcb_nuts2,
                   cfg.file_name_va_p_2030_delta_r_ielcb_nuts2[:-4],
                   wb_full,
                   unstack=0)

rw.write_var_excel(df_va_p_2030_delta_r_ielcb_nuts2,
                   cfg.file_name_va_p_2030_delta_r_ielcb_nuts2[:-4],
                   wb_delta_r,
                   unstack=0)

"""
Disaggregate employment to NUTS-2.
"""
# For each EU28 country,
# disagg value added over nuts2 acc to bm prod frac in base
df_emp_2030_base_ielcb_nuts2 = rc.calc_d_cntr_nuts2_ielcb(
    df_emp_2030_base, df_prod_nuts2_2030_base_s_bm_r
)

# For each EU28 country,
# disagg value added over nuts2 acc to bm prod frac in scen
df_emp_2030_scen_ielcb_nuts2 = rc.calc_d_cntr_nuts2_ielcb(
    df_emp_2030_scen, df_prod_nuts2_2030_scen_s_bm_r
)

df_emp_2030_delta_ielcb_nuts2 = (
    df_emp_2030_scen_ielcb_nuts2 - df_emp_2030_base_ielcb_nuts2
)

df_emp_2030_delta_r_ielcb_nuts2 = (
    df_emp_2030_scen_ielcb_nuts2 / df_emp_2030_base_ielcb_nuts2
) - 1


rw.write_var_nuts2(
    df_emp_2030_base_ielcb_nuts2, cfg.file_name_emp_2030_base_ielcb_nuts2
)

rw.write_var_nuts2(
    df_emp_2030_scen_ielcb_nuts2, cfg.file_name_emp_2030_scen_ielcb_nuts2
)

rw.write_var_nuts2(
    df_emp_2030_delta_ielcb_nuts2, cfg.file_name_emp_2030_delta_ielcb_nuts2
)

rw.write_var_nuts2(
    df_emp_2030_delta_r_ielcb_nuts2, cfg.file_name_emp_2030_delta_r_ielcb_nuts2
)


rw.write_var_excel(df_emp_2030_base_ielcb_nuts2,
                   cfg.file_name_emp_2030_base_ielcb_nuts2[:-4],
                   wb_full,
                   unstack=0)

rw.write_var_excel(df_emp_2030_scen_ielcb_nuts2,
                   cfg.file_name_emp_2030_scen_ielcb_nuts2[:-4],
                   wb_full,
                   unstack=0)

rw.write_var_excel(df_emp_2030_delta_ielcb_nuts2,
                   cfg.file_name_emp_2030_delta_ielcb_nuts2[:-4],
                   wb_full,
                   unstack=0)

rw.write_var_excel(df_emp_2030_delta_r_ielcb_nuts2,
                   cfg.file_name_emp_2030_delta_r_ielcb_nuts2[:-4],
                   wb_full,
                   unstack=0)

rw.write_var_excel(df_emp_2030_delta_r_ielcb_nuts2,
                   cfg.file_name_emp_2030_delta_r_ielcb_nuts2[:-4],
                   wb_delta_r,
                   unstack=0)

# Plot results.
if plot:
    plt.close("all")

    gdf_eu_gb = rr.read_gdf_eu(version='globiom')
    gdf_eu_gb.plot()

    gdf_eu_cm = rr.read_gdf_eu(version='circumat')
    gdf_eu_cm.plot()

    l_var = [
        ("va_p_2030_base_ielcb_nuts2", df_va_p_2030_base_ielcb_nuts2),
        # ("va_p_2030_scen_ielcb_nuts2", df_va_p_2030_scen_ielcb_nuts2),
        ("va_p_2030_delta_ielcb_nuts2", df_va_p_2030_delta_ielcb_nuts2),
        # ("va_p_2030_delta_r_ielcb_nuts2", df_va_p_2030_delta_r_ielcb_nuts2),
        ("emp_2030_base_ielcb_nuts2", df_emp_2030_base_ielcb_nuts2),
        # ("emp_2030_scen_ielcb_nuts2", df_emp_2030_scen_ielcb_nuts2),
        ("emp_2030_delta_ielcb_nuts2", df_emp_2030_delta_ielcb_nuts2),
        # ("emp_2030_delta_r_ielcb_nuts2", df_emp_2030_delta_r_ielcb_nuts2)
        ]

    plt.close('all')

    df_va_p_2030_delta_u = df_va_p_2030_delta.unstack()
    df_emp_2030_delta_u = df_emp_2030_delta.unstack()

    df_va_p_2030_nuts2_base = rc.var_cntr2nuts(df_va_p_2030_base)
    df_va_p_2030_nuts2_scen = rc.var_cntr2nuts(df_va_p_2030_scen)
    df_va_p_2030_nuts2_delta = rc.var_cntr2nuts(df_va_p_2030_delta)

    gdf_va_p_2030_nuts2_base = rw.var2gdf_cm(gdf_eu_cm,
                                             df_va_p_2030_nuts2_base)

    rw.plot_gdf_cm(gdf_va_p_2030_nuts2_base,
                   df_va_p_2030_nuts2_base,
                   scen='base')

    gdf_va_p_2030_nuts2_scen = rw.var2gdf_cm(gdf_eu_cm,
                                             df_va_p_2030_nuts2_scen)

    rw.plot_gdf_cm(gdf_va_p_2030_nuts2_scen,
                   df_va_p_2030_nuts2_scen,
                   scen='scen')

    gdf_va_p_2030_nuts2_delta = rw.var2gdf_cm(gdf_eu_cm,
                                              df_va_p_2030_nuts2_delta)

    rw.plot_gdf_cm(gdf_va_p_2030_nuts2_delta,
                   df_va_p_2030_nuts2_delta,
                   scen='delta')

    fig = plt.figure(figsize=rw.cm2inch((36/2, 281/3)), dpi=400)
    g = sns.heatmap(df_va_p_2030_nuts2_delta, cmap='coolwarm', square=True, center=0)
    g.set_facecolor('lightgrey')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(cfg.RESULT_PNG_DIR_PATH + 'va_p_2030_nuts2_delta')

    fig = plt.figure(figsize=rw.cm2inch((16, 14)), dpi=400)
    g = sns.heatmap(df_va_p_2030_delta_u.T, cmap='coolwarm', square=True, center=0)
    g.set_facecolor('lightgrey')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(cfg.RESULT_PNG_DIR_PATH + 'va_p_2030_delta_u_world')

    fig = plt.figure(figsize=rw.cm2inch((16, 14)), dpi=400)
    g = sns.heatmap(df_emp_2030_delta_u.T, cmap='coolwarm', square=True, center=0)
    g.set_facecolor('lightgrey')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(cfg.RESULT_PNG_DIR_PATH + 'emp_2030_delta_u_world')

    fig = plt.figure(figsize=rw.cm2inch((16, 16)), dpi=cfg.dpi)
    for t_var_id, t_var in enumerate(l_var):
        plot_id = t_var_id+1
        plot_loc = 220+plot_id
        ax = fig.add_subplot(plot_loc)

        var_name, var_df = t_var
        var_gdf = rw.globiom2gdf_nuts2(
            var_df, var_name, gdf_eu_gb
        )
        if 'delta' in var_name:
            cmap = 'coolwarm'
            cmap_name = cmap
            vmin = int(np.floor(-var_gdf.max()))
            vmax = int(np.ceil(var_gdf.max()))
        else:
            cmap_name = "crest"
            cmap = sns.color_palette(cmap_name, as_cmap=True)

            vmin = int(np.floor(var_gdf.min()))
            vmax = int(np.ceil(var_gdf.max()))

        gdf_eu_gb[var_name] = var_gdf
        gdf_eu_gb.plot(column=var_name,
                       missing_kwds={"color": "lightgrey"},
                       legend=True,
                       legend_kwds={'ticks': [vmin,
                                              vmax]},
                       cmap=cmap,
                       vmin=vmin,
                       vmax=vmax,
                       ax=ax)
        plt.axis('off')
    plt.tight_layout()
    plt.savefig(cfg.RESULT_PNG_DIR_PATH + 'eu28')

rw.save_wb(wb_full, cfg.RESULT_XLSX_DIR_PATH + cfg.file_name_excel_full)

rw.save_wb(wb_delta_r, cfg.RESULT_XLSX_DIR_PATH + cfg.file_name_excel_delta_r)

rw.save_wb(wb_base_na_data,
           cfg.RESULT_XLSX_DIR_PATH + cfg.file_name_excel_base_na_data)

rw.close_wb()
