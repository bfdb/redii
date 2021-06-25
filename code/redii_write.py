# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 08:20:37 2020

@author: bfdeboer
"""

import csv
from matplotlib.colors import TwoSlopeNorm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xlwings as xw

import cfg
import redii_read as rr
import utils as ut


def cntr_redii_iso3(df, d_cntr_redii2exio_iso3):
    d_df = df.to_dict()
    d_df_iso3 = {}
    for cntr_redii in d_df:
        val = d_df[cntr_redii]
        for cntr_iso3 in d_cntr_redii2exio_iso3[cntr_redii]:
            d_df_iso3[cntr_iso3] = val

    return pd.Series(d_df_iso3)


def cntr_iso3_world(df, var, gdf_world):
    d_world = gdf_world.to_dict()
    d_world_var = {}
    d_world_var[var] = {}
    d_world_var = {}
    d_world_var[var] = {}
    for idx in d_world["iso_a3"]:
        cntr_iso3 = d_world["iso_a3"][idx]
        if cntr_iso3 in df:
            d_world_var[var][idx] = df[cntr_iso3]
    return pd.DataFrame(d_world_var)


def add_world_var(df, var, gdf_world):
    gdf_world[var] = df
    return gdf_world


def plot_world_var(gdf_world, var):
    vmin = min(gdf_world[var])
    vmax = max(gdf_world[var])
    if vmin < 0:
        norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)
        gdf_world.plot(
            column=var,
            legend=True,
            cmap=sns.color_palette("vlag", as_cmap=True),
            norm=norm,
        )
    else:
        gdf_world.plot(
            column=var, legend=True, cmap=sns.color_palette("crest", as_cmap=True)
        )
    plt.savefig(cfg.RESULT_PNG_DIR_PATH + "{}_{}".format(cfg.DATE, var))


def plot_redii_world(df_redii, var):
    gdf_world = rr.read_gdf_world()
    d_cntr_redii2exio_iso3 = rr.redii_iso3()
    df_iso3 = cntr_redii_iso3(df_redii, d_cntr_redii2exio_iso3)
    df_world = cntr_iso3_world(df_iso3, var, gdf_world)
    gdf_world = add_world_var(df_world, var, gdf_world)
    plot_world_var(gdf_world, var)


# Get countries from world gpd.
def write_gdf_world_cntr(gdf_world):
    d_world = gdf_world.to_dict()
    with open(cfg.INPUT_DIR_PATH + "cntr_gpd_world.txt", "w") as write_file:
        csv_file = csv.writer(write_file, delimiter="\t", lineterminator="\n")
        row_write = ["Name", "ISO A3", "Continent"]
        csv_file.writerow(row_write)
        for idx in d_world["continent"]:
            cntr_name = d_world["name"][idx]
            cntr_iso_a3 = d_world["iso_a3"][idx]
            cntr_cont = d_world["continent"][idx]
            row_write = [cntr_name, cntr_iso_a3, cntr_cont]
            csv_file.writerow(row_write)


def cntr_redii_iso3(df, d_cntr_redii2exio_iso3):
    d_df = df.to_dict()
    d_df_iso3 = {}
    for cntr_redii in d_df:
        val = d_df[cntr_redii]
        for cntr_iso3 in d_cntr_redii2exio_iso3[cntr_redii]:
            d_df_iso3[cntr_iso3] = val

    return pd.Series(d_df_iso3)


def cntr_iso3_world(df, var, gdf_world):
    d_world = gdf_world.to_dict()
    d_world_var = {}
    d_world_var[var] = {}
    d_world_var = {}
    d_world_var[var] = {}
    for idx in d_world["iso_a3"]:
        cntr_iso3 = d_world["iso_a3"][idx]
        if cntr_iso3 in df:
            d_world_var[var][idx] = df[cntr_iso3]
    return pd.DataFrame(d_world_var)


# def add_world_var(df, var, gdf_world):
#     gdf_world[var] = df
#     return gdf_world


# def plot_world_var(gdf_world, var):
#     vmin = min(gdf_world[var])
#     vmax = max(gdf_world[var])
#     if vmin < 0:
#         norm = TwoSlopeNorm(vmin = vmin, vcenter=0, vmax = vmax)
#         gdf_world.plot(column = var,
#                        legend = True,
#                        cmap = sns.color_palette("vlag", as_cmap=True),
#                        norm = norm)
#     else:
#         gdf_world.plot(column = var,
#                        legend = True,
#                        cmap = sns.color_palette("crest", as_cmap=True))
#     plt.savefig('{}_{}'.format(cfg.date, var))


# def plot_redii_world(df_redii, var):
#     gdf_world = rr.read_gdf_world()
#     d_cntr_redii2exio_iso3 = rr.redii_iso3()
#     df_iso3 = cntr_redii_iso3(df_redii, d_cntr_redii2exio_iso3)
#     df_world = cntr_iso3_world(df_iso3, var, gdf_world)
#     gdf_world = add_world_var(df_world,
#                               var,
#                               gdf_world)
#     plot_world_var(gdf_world, var)


# Get countries from world gpd.
def write_gdf_world_cntr(gdf_world):
    d_world = gdf_world.to_dict()
    with open(cfg.INPUT_DIR_PATH + "cntr_gpd_world.txt", "w") as write_file:
        csv_file = csv.writer(write_file, delimiter="\t", lineterminator="\n")
        row_write = ["Name", "ISO A3", "Continent"]
        csv_file.writerow(row_write)
        for idx in d_world["continent"]:
            cntr_name = d_world["name"][idx]
            cntr_iso_a3 = d_world["iso_a3"][idx]
            cntr_cont = d_world["continent"][idx]
            row_write = [cntr_name, cntr_iso_a3, cntr_cont]
            csv_file.writerow(row_write)


def globiom2gdf_nuts2(df, var, gdf_eu):
    gdf_eu_nuts2 = gdf_eu["NUTS2"]
    d_df = df.sum(level=1)
    d_eu_nuts2 = {}
    d_eu_nuts2[var] = {}
    for nuts2_id, nuts2 in enumerate(gdf_eu_nuts2):
        if nuts2 in d_df:
            val = d_df[nuts2]
            d_eu_nuts2[var][nuts2_id] = val
        else:
            d_eu_nuts2[var][nuts2_id] = np.nan

    return pd.DataFrame(d_eu_nuts2)


def write_va(df, file_name):
    with open(cfg.RESULT_TXT_DIR_PATH + file_name, "w") as write_file:
        csv_file = csv.writer(write_file, delimiter="\t", lineterminator="\n")
        row_write = ["Country", "NUTS-2", "Val"]
        csv_file.writerow(row_write)
        d_df = df.to_dict()
        for t_cntr_nuts2 in d_df:
            cntr, nuts2 = t_cntr_nuts2
            val = d_df[t_cntr_nuts2]
            row_write = [cntr, nuts2, val]
            csv_file.writerow(row_write)


def write_var_nuts2(df, file_name):
    with open(cfg.RESULT_TXT_DIR_PATH + file_name, "w") as write_file:
        csv_file = csv.writer(write_file, delimiter="\t", lineterminator="\n")
        csv_file = csv.writer(write_file, delimiter="\t", lineterminator="\n")
        row_write = ["EXIOMOD execution date"] + list(cfg.t_em_base_datetime[0])
        csv_file.writerow(row_write)
        row_write = ["GLOBIOM execution date"] + list(cfg.t_gb_date[1])
        csv_file.writerow(row_write)

        row_write = ["Country", "NUTS-2", "Val"]
        csv_file.writerow(row_write)
        d_df = df.to_dict()
        for t_cntr_nuts2 in d_df:
            cntr, nuts2 = t_cntr_nuts2
            val = d_df[t_cntr_nuts2]
            row_write = [cntr, nuts2, val]
            csv_file.writerow(row_write)


def write_prod_bm_cntr(df, file_name):
    d_df = df.to_dict()
    with open(cfg.RESULT_TXT_DIR_PATH + file_name, "w") as write_file:
        csv_file = csv.writer(write_file, delimiter="\t", lineterminator="\n")
        row_write = ["EXIOMOD execution date"] + list(cfg.t_em_base_datetime[0])
        csv_file.writerow(row_write)
        row_write = ["GLOBIOM execution date"] + list(cfg.t_gb_date[1])
        csv_file.writerow(row_write)
        csv_file = csv.writer(write_file, delimiter="\t", lineterminator="\n")
        row_write = ["Country", "Val"]
        csv_file.writerow(row_write)
        for cntr in d_df:
            val = d_df[cntr]
            row_write = [cntr, val]
            csv_file.writerow(row_write)


def write_va_ifore_eu(df, file_name):
    d_df = df.to_dict()
    with open(cfg.RESULT_TXT_DIR_PATH + file_name, "w") as write_file:
        csv_file = csv.writer(write_file, delimiter="\t", lineterminator="\n")
        row_write = ["EXIOMOD execution date"] + list(cfg.t_em_base_datetime[0])
        csv_file.writerow(row_write)
        row_write = ["GLOBIOM execution date"] + list(cfg.t_gb_date[1])
        csv_file.writerow(row_write)

        row_write = ["Country", "Val"]
        csv_file.writerow(row_write)
        for cntr in d_df:
            val = d_df[cntr]
            row_write = [cntr, val]
            csv_file.writerow(row_write)


def write_var(df, file_name):
    ut.log(f'Write EXIOMOD output tot {file_name}.')
    d_df = df.to_dict()
    with open(cfg.RESULT_TXT_DIR_PATH + file_name, "w") as write_file:
        csv_file = csv.writer(write_file, delimiter="\t", lineterminator="\n")
        row_write = ["EXIOMOD execution date"] + list(cfg.t_em_base_datetime[0])
        csv_file.writerow(row_write)
        row_write = ["GLOBIOM execution date"] + list(cfg.t_gb_date[1])
        csv_file.writerow(row_write)
        row_write = ["Region", "Industry", "Value"]
        csv_file.writerow(row_write)
        for t_cntr_ind in d_df:
            cntr, ind = t_cntr_ind
            val = d_df[t_cntr_ind]
            row_write = [cntr, ind, val]
            csv_file.writerow(row_write)


def create_wb():
    return xw.Book()


def write_var_excel(df, sheet_name, wb, unstack):
    ut.log(f'Write output to Excel workbook, sheet {sheet_name}.')

    sht = wb.sheets.add(sheet_name, after=wb.sheets[-1])
    if unstack:
        sht.range("A1").value = df.unstack()
    else:
        sht.range("A1").value = df
    return wb


def save_wb(wb, file_path):
    for sheet in wb.sheets:
        if "Sheet" in sheet.name:
            # print('\t\tDeleting sheet with name {}'.format(sheet.name))
            sheet.delete()
    wb.save(file_path)


def close_wb():
    app = xw.apps.active
    app.quit()


def cm2inch(tup_cm):
    """ Convert cm to inch.
        Used for figure generation.

        Parameters
        ----------
        tup_cm: tuple with values in cm.

        Returns
        -------
        tup_inch: tuple with values in inch.

    """
    inch = 2.54
    tup_inch = tuple(i/inch for i in tup_cm)
    return tup_inch


def plot_gdf_cm(gdf_eu, df, scen):
    for col in df:
        if scen == 'delta':
            cmap = 'coolwarm'
            cmap_name = cmap
            vmin = int(np.floor(-df[col].max()))
            vmax = int(np.ceil(df[col].max()))
        else:
            cmap_name = "crest"
            cmap = sns.color_palette(cmap_name, as_cmap=True)

            vmin = int(np.floor(df[col].min()))
            vmax = int(np.ceil(df[col].max()))
        plt.figure()
        gdf_eu.plot(column=col,
                    missing_kwds={"color": "lightgrey"},
                    legend=True,
                    legend_kwds={'ticks': [vmin,
                                           # int((vmin+vmax)/2),
                                           vmax]},
                    cmap=cmap,
                    vmin=vmin,
                    vmax=vmax)
        plt.tight_layout()
        plt.savefig(f'{cfg.RESULT_PNG_DIR_PATH}{scen}_{col}')
        plt.close('all')


def var2gdf_cm(gdf_eu_cm, df):
    d_eu_cm_nuts2 = {}
    for ind in df:
        d_eu_cm_nuts2[ind] = {}
        for nuts2_id, nuts2 in enumerate(gdf_eu_cm['NUTS_ID']):
            if nuts2 in df.index:
                d_eu_cm_nuts2[ind][nuts2_id] = df.loc[nuts2, ind]
            else:
                d_eu_cm_nuts2[ind][nuts2_id] = np.nan

    df_eu_cm_nuts2 = pd.DataFrame(d_eu_cm_nuts2)

    for col in df_eu_cm_nuts2:
        gdf_eu_cm[col] = df_eu_cm_nuts2[col]

    return gdf_eu_cm
