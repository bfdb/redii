# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:08:43 2020

@author: bfdeboer
"""

import csv
import geopandas as gpd
import numpy as np
import pandas as pd

import cfg
import gdxr


def read_gdx(file_path, var_name):
    with gdxr.GdxFile(file_path) as f:
        df_var = f[var_name]
    return df_var


def get_ind_out_ielcb(file_path_eu28, var_name_ind_out):
    df_ind_out = read_gdx(file_path_eu28, var_name_ind_out)
    df_ind_out_pelca = df_ind_out.loc[:,'iELCB',]
    df_ind_out_pelca_2030 = df_ind_out_pelca.loc[:,'2030']
    return df_ind_out_pelca_2030


def get_imp_pelca(file_path_eu28, var_name_imp):
    df_imp = read_gdx(file_path_eu28, var_name_imp)
    df_imp_pelca = df_imp.loc['pELCA',:,:]
    df_imp_pelca_2030 = df_imp_pelca[:,'2030']
    return df_imp_pelca_2030


def find_imp_pelca_missing_val(df_ind_out_ielcb, df_imp_pelca):
    l_ind_out_t_cntr_yr = list(df_ind_out_ielcb.index)
    l_imp_t_cntr_yr = list(df_imp_pelca.index)
    l_missing_val = []
    for t_cntr_yr in l_ind_out_t_cntr_yr:
        if t_cntr_yr not in l_imp_t_cntr_yr:
            l_missing_val.append(t_cntr_yr)
    return l_missing_val


def read_va_yr(file_path, var_name, yr):
    df_gdx = read_gdx(file_path, var_name)
    df_gdx_yr = df_gdx[:,:, str(yr)]
    return df_gdx_yr

def read_l_yr(file_path, var_name, yr):
    df_gdx = read_gdx(file_path, var_name)
    df_gdx_yr = df_gdx[:,:, str(yr)]
    return df_gdx_yr

def read_gdf_world():
    gdf_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Fix missing ISO3 values.
    gdf_world.loc[gdf_world['name'] == 'France', 'iso_a3'] = 'FRA'
    gdf_world.loc[gdf_world['name'] == 'Norway', 'iso_a3'] = 'NOR'
    gdf_world.loc[gdf_world['name'] == 'Somaliland', 'iso_a3'] = 'SOM'
    gdf_world.loc[gdf_world['name'] == 'Kosovo', 'iso_a3'] = 'RKS'
    gdf_world.loc[gdf_world['name'] == 'N. Cyprus', 'iso_a3'] = 'CYP'

    gdf_world = gdf_world[(gdf_world.name != "Antarctica") &
                          (gdf_world.name != "Fr. S. Antarctic Lands")]
    gdf_world = gdf_world.to_crs('+proj=wintri')

    return gdf_world

def read_gdf_eu():
    return gpd.read_file('../input/NUTS_RG_20M_2003_3035_LEVL_2.shp')


def fill_na_base(df_prod_nuts2_2030_base_na, df_prod_nuts2_2030_scen):

    d_prod_nuts2_2030_base = df_prod_nuts2_2030_base_na.to_dict()
    d_prod_nuts2_2030_scen = df_prod_nuts2_2030_scen.to_dict()

    d_prod_nuts2_2030_base_fillna = {}
    for row in d_prod_nuts2_2030_scen:
        if row not in d_prod_nuts2_2030_base:
            d_prod_nuts2_2030_base_fillna[row] = np.nan
        else:
            d_prod_nuts2_2030_base_fillna[row] = d_prod_nuts2_2030_base[row]

    return pd.Series(d_prod_nuts2_2030_base_fillna)


# Read mapping from ISO2 to ISO3 country codes.
def read_iso2_iso3():
    d_iso2_iso3 = {}
    with open(cfg.INPUT_DIR_PATH + 'iso2_iso3.txt', 'r') as read_file:
        csv_file = csv.reader(read_file, delimiter='\t')
        for row_id, row in enumerate(csv_file):
            if row_id:
                iso2, iso3 = row
                d_iso2_iso3[iso2] = iso3
    return d_iso2_iso3

# Read mapping from model to ISO2 EXIO countries and regions
def read_rox_iso2():
    d_cntr_redii2exio_iso2 = {}
    with open(cfg.INPUT_DIR_PATH+'cntr_exio2redii.txt', 'r') as read_file:
        csv_file = csv.reader(read_file, delimiter='\t')
        for row in csv_file:
            cntr_exio, cntr_redii = row
            if cntr_redii not in d_cntr_redii2exio_iso2:
                d_cntr_redii2exio_iso2[cntr_redii] = []
            d_cntr_redii2exio_iso2[cntr_redii].append(cntr_exio)
    return d_cntr_redii2exio_iso2


# Read ISO3 country codes from RoX regions.
def read_rox_iso3():
    d_cntr_rox2exio_iso3 = {}
    with open(cfg.INPUT_DIR_PATH+'cntr_exio_rox.txt', 'r') as read_file:
        csv_file = csv.reader(read_file, delimiter='\t')
        for row_id, row in enumerate(csv_file):
            if row_id:
                s_rox_name, s_rox, s_cntr_name, s_cntr_iso2, s_cntr_iso3 = row
                if s_rox not in d_cntr_rox2exio_iso3:
                    d_cntr_rox2exio_iso3[s_rox] = []
                d_cntr_rox2exio_iso3[s_rox].append(s_cntr_iso3)
    return d_cntr_rox2exio_iso3

# Map model RoX regions to ISO3 country codes.
def redii_iso3():
    d_iso2_iso3 = read_iso2_iso3()
    d_cntr_redii2exio_iso2 = read_rox_iso2()
    d_cntr_rox2exio_iso3 = read_rox_iso3()
    # Map model non RoX countries from ISO2 to ISO3 country codes.
    d_cntr_redii2exio_iso3 = {}
    for cntr_redii in d_cntr_redii2exio_iso2:
        d_cntr_redii2exio_iso3[cntr_redii] = []
        for cntr_exio_iso2 in d_cntr_redii2exio_iso2[cntr_redii]:
            if cntr_exio_iso2 in d_iso2_iso3:
                cntr_exio_iso3 = d_iso2_iso3[cntr_exio_iso2]
                d_cntr_redii2exio_iso3[cntr_redii].append(cntr_exio_iso3)
    for cntr_redii in d_cntr_redii2exio_iso2:
        for cntr_exio in d_cntr_redii2exio_iso2[cntr_redii]:
            if cntr_exio in d_cntr_rox2exio_iso3:
                for cntr_rox_iso3 in d_cntr_rox2exio_iso3[cntr_exio]:
                    d_cntr_redii2exio_iso3[cntr_redii].append(cntr_rox_iso3)

    return d_cntr_redii2exio_iso3