# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 08:21:26 2020

@author: bfdeboer
"""

import pandas as pd

import cfg

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
            val_r = val/s_cntr
            d_cntr_nuts2_r[(cntr,nuts2)] = val_r
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
            cntr_va = d_df_va[cntr_exio, 'iELCB']
            cntr_nuts2_r = d_cntr_nuts2_r[t_cntr_nuts2]
            cntr_nuts2_va = cntr_nuts2_r*cntr_va
            d_cntr_nuts2_va[t_cntr_nuts2] = cntr_nuts2_va

    df_cntr_nuts2_va = pd.Series(d_cntr_nuts2_va)
    return df_cntr_nuts2_va