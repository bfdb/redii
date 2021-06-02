# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:08:43 2020

@author: bfdeboer
"""

import csv
import gdxr
import geopandas as gpd
import numpy as np
import os
import pandas as pd
import pickle

import cfg
import exiobase as eb
import utils as ut


def read_eb_proc(t_eb_proc):
    """ Read Input-Output tables from EXIOBASE.'

    """
    ut.log('Reading Input-Output tables from EXIOBASE.')
    eb_dir_path, eb_file_name = t_eb_proc
    # If EXIOBASE has already been parsed, read the pickle.
    if eb_file_name in os.listdir(cfg.DATA_DIR_PATH):
        d_eb_proc = pickle.load(
            open(cfg.DATA_DIR_PATH+eb_file_name,
                 'rb'))
    # Else, parse and process EXIOBASE and optionally save for future runs
    else:
        d_eb_proc = eb.process(eb.parse(eb_dir_path))
        if cfg.SAVE_EB:
            pickle.dump(d_eb_proc,
                        open(cfg.DATA_DIR_PATH+eb_file_name,
                             'wb'))
    return d_eb_proc


def read_gdx(file_path, var_name):
    ut.log(f'Read {var_name} from gdx.')
    with gdxr.GdxFile(file_path) as f:
        df_var = f[var_name]
    return df_var


def read_exec_date(file_path, var_name):
    ar_exec_date = read_gdx(file_path, var_name)
    str_exec_date = str(ar_exec_date.astype(str)[0])
    (str_exec_date_mm, str_exec_date_dd, str_exec_date_yy) = str_exec_date.split("/")
    str_exec_date_yyyy = "".join(["20", str_exec_date_yy])
    t_exec_date = (str_exec_date_yyyy, str_exec_date_mm, str_exec_date_dd)
    return t_exec_date


def read_exec_time(file_path, var_name):
    ar_exec_time = read_gdx(file_path, var_name)
    str_exec_time = str(ar_exec_time.astype(str)[0])
    (str_exec_time_hh, str_exec_time_mm, str_exec_time_ss) = str_exec_time.split(":")
    t_exec_time = (str_exec_time_hh, str_exec_time_mm, str_exec_time_ss)
    return t_exec_time


def get_emp_c():
    ut.log('Get employment coefficients.s')
    df_y_p_2011_base = read_va_yr(
        cfg.DATA_SHARE_DIR_PATH + cfg.EXIOMOD_DIR_PATH + cfg.file_name_base_eu28,
        cfg.var_name_y_time_p,
        cfg.yr_start,
    )

    df_emp_2011 = read_emp(
        cfg.DATA_SHARE_DIR_PATH + cfg.EXIOMOD_DIR_PATH + cfg.file_name_base_eu28,
        cfg.var_name_emp,
    )

    df_emp_c = df_emp_2011 / df_y_p_2011_base
    return df_emp_c


def read_emp(file_name, var_name):
    df_emp = read_gdx(file_name, var_name)
    df_emp_s_gender_skill = df_emp.sum(level=[0, 1])
    return df_emp_s_gender_skill


def get_missing_emp_data(df_y_p_2011_base, df_emp_2011, df_emp_2011_c):
    idx_df_y_p_2011_base = list(df_y_p_2011_base.index)
    idx_df_emp_2011 = list(df_emp_2011.index)
    idx_df_emp_2011_c = list(df_emp_2011_c.index)

    for idx in idx_df_emp_2011_c:
        if idx not in idx_df_y_p_2011_base:
            print("{} not in industry output".format(idx))
        if idx not in idx_df_emp_2011:
            print("{} not in employment".format(idx))


def read_exec_datetime(file_path):
    t_exec_date = read_exec_date(file_path, cfg.var_name_exec_date)
    t_exec_time = read_exec_time(file_path, cfg.var_name_exec_time)
    t_exec_datetime = (t_exec_date, t_exec_time)
    return t_exec_datetime


def get_ind_out_ielcb(file_path_eu28, var_name_ind_out):
    df_ind_out = read_gdx(file_path_eu28, var_name_ind_out)
    df_ind_out_pelca = df_ind_out.loc[
        :, "iELCB",
    ]
    df_ind_out_pelca_2030 = df_ind_out_pelca.loc[:, "2030"]
    return df_ind_out_pelca_2030


def get_imp_pelca(file_path_eu28, var_name_imp):
    df_imp = read_gdx(file_path_eu28, var_name_imp)
    df_imp_pelca = df_imp.loc["pELCA", :, :]
    df_imp_pelca_2030 = df_imp_pelca[:, "2030"]
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
    ut.log('Reading EXIOMOD input.')
    df_gdx = read_gdx(file_path, var_name)
    df_gdx_yr = df_gdx[:, :, str(yr)]
    return df_gdx_yr


def read_l_yr(file_path, var_name, yr):
    df_gdx = read_gdx(file_path, var_name)
    df_gdx_yr = df_gdx[:, :, str(yr)]
    return df_gdx_yr


def read_gdf_world():
    gdf_world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    # Fix missing ISO3 values.
    gdf_world.loc[gdf_world["name"] == "France", "iso_a3"] = "FRA"
    gdf_world.loc[gdf_world["name"] == "Norway", "iso_a3"] = "NOR"
    gdf_world.loc[gdf_world["name"] == "Somaliland", "iso_a3"] = "SOM"
    gdf_world.loc[gdf_world["name"] == "Kosovo", "iso_a3"] = "RKS"
    gdf_world.loc[gdf_world["name"] == "N. Cyprus", "iso_a3"] = "CYP"

    gdf_world = gdf_world[
        (gdf_world.name != "Antarctica") & (gdf_world.name != "Fr. S. Antarctic Lands")
    ]
    gdf_world = gdf_world.to_crs("+proj=wintri")

    return gdf_world


def read_gdf_eu(version):
    if version == 'globiom':
        return gpd.read_file(cfg.input_path + cfg.file_name_nuts2_shp_globiom)
    elif version == 'circumat':
        return gpd.read_file(cfg.input_path + cfg.file_name_nuts2_shp_cm)


def fill_base(df_prod_nuts2_2030_base_na, df_prod_nuts2_2030_scen, fill_na_val):
    ut.log(f'Fill missing values in baseline with {fill_na_val}')
    d_prod_nuts2_2030_base = df_prod_nuts2_2030_base_na.to_dict()
    d_prod_nuts2_2030_scen = df_prod_nuts2_2030_scen.to_dict()

    d_prod_nuts2_2030_base_fillna = {}

    d_base_na_scen_data = {}
    for row in d_prod_nuts2_2030_scen:
        if row not in d_prod_nuts2_2030_base:
            if fill_na_val == "scen":
                val_fill = d_prod_nuts2_2030_scen[row]
            else:
                val_fill = fill_na_val
            d_prod_nuts2_2030_base_fillna[row] = val_fill

            d_base_na_scen_data[row] = d_prod_nuts2_2030_scen[row]
        else:
            d_prod_nuts2_2030_base_fillna[row] = d_prod_nuts2_2030_base[row]

    return pd.Series(d_prod_nuts2_2030_base_fillna), pd.Series(d_base_na_scen_data)


# Read mapping from ISO2 to ISO3 country codes.
def read_iso2_iso3():
    d_iso2_iso3 = {}
    with open(cfg.INPUT_DIR_PATH + "iso2_iso3.txt", "r") as read_file:
        csv_file = csv.reader(read_file, delimiter="\t")
        for row_id, row in enumerate(csv_file):
            if row_id:
                iso2, iso3 = row
                d_iso2_iso3[iso2] = iso3
    return d_iso2_iso3


# Read mapping from model to ISO2 EXIO countries and regions
def read_rox_iso2():
    d_cntr_redii2exio_iso2 = {}
    with open(cfg.INPUT_DIR_PATH + "cntr_exio2redii.txt", "r") as read_file:
        csv_file = csv.reader(read_file, delimiter="\t")
        for row in csv_file:
            cntr_exio, cntr_redii = row
            if cntr_redii not in d_cntr_redii2exio_iso2:
                d_cntr_redii2exio_iso2[cntr_redii] = []
            d_cntr_redii2exio_iso2[cntr_redii].append(cntr_exio)
    return d_cntr_redii2exio_iso2


# Read ISO3 country codes from RoX regions.
def read_rox_iso3():
    d_cntr_rox2exio_iso3 = {}
    with open(cfg.INPUT_DIR_PATH + "cntr_exio_rox.txt", "r") as read_file:
        csv_file = csv.reader(read_file, delimiter="\t")
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


def load_data(source, l_cntr):

    if 'eb' in source:
        if 'ixi' in source:
            print('use EXIOBASE ixi')
            eb_ver_name = cfg.T_EB_IXI_FPA_3_3_2011_PROC
        elif 'pxp' in source:
            print('use EXIOBASE pxp')
            eb_ver_name = cfg.T_EB_PXP_ITA_3_3_2011_PROC

        d_eb_proc = read_eb_proc(eb_ver_name)

        df_a_mr = d_eb_proc['cA']
        df_y_mr = d_eb_proc['tY']
        df_v_mr = d_eb_proc['cV']

    elif source == 'cm':
        print('use circumat')

        # use exiobase pxp data for labels
        eb_ver_name = cfg.T_EB_PXP_ITA_3_3_2011_PROC
        d_eb_proc = read_eb_proc(eb_ver_name)

        # use circumat data.

        data_folder = cfg.INPUT_DIR_PATH+'cm/'

        A_mr = np.load(data_folder+"A_v4.npy")
        Y_mr = np.load(data_folder+"Y_v4.npy")

        df_a_mr = pd.DataFrame(A_mr,
                               index=d_eb_proc['cA'].index,
                               columns=d_eb_proc['cA'].columns)

        df_y_mr = pd.DataFrame(Y_mr,
                               index=d_eb_proc['tY'].index,
                               columns=d_eb_proc['tY'].columns)

        df_v_mr = d_eb_proc['cV']

    df_a_mr_cntr = df_a_mr[l_cntr].loc[l_cntr]
    df_y_mr_cntr = df_y_mr[l_cntr].loc[l_cntr]
    df_v_mr_cntr = df_v_mr[l_cntr]
    return df_a_mr_cntr, df_y_mr_cntr, df_v_mr_cntr


def read_d_cv_cat():
    """ Read socio-economic impact categories.'

    """
    ut.log('Reading socio-economic impact categories.')
    dict_impact = {}
    list_fp_type = ['emp', 'va']
    for fp_type in list_fp_type:
        dict_impact[fp_type] = []
        fp_file_name = cfg.D_FP_FILE_NAME[fp_type]
        with open(cfg.INPUT_DIR_PATH+fp_file_name) as read_file:
            csv_file = csv.reader(read_file, delimiter='\t')
            for row in csv_file:
                dict_impact[fp_type].append(tuple(row))
    return dict_impact


def read_d_x_cm():
    return pickle.load(open(cfg.INPUT_DIR_PATH+'d_x.pkl', 'rb'))


def read_ind_cm2em():
    df_eb_ind_code2em_ind_agg = (pd.read_csv(cfg.INPUT_DIR_PATH +
                                             cfg.EB_IND_CODE2EM_IND_AGG_FILE_NAME,
                                             sep='\t',
                                             index_col=[0, 1],
                                             header=[0]))
    df_eb_ind_code2em_ind_agg = df_eb_ind_code2em_ind_agg.droplevel(axis=0,
                                                                    level=0)
    return df_eb_ind_code2em_ind_agg
