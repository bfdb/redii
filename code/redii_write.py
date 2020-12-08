# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 08:20:37 2020

@author: bfdeboer
"""

from matplotlib.colors import TwoSlopeNorm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import cfg# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 08:20:37 2020

@author: bfdeboer
"""

from matplotlib.colors import TwoSlopeNorm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import cfg
import redii_read as rr


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
    for idx in d_world['iso_a3']:
        cntr_iso3 = d_world['iso_a3'][idx]
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
        norm = TwoSlopeNorm(vmin = vmin, vcenter=0, vmax = vmax)
        gdf_world.plot(column = var,
                       legend = True,
                       cmap = sns.color_palette("vlag", as_cmap=True),
                       norm = norm)
    else:
        gdf_world.plot(column = var,
                       legend = True,
                       cmap = sns.color_palette("crest", as_cmap=True))
    plt.savefig(cfg.RESULT_PNG_DIR_PATH+'{}_{}'.format(cfg.DATE, var))


def plot_redii_world(df_redii, var):
    gdf_world = rr.read_gdf_world()
    d_cntr_redii2exio_iso3 = rr.redii_iso3()
    df_iso3 = cntr_redii_iso3(df_redii, d_cntr_redii2exio_iso3)
    df_world = cntr_iso3_world(df_iso3, var, gdf_world)
    gdf_world = add_world_var(df_world,
                              var,
                              gdf_world)
    plot_world_var(gdf_world, var)


# Get countries from world gpd.
def write_gdf_world_cntr(gdf_world):
    d_world = gdf_world.to_dict()
    with open(cfg.INPUT_DIR_PATH+'cntr_gpd_world.txt', 'w') as write_file:
        csv_file = csv.writer(write_file, delimiter='\t', lineterminator='\n')
        row_write = ['Name', 'ISO A3', 'Continent']
        csv_file.writerow(row_write)
        for idx in d_world['continent']:
            cntr_name = d_world['name'][idx]
            cntr_iso_a3 = d_world['iso_a3'][idx]
            cntr_cont = d_world['continent'][idx]
            row_write = [cntr_name, cntr_iso_a3, cntr_cont]
            csv_file.writerow(row_write)

def globiom2gdf_nuts2(df, var, gdf_eu):
    gdf_eu_nuts2 = gdf_eu['NUTS_ID']
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
import redii_read as rr


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
    for idx in d_world['iso_a3']:
        cntr_iso3 = d_world['iso_a3'][idx]
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
    with open(cfg.INPUT_DIR_PATH+'cntr_gpd_world.txt', 'w') as write_file:
        csv_file = csv.writer(write_file, delimiter='\t', lineterminator='\n')
        row_write = ['Name', 'ISO A3', 'Continent']
        csv_file.writerow(row_write)
        for idx in d_world['continent']:
            cntr_name = d_world['name'][idx]
            cntr_iso_a3 = d_world['iso_a3'][idx]
            cntr_cont = d_world['continent'][idx]
            row_write = [cntr_name, cntr_iso_a3, cntr_cont]
            csv_file.writerow(row_write)

def globiom2gdf_nuts2(df, var, gdf_eu):
    gdf_eu_nuts2 = gdf_eu['NUTS_ID']
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