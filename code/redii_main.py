# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:08:15 2020

@author: bfdeboer
"""

import csv
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import cfg
import redii_read as rr
import redii_calc as rc
import redii_write as rw
import utils as ut

ut.makedirs()
# Read value added from baseline and EUCO3232.5.
df_va_p_2030_base = rr.read_va_yr(
    cfg.DATA_DIR_PATH+cfg.EXIOMOD_DIR_PATH+cfg.file_name_base_eu28,
    cfg.var_name_va_p_new,
    cfg.yr_end)

df_va_p_2030_scen = rr.read_va_yr(
    cfg.DATA_DIR_PATH+cfg.EXIOMOD_DIR_PATH+cfg.file_name_scen_eu28,
    cfg.var_name_va_p_new,
    cfg.yr_end)

# Calculate relative difference between baseline and EUCO3232.5 scenario.
df_va_p_2030_delta = df_va_p_2030_scen - df_va_p_2030_base
df_va_p_2030_delta_r = df_va_p_2030_scen / df_va_p_2030_base-1

# Sum value added per country.
df_va_p_2030_cntr_base = df_va_p_2030_base.sum(level=0)
df_va_p_2030_cntr_scen = df_va_p_2030_scen.sum(level=0)

df_va_p_2030_cntr_delta = df_va_p_2030_cntr_scen - df_va_p_2030_cntr_base
df_va_p_2030_cntr_delta_r = df_va_p_2030_cntr_scen / df_va_p_2030_cntr_base-1

# Read biomass productivity from baseline and EUCO3232.5
df_out_nuts2 = rr.read_gdx(cfg.DATA_DIR_PATH+
                           cfg.GLOBIOM_DIR_PATH+
                           cfg.file_name_globiom_out,
                           'OUTPUT_NUTS2')

df_prod_nuts2_2030_base_na = df_out_nuts2['output_REF_7sept2020',
                                       'PROD',
                                       '1000 t',
                                       :,
                                       :,
                                       :,
                                       'SSP2',
                                       'REFERENCE',
                                       'REFERENCE',
                                       '2030']
df_prod_nuts2_2030_scen = df_out_nuts2['output_EUCO32_7sept2020',
                                       'PROD',
                                       '1000 t',
                                       :,
                                       :,
                                       :,
                                       'SSP2',
                                       'REFERENCE',
                                       'EUCO32',
                                       '2030']

# Fill missing values in baseline with NaN.
df_prod_nuts2_2030_base = rr.fill_na_base(df_prod_nuts2_2030_base_na,
                                         df_prod_nuts2_2030_scen)

# Sum over biomass
df_prod_nuts2_2030_base_s_bm = df_prod_nuts2_2030_base.sum(level=[0,1])
df_prod_nuts2_2030_scen_s_bm = df_prod_nuts2_2030_scen.sum(level=[0,1])
df_prod_nuts2_2030_delta_s_bm = (
    df_prod_nuts2_2030_scen_s_bm - df_prod_nuts2_2030_base_s_bm)
df_prod_nuts2_2030_delta_r_s_bm = (
    df_prod_nuts2_2030_scen_s_bm/df_prod_nuts2_2030_base_s_bm)-1

'''
For each EU28 country,
calc fraction of biomass prod per nuts2 region in base
'''
df_prod_nuts2_2030_base_s_bm_r = (
    rc.calc_d_cntr_nuts2_r(df_prod_nuts2_2030_base_s_bm))

'''
For each EU28 country,
disagg value added over nuts2 acc to bm prod frac in base
'''
df_va_p_2030_base_ielcb_nuts2 = (
    rc.calc_d_cntr_nuts2_va_ielcb(df_va_p_2030_base,
                               df_prod_nuts2_2030_base_s_bm_r))

'''
For each EU28 country,
calc fraction of biomassm prod per nuts2 region in scen
'''
df_prod_nuts2_2030_scen_s_bm_r = (
    rc.calc_d_cntr_nuts2_r(df_prod_nuts2_2030_scen_s_bm))

'''
For each EU28 country,
disagg value added over nuts2 acc to bm prod frac in scen
'''
df_va_p_2030_scen_ielcb_nuts2 = (
    rc.calc_d_cntr_nuts2_va_ielcb(df_va_p_2030_scen,
                               df_prod_nuts2_2030_scen_s_bm_r))

df_va_p_2030_delta_ielcb_nuts2 = (
    df_va_p_2030_scen_ielcb_nuts2 - df_va_p_2030_base_ielcb_nuts2)

df_va_p_2030_delta_r_ielcb_nuts2 = (
    df_va_p_2030_scen_ielcb_nuts2 / df_va_p_2030_base_ielcb_nuts2)-1

plt.close('all')

rw.plot_redii_world(df_va_p_2030_cntr_base,
                    'va_p_2030_cntr_base_world')

rw.plot_redii_world(df_va_p_2030_cntr_delta,
                    'va_p_2030_cntr_delta_world')

rw.plot_redii_world(df_va_p_2030_cntr_delta_r,
                    'va_p_2030_cntr_delta_world_r')

gdf_eu = rr.read_gdf_eu()

var = 'va_p_2030_base_ielcb_nuts2'
df_eu_va_p_2030_base_ielcb_nuts2 = rw.globiom2gdf_nuts2(df_va_p_2030_base_ielcb_nuts2,
                                                      var,
                                                      gdf_eu)

gdf_eu[var] = df_eu_va_p_2030_base_ielcb_nuts2
gdf_eu.plot(column = var,
            missing_kwds={'color':'lightgrey'})
plt.savefig(cfg.RESULT_PNG_DIR_PATH+'{}_{}'.format(cfg.DATE, var))


# Read employment from baseline and EUCO3232.5.
df_l_p_2030_base = rr.read_l_yr(
    cfg.DATA_DIR_PATH+cfg.EXIOMOD_DIR_PATH+cfg.file_name_base_eu28,
    cfg.var_name_l_time_p,
    cfg.yr_end)

df_l_p_2030_scen = rr.read_l_yr(
    cfg.DATA_DIR_PATH+cfg.EXIOMOD_DIR_PATH+cfg.file_name_scen_eu28,
    cfg.var_name_l_time_p,
    cfg.yr_end)

df_l_p_2030_delta = df_l_p_2030_scen - df_l_p_2030_base
df_l_p_2030_delta_r = df_l_p_2030_scen / df_l_p_2030_base - 1

###############################
# Read industry code and names in exio classification.
dict_ind_exio = {}
with open('../input/industries_database.txt', 'r') as read_file:
    csv_file = csv.reader(read_file, delimiter='\'')
    for row in csv_file:
        ind_exio, ind_exio_name, na = row
        ind_exio = ind_exio.strip()
        ind_exio_name = ind_exio_name.strip()
        if ind_exio_name[-1] == ')':
            ind_exio_name = ind_exio_name[:-5]
        dict_ind_exio[ind_exio] = ind_exio_name


# Read industry code to aggregate.
dict_ind_agg = {}
with open('../input/industries_database_to_model_redii.txt','r') as read_file:
    csv_file = csv.reader(read_file, delimiter='.')
    for row in csv_file:
        ind_exio, ind_agg = row
        if ind_agg not in dict_ind_agg:
            dict_ind_agg[ind_agg] = []
        dict_ind_agg[ind_agg].append(ind_exio)

# Generate dictionary from industry aggregate to exio names.
dict_ind_agg_name = {}
for ind_agg in dict_ind_agg:
    dict_ind_agg_name[ind_agg] = []
    for ind_exio in dict_ind_agg[ind_agg]:
        ind_exio_name = dict_ind_exio[ind_exio]
        dict_ind_agg_name[ind_agg].append(ind_exio_name)

# Generate dictionary with industry exio name to aggregate
dict_ind_exio_agg_name = {}
for ind_agg in dict_ind_agg_name:
    for ind_exio in dict_ind_agg_name[ind_agg]:
        dict_ind_exio_agg_name[ind_exio] = ind_agg

# Read factor inputs.
df = pd.read_csv('../input/mrFactorInputs_3.3_2011.txt',
                 sep='\t',
                 header=[0,1],
                 index_col=[0,1])

# Generate dictionary with factor inputs.
dict_va = {}
for df_ind in df.index:
    va, va_unit = df_ind
    if va_unit == '1000 p':
        dict_va[(va, va_unit)] = {}
        for df_col in df.columns:
            cntr, ind = df_col
            if cntr not in dict_va[(va, va_unit)]:
                dict_va[(va, va_unit)][cntr] = {}
            dict_va[(va, va_unit)][cntr][ind] = df.loc[df_ind,df_col]

# Generate dictionary with factor inputs
dict_va_ind_agg = {}
for va in dict_va:
    dict_va_ind_agg[va] = {}
    for cntr in dict_va[va]:
        if cntr not in dict_va_ind_agg[va]:
            dict_va_ind_agg[va][cntr] = {}
        for ind_exio in dict_va[va][cntr]:
            val = dict_va[va][cntr][ind_exio]
            ind_agg = dict_ind_exio_agg_name[ind_exio]
            if ind_agg not in dict_va_ind_agg[va][cntr]:
                dict_va_ind_agg[va][cntr][ind_agg] = 0
            dict_va_ind_agg[va][cntr][ind_agg] += val

dict_va_ind_agg_df = {}
for va in dict_va_ind_agg:
    dict_va_ind_agg_df[va] = {}
    for cntr in dict_va_ind_agg[va]:
        for ind in dict_va_ind_agg[va][cntr]:
            tup_cntr_ind = (cntr, ind)
            val = dict_va_ind_agg[va][cntr][ind]
            dict_va_ind_agg_df[va][tup_cntr_ind] = val

df_va_ind_agg = pd.DataFrame.from_dict(dict_va_ind_agg_df).T

dict_cntr_reg = {}
with open('../input/regions_all_database_to_model_redii.txt', 'r') as read_file:
    csv_file = csv.reader(read_file, delimiter='.')
    for row in csv_file:
        cntr, reg = row
        dict_cntr_reg[cntr] = reg

dict_va_reg_ind_agg = {}
for va in dict_va:
    dict_va_reg_ind_agg[va] = {}
    for cntr in dict_va[va]:
        reg = dict_cntr_reg[cntr]
        if reg not in dict_va_reg_ind_agg[va]:
            dict_va_reg_ind_agg[va][reg] = {}
        for ind_exio in dict_va[va][cntr]:
            val = dict_va[va][cntr][ind_exio]
            ind_agg = dict_ind_exio_agg_name[ind_exio]
            if ind_agg not in dict_va_reg_ind_agg[va][reg]:
                dict_va_reg_ind_agg[va][reg][ind_agg] = 0
            dict_va_reg_ind_agg[va][reg][ind_agg] += val

dict_emp_reg_ind_agg = {}
for va in dict_va_reg_ind_agg:
    for reg in dict_va_reg_ind_agg[va]:
        if reg not in dict_emp_reg_ind_agg:
            dict_emp_reg_ind_agg[reg] = {}
        for ind in dict_va_reg_ind_agg[va][reg]:
            if ind not in dict_emp_reg_ind_agg[reg]:
                dict_emp_reg_ind_agg[reg][ind] = 0
            val = dict_va_reg_ind_agg[va][reg][ind]
            dict_emp_reg_ind_agg[reg][ind] += val
