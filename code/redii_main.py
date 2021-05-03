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
import redii_read as rr
import redii_calc as rc
import redii_write as rw
import utils as ut

ut.makedirs()
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


# # Fill missing values in baseline.
# df_prod_nuts2_2030_base = rr.fill_base(
#     df_prod_nuts2_2030_base_na, df_prod_nuts2_2030_scen, "scen"
# )

# Fill missing values in baseline.
df_prod_nuts2_2030_base, df_base_na_scen_data = rr.fill_base(
    df_prod_nuts2_2030_base_na, df_prod_nuts2_2030_scen, fill_na_val=0
)

# Harmonize order of columns.
df_prod_nuts2_2030_scen_u = df_prod_nuts2_2030_scen.unstack()
df_prod_nuts2_2030_base_u = df_prod_nuts2_2030_base.unstack()
df_prod_nuts2_2030_base_u = df_prod_nuts2_2030_base_u[df_prod_nuts2_2030_scen_u.columns]
df_prod_nuts2_2030_base = df_prod_nuts2_2030_base_u.stack(dropna=False)
df_prod_nuts2_2030_scen = df_prod_nuts2_2030_scen_u.stack(dropna=False)

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
plt.close("all")

# rw.plot_redii_world(df_va_p_2030_cntr_base, "va_p_2030_cntr_base_world")

# rw.plot_redii_world(df_va_p_2030_cntr_delta, "va_p_2030_cntr_delta_world")

# rw.plot_redii_world(df_va_p_2030_cntr_delta_r, "va_p_2030_cntr_delta_world_r")

gdf_eu = rr.read_gdf_eu()
gdf_eu.plot()


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

# l_cmap = ['seismic',
#           'coolwarm',
#           'Spectral']

# for cmap in l_cmap:

plt.close('all')

df_va_p_2030_delta_u = df_va_p_2030_delta.unstack()
df_emp_2030_delta_u = df_emp_2030_delta.unstack()

###
# begin full sort
df_va_p_2030_delta_u = df_va_p_2030_delta.unstack()
d_va_p_2030_delta = df_va_p_2030_delta.to_dict()
d_va_p_2030_delta_abs = {}
d_va_p_2030_delta_reg = {}
d_va_p_2030_delta_ind = {}
val_abs_sum = 0
for t_reg_ind in d_va_p_2030_delta:
    reg, ind = t_reg_ind
    val_abs = abs(d_va_p_2030_delta[t_reg_ind])
    if reg not in d_va_p_2030_delta_reg:
        d_va_p_2030_delta_reg[reg] = 0
    if ind not in d_va_p_2030_delta_ind:
        d_va_p_2030_delta_ind[ind] = 0
    d_va_p_2030_delta_reg[reg] += val_abs
    d_va_p_2030_delta_ind[ind] += val_abs
    d_va_p_2030_delta_abs[t_reg_ind] = val_abs
    val_abs_sum += val_abs
    print(reg, ind)

d = d_va_p_2030_delta_abs
l_sort = sorted(d.items(),
                key=operator.itemgetter(1),
                reverse=True)

l_sort_abs_rel = []
val_abs_rel_cum = 0
val_abs_rel_cum_thresh = 0.8
for t_reg_ind_val in l_sort:
    (reg, ind), val_abs = t_reg_ind_val
    val_abs_rel = val_abs/val_abs_sum
    val_abs_rel_cum += val_abs_rel
    print(val_abs_rel_cum)
    l_sort_abs_rel.append(((reg, ind), val_abs_rel))


def sort(d):
    l_sort = sorted(d.items(),
                    key=operator.itemgetter(1),
                    reverse=True)
    l_sort_idx = []
    for t_idx_val in l_sort:
        idx, val = t_idx_val
        l_sort_idx.append(idx)
    return l_sort_idx


l_va_p_2030_delta_reg_sort = sort(d_va_p_2030_delta_reg)
l_va_p_2030_delta_ind_sort = sort(d_va_p_2030_delta_ind)
df_va_p_2030_delta_u = df_va_p_2030_delta_u[l_va_p_2030_delta_ind_sort]
df_va_p_2030_delta_u = df_va_p_2030_delta_u.reindex(l_va_p_2030_delta_reg_sort)
# end full sort
###

# ###
# # begin threshold sort
# df_va_p_2030_delta_u = df_va_p_2030_delta.unstack()
# d_va_p_2030_delta = df_va_p_2030_delta.to_dict()
# d_va_p_2030_delta_abs = {}
# d_va_p_2030_delta_reg = {}
# d_va_p_2030_delta_ind = {}
# val_abs_sum = 0
# for t_reg_ind in d_va_p_2030_delta:
#     reg, ind = t_reg_ind
#     val_abs = abs(d_va_p_2030_delta[t_reg_ind])
#     d_va_p_2030_delta_abs[t_reg_ind] = val_abs
#     val_abs_sum += val_abs
#     print(reg, ind)

