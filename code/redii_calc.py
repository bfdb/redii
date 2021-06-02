# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 08:21:26 2020

@author: bfdeboer
"""

import numpy as np
import pandas as pd

import cfg
import redii_read as rr
import utils as ut


def calc_d_cntr_nuts2_r(df):
    d_df = df.to_dict()
    d_cntr_nuts2 = {}
    d_s_cntr = {}
    for t_cntr_nuts2 in d_df:
        cntr, nuts2 = t_cntr_nuts2
        val = d_df[t_cntr_nuts2]
        if cntr not in d_cntr_nuts2:
            d_cntr_nuts2[cntr] = {}
            d_s_cntr[cntr] = 0
        d_cntr_nuts2[cntr][nuts2] = val
        d_s_cntr[cntr] += val

    d_cntr_nuts2_r = {}
    for cntr in d_cntr_nuts2:
        s_cntr = d_s_cntr[cntr]
        for nuts2 in d_cntr_nuts2[cntr]:
            val = d_cntr_nuts2[cntr][nuts2]
            val_r = val / s_cntr
            d_cntr_nuts2_r[(cntr, nuts2)] = val_r
    df_cntr_nuts2_r = pd.Series(d_cntr_nuts2_r)
    return df_cntr_nuts2_r


def calc_d_cntr_nuts2_va_ielcb(df_va, df_cntr_nuts2_r):
    d_df_va = df_va.to_dict()
    d_cntr_nuts2_r = df_cntr_nuts2_r.to_dict()
    d_cntr_nuts2_va = {}
    for t_cntr_nuts2 in d_cntr_nuts2_r:
        cntr, nuts2 = t_cntr_nuts2
        if cntr in cfg.d_cntr_globiom2exio:
            cntr_exio = cfg.d_cntr_globiom2exio[cntr]
            cntr_va = d_df_va[cntr_exio, "iELCB"]
            cntr_nuts2_r = d_cntr_nuts2_r[t_cntr_nuts2]
            cntr_nuts2_va = cntr_nuts2_r * cntr_va
            d_cntr_nuts2_va[t_cntr_nuts2] = cntr_nuts2_va

    df_cntr_nuts2_va = pd.Series(d_cntr_nuts2_va)
    return df_cntr_nuts2_va


def calc_d_cntr_nuts2_ielcb(df, df_cntr_nuts2_r):
    d_df = df.to_dict()
    d_cntr_nuts2_r = df_cntr_nuts2_r.to_dict()
    d_cntr_nuts2_val = {}
    for t_cntr_nuts2 in d_cntr_nuts2_r:
        cntr, nuts2 = t_cntr_nuts2
        if cntr in cfg.d_cntr_globiom2exio:
            cntr_exio = cfg.d_cntr_globiom2exio[cntr]
            cntr_val = d_df[cntr_exio, "iELCB"]
            cntr_nuts2_r = d_cntr_nuts2_r[t_cntr_nuts2]
            cntr_nuts2_val = cntr_nuts2_r * cntr_val
            d_cntr_nuts2_val[t_cntr_nuts2] = cntr_nuts2_val

    df_cntr_nuts2_val = pd.Series(d_cntr_nuts2_val)
    return df_cntr_nuts2_val


def va_ind_cntr_eu(df_va, ind):
    df_va_ind = df_va[:, ind]
    d_df_va_ind = df_va_ind.to_dict()
    d_df_va_cntr_exio2globiom = {}
    for cntr in d_df_va_ind:
        if cntr in cfg.d_cntr_exio2globiom and "EU28_" in cntr:
            cntr_globiom = cfg.d_cntr_exio2globiom[cntr]
            cntr_va = d_df_va_ind[cntr]
            d_df_va_cntr_exio2globiom[cntr_globiom] = cntr_va

    return pd.Series(d_df_va_cntr_exio2globiom)


def var_cntr2nuts(df_var):
    d_var_cntr2nuts = {}
    # disaggregate VA, emp with circumat x_nuts/x_cntr
    d_x_cm = rr.read_d_x_cm()
    # Aggregate sectors to EXIOMOD classification
    df_ind_cm2em = rr.read_ind_cm2em()

    for cntr in cfg.l_eu28:
        df_var_cntr = df_var[cntr]

        df_x_cm_cntr = d_x_cm[cntr]['x_cntr']
        df_x_cm_nuts2 = d_x_cm[cntr]['x_nuts2']

        df_x_em_cntr = df_x_cm_cntr.dot(df_ind_cm2em)
        df_x_em_nuts2 = df_x_cm_nuts2.unstack().dot(df_ind_cm2em)

        df_x_em_nuts2_rel = df_x_em_nuts2.divide(df_x_em_cntr)
        df_x_em_nuts2_rel.fillna(0, inplace=True)

        # Reorder index.
        df_x_em_nuts2_rel = df_x_em_nuts2_rel[df_var_cntr.index]

        df_var_cntr_diag = pd.DataFrame(np.diag(df_var_cntr),
                                        index=df_var_cntr.index,
                                        columns=df_var_cntr.index)

        df_var_nuts2 = (
            df_x_em_nuts2_rel.dot(df_var_cntr_diag))
        d_var_cntr2nuts[cntr] = df_var_nuts2

    df_cat = pd.DataFrame()
    for cntr in d_var_cntr2nuts:
        df = d_var_cntr2nuts[cntr]
        if df_cat.empty:
            df_cat = df
        else:
            df_cat = pd.concat([df_cat, df])

    return df_cat