# d = d_va_p_2030_delta_abs
# l_sort = sorted(d.items(),
#                 key=operator.itemgetter(1),
#                 reverse=True)

# l_sort_abs_rel = []
# l_sort_abs_rel_cum = []
# d_sort_abs_rel_reg = {}
# d_sort_abs_rel_ind = {}
# val_abs_rel_cum = 0
# val_abs_rel_cum_thresh = 1.0
# for t_reg_ind_val in l_sort:
#     (reg, ind), val_abs = t_reg_ind_val
#     val_abs_rel = val_abs/val_abs_sum
#     val_abs_rel_cum += val_abs_rel
#     if val_abs_rel_cum <= val_abs_rel_cum_thresh:
#         print(val_abs_rel_cum)
#         l_sort_abs_rel.append(((reg, ind), val_abs_rel))
#         if reg not in d_sort_abs_rel_reg:
#             d_sort_abs_rel_reg[reg] = 0
#         if ind not in d_sort_abs_rel_ind:
#             d_sort_abs_rel_ind[ind] = 0
#         d_sort_abs_rel_reg[reg] += val_abs_rel
#         d_sort_abs_rel_ind[ind] += val_abs_rel
#         l_sort_abs_rel_cum.append(val_abs_rel_cum)


# def sort(d):
#     l_sort = sorted(d.items(),
#                     key=operator.itemgetter(1),
#                     reverse=True)
#     l_sort_idx = []
#     for t_idx_val in l_sort:
#         idx, val = t_idx_val
#         l_sort_idx.append(idx)
#     return l_sort_idx


# l_va_p_2030_delta_reg_sort = sort(d_sort_abs_rel_reg)
# l_va_p_2030_delta_ind_sort = sort(d_sort_abs_rel_ind)
# df_va_p_2030_delta_u = df_va_p_2030_delta_u[l_va_p_2030_delta_ind_sort]
# df_va_p_2030_delta_u = df_va_p_2030_delta_u.reindex(l_va_p_2030_delta_reg_sort)
# # end threshold sort
# ###


fig = plt.figure(figsize=rw.cm2inch((16, 14)), dpi=400)
# plt.rcParams['font.size'] = 7.0
g = sns.heatmap(df_va_p_2030_delta_u.T, cmap='coolwarm', square=True, center=0)
g.set_facecolor('lightgrey')
# g.yaxis.set_ticks_position("right")
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(cfg.RESULT_PNG_DIR_PATH + 'va_p_2030_delta_u_world')

fig = plt.figure(figsize=rw.cm2inch((16, 14)), dpi=400)
# plt.rcParams['font.size'] = 7.0
g = sns.heatmap(df_emp_2030_delta_u.T, cmap='coolwarm', square=True, center=0)
g.set_facecolor('lightgrey')
# g.yaxis.set_ticks_position("right")
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
        var_df, var_name, gdf_eu
    )
    if 'delta' in var_name:
        cmap = 'coolwarm'
        cmap_name = cmap
        vmin = int(np.floor(-var_gdf.max()))
        vmax = int(np.ceil(var_gdf.max()))
    else:
        # cmap_name = 'viridis'
        # cmap = cmap_name

        # cmap_name = "flare"
        # cmap = sns.color_palette(cmap_name, as_cmap=True)

        cmap_name = "crest"
        cmap = sns.color_palette(cmap_name, as_cmap=True)

        vmin = int(np.floor(var_gdf.min()))
        vmax = int(np.ceil(var_gdf.max()))

    gdf_eu[var_name] = var_gdf
    gdf_eu.plot(column=var_name,
                missing_kwds={"color": "lightgrey"},
                legend=True,
                legend_kwds={'ticks': [vmin,
                                       # int((vmin+vmax)/2),
                                       vmax]},
                cmap=cmap,
                vmin=vmin,
                vmax=vmax,
                ax=ax)
    plt.axis('off')
    # plt.tight_layout()
    # plt.savefig(cfg.RESULT_PNG_DIR_PATH + f"{cfg.DATE}_{var_name}_{cmap_name}")
plt.tight_layout()
plt.savefig(cfg.RESULT_PNG_DIR_PATH + 'eu28')

rw.save_wb(wb_full, cfg.RESULT_XLSX_DIR_PATH + cfg.file_name_excel_full)

rw.save_wb(wb_delta_r, cfg.RESULT_XLSX_DIR_PATH + cfg.file_name_excel_delta_r)

rw.save_wb(wb_base_na_data,
           cfg.RESULT_XLSX_DIR_PATH + cfg.file_name_excel_base_na_data)

rw.close_wb()
