# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:04:16 2020

@author: navarrenhn
"""
from memory_profiler import profile

import numpy as np
import pandas as pd
import pickle as pk
import matplotlib.pyplot as plt
from collections import defaultdict

import csv
import os
import pickle

import cfg
import exiobase as eb
import redii_read as rr
import utils as ut


def calc_x(ar_a, ar_y):
    print('calc_x')
    ar_l = np.linalg.inv(np.identity(len(ar_a)) - ar_a)
    return np.dot(ar_l, np.sum(ar_y, axis=1))


def calc_z_s(ar_a, ar_x):
    ar_z = np.dot(ar_a, np.array(np.diag(ar_x)))
    ar_z_s_in = np.sum(ar_z, axis=0)
    ar_z_s_out = np.sum(ar_z, axis=1)
    return ar_z_s_in, ar_z_s_out


def get_cm_reg_nuts2_start():
    print('get_cm_reg_nuts2_start')
    d_cm_reg = {}
    d_cm_reg_nuts2_start = {}
    with open(cfg.INPUT_DIR_PATH+'cm_reg.txt', encoding='utf-8') as read_file:
        csv_file = csv.reader(read_file, delimiter='\t')
        for row in csv_file:
            reg_name, reg_code, global_id, parent_id, local_id, level = row
            # country level
            if level == '2':
                d_cm_reg[reg_code] = {}
                d_cm_reg[reg_code]['reg_name'] = reg_name
                d_cm_reg[reg_code]['global_id'] = global_id
                d_cm_reg[reg_code]['parent_id'] = global_id
                d_cm_reg[reg_code]['local_id'] = local_id
                d_cm_reg[reg_code]['level'] = level
                d_cm_reg[reg_code]['NUTS2'] = {}
            if level == '3':
                reg_code_parent = reg_code[0:2]
                d_cm_reg[reg_code_parent]['NUTS2'][reg_code] = {}
                d_cm_reg[reg_code_parent]['NUTS2'][reg_code]['reg_name'] = reg_name
                d_cm_reg[reg_code_parent]['NUTS2'][reg_code]['global_id'] = global_id
                d_cm_reg[reg_code_parent]['NUTS2'][reg_code]['parent_id'] = global_id
                d_cm_reg[reg_code_parent]['NUTS2'][reg_code]['local_id'] = local_id
                d_cm_reg[reg_code_parent]['NUTS2'][reg_code]['level'] = level
                if reg_code_parent not in d_cm_reg_nuts2_start:
                    d_cm_reg_nuts2_start[reg_code_parent] = int(global_id)
    return d_cm_reg_nuts2_start


def load_data(source, reg):
    print('load_data')

    if reg == 'world':
        l_cntr = cfg.l_wrld
    elif reg == 'eu28':
        l_cntr = cfg.l_eu28_eb
    elif reg == 'eu28exuk':
        l_cntr = cfg.l_eu28exuk_eb
    elif reg == 'IE':
        l_cntr = ['IE']

    df_a_mr, df_y_mr, df_v_mr = (
        rr.load_data(source=source,
                     l_cntr=l_cntr)
        )

    df_x_file_name = 'df_x.pkl'
    if df_x_file_name in os.listdir(cfg.INPUT_DIR_PATH):
        df_x_mr = pickle.load(
            open(cfg.INPUT_DIR_PATH+df_x_file_name,
                 'rb'))
    else:
        ar_x_mr = calc_x(df_a_mr, df_y_mr)

        df_x_mr = pd.Series(ar_x_mr,
                            index=df_a_mr.columns)
        pickle.dump(df_x_mr,
                    open(cfg.INPUT_DIR_PATH+df_x_file_name,
                         'wb'))

    return df_a_mr, df_y_mr, df_v_mr, df_x_mr


def va_cntr2nuts2(cntr_em, df_x_cntr, df_x_nuts2):
    print('va_cntr2nuts2')

    # Read value added in prices from baseline and EUCO3232.5.
    df_va_p_2030_base = rr.read_va_yr(
        cfg.DATA_SHARE_DIR_PATH +
        cfg.EXIOMOD_DIR_PATH +
        cfg.file_name_base_eu28,
        cfg.var_name_va_p_new,
        cfg.yr_end,
    )

    # Aggregate sectors to EXIOMOD classification
    df_eb_ind_code2em_ind_agg = (
        pd.read_csv(cfg.INPUT_DIR_PATH +
                    cfg.EB_IND_CODE2EM_IND_AGG_FILE_NAME,
                    sep='\t',
                    index_col=[0, 1],
                    header=[0]))
    df_eb_ind_code2em_ind_agg = df_eb_ind_code2em_ind_agg.droplevel(axis=0,
                                                                    level=0)

    df_x_cntr_em = df_x_cntr.dot(df_eb_ind_code2em_ind_agg)
    df_x_nuts2_em = df_x_nuts2.unstack().dot(df_eb_ind_code2em_ind_agg)

    df_x_nuts2_em_rel = df_x_nuts2_em.divide(df_x_cntr_em)
    df_x_nuts2_em_rel.fillna(0, inplace=True)

    df_va_p_2030_base_cntr = df_va_p_2030_base[cntr_em]

    df_x_nuts2_em_rel = df_x_nuts2_em_rel[df_va_p_2030_base_cntr.index]
    df_va_p_2030_base_cntr_diag = pd.DataFrame(np.diag(df_va_p_2030_base_cntr),
                                               index=df_va_p_2030_base_cntr.index,
                                               columns=df_va_p_2030_base_cntr.index)

    df_va_p_2030_base_nuts2 = (
        df_x_nuts2_em_rel.dot(df_va_p_2030_base_cntr_diag))

    return df_va_p_2030_base_cntr, df_va_p_2030_base_nuts2


ut.makedirs()


@profile(stream=open(cfg.LOG_DIR_PATH+'memory_profiler.txt', 'w+'))
def x_cntr2nuts2(source,
                 s_country_cm,
                 s_country_eb,
                 # s_country_es,
                 country_start,
                 df_a_mr,
                 df_y_mr,
                 df_v_mr,
                 df_x_mr):
    print('x_cntr2nuts2')
    country = [s_country_eb]
    country_start = [country_start]

    n_cntr = 49
    n_prod = 200
    n_ind = 163
    n_y = 7

    if source == 'eb_ixi':
        n_sect = n_ind
    elif source == 'eb_pxp':
        n_sect = n_prod
    elif source == 'cm':
        n_sect = n_prod

    # Pick countries you want to disaggregate
    # country_start = [183]
    # country = ["IE"]

    data_folder = cfg.INPUT_DIR_PATH+'cm/'

    A_mr = df_a_mr.values
    Y_mr = df_y_mr.values
    B_mr = df_v_mr.values

    A_mr_original = A_mr
    Y_mr_original = Y_mr
    B_mr_original = B_mr

    X_total_original = df_x_mr.values
    # X_total_original = calc_x(A_mr_original, Y_mr_original)

    # Y_mr_org = Y_mr
    # A_mr_org = A_mr
    # B_mr_org = B_mr

    # number of countries in the original mrio
    n_c = Y_mr.shape[1] / n_y  # number of countries in the original mrio
    n_c = int(n_c)
    n_c_org = n_c
    n_s = A_mr.shape[0] / n_c  # number of sectors (or products) in the original mrio
    n_s = int(n_s)
    n_v = 1  # number of diferent parts in the va
    n_v = int(n_v)
    n_r = 2  # this is always two, we will divide region into two parts

    n_b = B_mr.shape[0]  # number of environmental indicators
    n_b = int(n_b)

    # df_x_mr = pd.Series(X_total_original,
    #                     index=df_a_mr.columns)

    # list including the table for country and its subnational details
    # regions = pd.read_excel(data_folder+"circumat_regions_v3.xls")
    regions = pd.read_excel(data_folder+"circumat_regions.xls")

    # list of final demand categories for EXIOBASE regions.
    l_y_col = list(df_y_mr.columns)
    l_idx = list(df_y_mr.index)
    l_idx_nuts2 = l_idx.copy()

    # conversion of the sectors in eurostat to exiobase starts..
    # for sbs
    conversion_matrix = pd.read_excel(
        data_folder + "SBS_MATCH.xls",
        sheet_name="matrix",
        header=None,
    )
    conversion_matrix = np.array(conversion_matrix)
    tmp = conversion_matrix.shape
    nrows = tmp[0]
    ncols = tmp[1]

    rowsum_conversion_matrix = np.sum(
        conversion_matrix, axis=1
    )  # this should be NONZERO! BUT unless it is a parent sector!

    convert_matrix = conversion_matrix * np.reshape(
        np.repeat(1 / (rowsum_conversion_matrix + +(10 ** (-31))), ncols),
        [nrows, ncols],
    )

    for m, n in zip(country_start, country):

        l_nuts2 = []

        # get labels of final demand categories.
        l_y_cat = list(df_y_mr[n].columns)

        # get labels of sectors (either product or index, depending on pxp or ixi)
        l_sect = list(df_y_mr.loc[n].index)

        # # this list will be used to recover the individual X_rr arrays of each region
        # # when calculating everything at once.
        # X_rr_list = (
        #     []
        # )
        id_prev = 0
        Region_data = defaultdict(list)
        Reg_exp_total = []
        Reg_emp_total = []
        Excess_demand_list = []
        Region_names = []
        """
        Pick any range of regions you'd like
        Check in the circumat_regions.xlsx for the numbers.
        266-311 (SK) is nice because it runs quickly while having multiple regions.
        207-208 (LT) only has two regions, so it's easier to see the breakdown.
        """

        """
        INPUT: Adjust the start range of the for loop to equal the first subregion.
        Update the if z> statement to match the start range.
        Update the if id_rof != '' to be the country initials
        """

        for z in range(m, len(regions)+1):
            print(m, n, z)
            """
            This first portion focuses on importing the disaggregation data and building
            the national vs regional ratios,
            and finding the columns and rof of interest in the matrices.
            """

            if z > m:
                Y_mr = Y_mr_disagg
                Y_mr[
                    np.array(range(0, n_c_org * n_s))[:, None],
                    np.array(range(0, n_c_org * n_y)),
                ] = Y_mr_original

                A_mr = A_mr_disagg
                A_mr[
                    np.array(range(0, n_c_org * n_s))[:, None],
                    np.array(range(0, n_c_org * n_s)),
                ] = A_mr_original

                B_mr = B_mr_disagg
                B_mr[
                    np.array(range(0, n_b))[:, None], np.array(range(0, n_c_org * n_s))
                ] = B_mr_original

                n_c = Y_mr.shape[1] / n_y  # number of countries in the original mrio
                n_c = int(n_c)

                n_s = (
                    A_mr.shape[0] / n_c
                )  # number of sectors (or products) in the original mrio
                n_s = int(n_s)

            Nuts2 = z
            # find the region of interest =rof in the exiobase,
            # i.e. the parent country of the region.
            # this is according to the exiobase numbering
            # here the exiobase starts from 1, parent id
            rof = int(regions.iloc[int(np.where(regions.iloc[:, 2] == Nuts2)[0]), 3])
            # find the name of the country
            name_rof = regions.iloc[int(np.where(regions.iloc[:, 2] == rof)[0]), 0]
            # find the  id  of the nuts2; the code of it
            id_Nuts2 = regions.iloc[int(np.where(regions.iloc[:, 2] == Nuts2)[0]), 1]
            # find the label of the country; the code of it.
            # that is the frst two letter of above
            id_rof = id_Nuts2[0:2]

            # Stop the code from running on to a new nation.

            # if id_rof != n:
            if id_rof != s_country_cm:
                break

            # print(f'Nuts2 {Nuts2}, rof {rof}, name_rof {name_rof}, ' +
            #       f'id_Nuts2 {id_Nuts2}, id_rof {id_rof}')
            l_nuts2.append(id_Nuts2)

            # generate labels of final demand categories for nuts2 region
            l_y_nuts2_cat = []
            for cat in l_y_cat:
                t_nuts2_cat = (id_Nuts2, cat)
                l_y_nuts2_cat.append(t_nuts2_cat)

            # concatenate with list of final demand categories for EXIOBASE regions.
            l_y_col += l_y_nuts2_cat

            # generate labels of sectors for nuts2 region
            l_y_nuts2_sect = []
            for sect in l_sect:
                t_nuts2_sect = (id_Nuts2, sect)
                l_y_nuts2_sect.append(t_nuts2_sect)

            # concatenate with indices for EXIOBASE regions-sector pairs.
            l_idx_nuts2 += l_y_nuts2_sect

            id_prev = id_rof
            Region_names.append(id_Nuts2)
            print(id_rof, id_Nuts2)

            # according to the country code, read the income data
            reg_exp_shares_all = pd.read_csv(
                data_folder
                + "Income/2011_income_"
                + "%s" % id_rof
                + "_"
                + "%s" % name_rof
                + "_B5N_MIO_EUR.csv",
                header=None,
                sep="\t",
            )

            # # accomodate for eurostat bug
            # # according to the country code, read the income data
            # reg_exp_shares_all = pd.read_csv(
            #     data_folder
            #     + "Income/2011_income_"
            #     + "%s" % s_country_es
            #     + "_"
            #     + "%s" % name_rof
            #     + "_B5N_MIO_EUR.csv",
            #     header=None,
            #     sep="\t",
            # )

            """
            reg_exp_shares_all[0][0] = 'SL03'
            reg_exp_shares_all[0][1] = 'SL04'
            """

            # turn reg_exp_shares_all of the country into another matrix the rest of the
            # country  as region 1 and the selected nuts 2 as region 2
            reg_exp_shares = np.zeros((n_y, n_r))
            # first find the nuts 2
            internal_id_Nuts2 = (
                (np.where(reg_exp_shares_all.iloc[:, 0] == id_Nuts2)[0])[0])
            # print(f"internal_id_Nuts2 {internal_id_Nuts2} id_Nuts2 {id_Nuts2}")
            # write the nuts 2 income data into the second column, and scale it with the
            # sum of all income in the country
            reg_exp_shares[:, 1] = (
                reg_exp_shares_all.iloc[internal_id_Nuts2, 1] / np.sum(
                    reg_exp_shares_all.iloc[:, 1], axis=0))
            # then fll in the rest of the nation details i.e. all sum minus the nuts2 in
            # the column 1
            reg_exp_shares[:, 0] = (
                np.sum(reg_exp_shares_all.iloc[:, 1], axis=0)
                - reg_exp_shares_all.iloc[internal_id_Nuts2, 1]
            ) / np.sum(reg_exp_shares_all.iloc[:, 1], axis=0)

            # according to the country code, read the sbs employnment data
            sbs_emp_numbers_all = pd.read_csv(
                data_folder
                + "Employment_By_Sector/2011_SBS_"
                + "%s" % id_rof
                + "_"
                + "%s" % name_rof
                + "_V16110.csv",
                sep="\t",
            )

            # problems with SL being written inconsistently in the source files.
            """
            if id_Nuts2 == 'SL03':
                id_Nuts2 = 'Sl03'

            else:
                id_Nuts2 = 'Sl04'
            """
            # turn it into another matrix the rest of the country  as region 1 and
            # the selected nuts 2 as region 2

            sbs_emp_numbers = np.zeros((sbs_emp_numbers_all.shape[1] - 1, n_r))
            # first find the nuts 2
            internal_id_Nuts2 = (
                (np.where(sbs_emp_numbers_all.iloc[:, 0] == id_Nuts2)[0])[0])
            # first fill the nuts 2 region details
            sbs_emp_numbers[:, 1] = sbs_emp_numbers_all.iloc[
                internal_id_Nuts2, 1:sbs_emp_numbers_all.shape[1]
            ]
            # then fll in the rest of the nation details i.e. all sum minus the nuts2
            sbs_emp_numbers[:, 0] = (
                np.sum(
                    sbs_emp_numbers_all.iloc[:, 1:sbs_emp_numbers_all.shape[1]], axis=0
                )
                - sbs_emp_numbers[:, 1]
            )

            """
            if id_Nuts2 == 'Sl03':
                id_Nuts2 = 'SL03'

            else:
                id_Nuts2 = 'SL04'
            """

            # convert them to numpy arrays
            sbs_emp_numbers = np.array(sbs_emp_numbers)
            reg_exp_shares = np.array(reg_exp_shares)

            sbs_emp_numbers_all_in_exiobase = np.dot(
                np.transpose(sbs_emp_numbers), convert_matrix
            )

            # if ixi, multiply with concordance matrix from pxp to ixi.
            if source == 'eb_ixi':
                df_eb_pxp2ixi = pd.read_csv(cfg.INPUT_DIR_PATH+cfg.file_name_eb_pxp2ixi,
                                            sep='\t',
                                            header=[0],
                                            index_col=[0])
                sbs_emp_numbers_all_in_eb_ixi = np.dot(sbs_emp_numbers_all_in_exiobase,
                                                       df_eb_pxp2ixi)
                sbs_emp_numbers_all_in_exiobase = sbs_emp_numbers_all_in_eb_ixi

            sbs_emp_numbers_all_in_exiobase = (
                np.transpose(sbs_emp_numbers_all_in_exiobase))

            reg_emp_numbers = sbs_emp_numbers_all_in_exiobase

            # convert them to numpy arrays
            reg_emp_numbers = np.array(reg_emp_numbers)
            reg_exp_shares = np.array(reg_exp_shares)

            # calculate the total  employment for each sector in whole country
            tot_emp = np.dot(reg_emp_numbers, np.ones((n_r, 1)))

            # calculate the employment shares in each region for each sector
            # what is the ratio between (sector S workers in region R)
            # and (total employment of sector S)
            # it shows the share of that sector per region
            emp_shares = (
                np.multiply(reg_emp_numbers, np.reciprocal(tot_emp + 10 ** (-31))))

            # calculate the location quotient in each region for each sector
            # what is the ratio between (employment share of sector S in region R)
            # and (employment share of S ?n all country)
            # share of people workin in that region as opposed to all country
            reg_emp_share = np.sum(reg_emp_numbers, axis=0) / (
                np.sum(np.sum(reg_emp_numbers, axis=0)) + 10 ** (-31)
            )
            # location_quatients=emp_shares./reg_emp_share
            location_quatients = emp_shares / (reg_emp_share + 10 ** (-31))

            # find the rows and column indices of the country in the exiobase in py
            # (ie index starts from 0)
            # changed calculation to accomodate for inclusion of UK
            l_a_cntr_col = df_a_mr.columns.get_loc(n)
            l_y_cntr_col = df_y_mr.columns.get_loc(n)
            l_a_cntr_idx = df_a_mr.index.get_loc(n)
            if type(l_a_cntr_col) == np.ndarray:
                a_cntr_col_start = l_a_cntr_col.nonzero()[0][0]
                a_cntr_col_stop = l_a_cntr_col.nonzero()[0][-1]+1

                y_cntr_col_start = l_y_cntr_col.nonzero()[0][0]
                y_cntr_col_stop = l_y_cntr_col.nonzero()[0][-1]+1

                a_cntr_idx_start = l_a_cntr_idx.nonzero()[0][0]
                a_cntr_idx_stop = l_a_cntr_idx.nonzero()[0][-1]+1

            elif type(l_a_cntr_col) == slice:
                a_cntr_col_start = df_a_mr.columns.get_loc(n).start
                a_cntr_col_stop = df_a_mr.columns.get_loc(n).stop

                y_cntr_col_start = df_y_mr.columns.get_loc(n).start
                y_cntr_col_stop = df_y_mr.columns.get_loc(n).stop

                a_cntr_idx_start = df_a_mr.index.get_loc(n).start
                a_cntr_idx_stop = df_a_mr.index.get_loc(n).stop
            Zcolumns_of_rof = np.array(range(a_cntr_col_start,
                                             a_cntr_col_stop))
            Ycolumns_of_rof = np.array(range(y_cntr_col_start,
                                             y_cntr_col_stop))
            Zrows_of_rof = np.array(range(a_cntr_idx_start,
                                          a_cntr_idx_stop))

            """
            The second partion of this code focuses on building the new regional matrix
            values according to the disaggregation calculations done before.
            Early in the code A_mr and Y_mr are updated to A_mr_disagg and Y_mr to
            include the previously disaggregated regions.
            """
            # calculate the leontief
            # X_total = calc_x(A_mr, Y_mr)

            # X_total[range(0, n_c_org * n_s)] = X_total_original

            # X_rof = X_total[Zrows_of_rof]
            X_rof = X_total_original[Zrows_of_rof]

            # it gives an ns by nr matrix
            R_x = (
                np.transpose(np.tile(X_rof, (2, 1))) * emp_shares
            )

            # # thus reshape it to a column matrix.
            # # reshape function takes the first column first and etc.
            # X_rr = np.reshape(
            #     R_x, n_r * n_s, order="F"
            # )

            A_rof = A_mr[Zrows_of_rof[:, None], Zcolumns_of_rof]

            # for each sector in each new region: miller and blair- page 367
            basic_demand = np.minimum(location_quatients, 1)
            excess_demand = np.subtract(1, basic_demand)

            # find the technical coeff
            # what can the sector output to the sectors in the region
            A_r1r1 = A_rof * np.reshape(np.array(basic_demand[:, 0]), (n_s, 1))
            A_r2r2 = A_rof * np.reshape(np.array(basic_demand[:, 1]), (n_s, 1))

            # what is the trade between the sectors in rest of the nation and
            # the nuts 2 region
            A_r1r2 = A_rof * np.reshape(np.array(excess_demand[:, 1]), (n_s, 1))
            A_r2r1 = A_rof * np.reshape(np.array(excess_demand[:, 0]), (n_s, 1))

            A_rr = np.concatenate(
                (
                    np.concatenate((A_r1r1, A_r2r1), axis=1),
                    np.concatenate((A_r1r2, A_r2r2), axis=1),
                ),
                axis=0,
            )

            # Z_rr = np.dot(A_rr, np.diag(X_rr))

            Y_r1 = Y_mr[Zrows_of_rof[:, None], Ycolumns_of_rof] * np.transpose(
                np.reshape(np.array(reg_exp_shares[:, 0]), (n_y, 1))
            )
            Y_r2 = Y_mr[Zrows_of_rof[:, None], Ycolumns_of_rof] * np.transpose(
                np.reshape(np.array(reg_exp_shares[:, 1]), (n_y, 1))
            )

            Y_r1r1 = Y_r1 * np.reshape(np.array(basic_demand[:, 0]), (n_s, 1))
            Y_r2r2 = Y_r2 * np.reshape(np.array(basic_demand[:, 1]), (n_s, 1))
            Y_r1r2 = Y_r2 * np.reshape(np.array(excess_demand[:, 1]), (n_s, 1))
            Y_r2r1 = Y_r1 * np.reshape(np.array(excess_demand[:, 0]), (n_s, 1))

            Y_rr1 = np.concatenate((Y_r1r1, Y_r1r2), axis=1)
            Y_rr2 = np.concatenate((Y_r2r1, Y_r2r2), axis=1)
            Y_rr = np.concatenate(
                (
                    np.concatenate((Y_r1r1, Y_r1r2), axis=1),
                    np.concatenate((Y_r2r1, Y_r2r2), axis=1),
                ),
                axis=0,
            )

            # lets go to the updated mr database
            # the new region 2 is added at the end of the natabase whereas its parent
            # country stays the same
            new_Zcolumns_of_region2 = np.array(range((n_c) * n_s, (n_c + 1) * n_s))
            new_Ycolumns_of_region2 = np.array(range((n_c) * n_y, (n_c + 1) * n_y))
            new_Zrows_of_region2 = np.array(range((n_c) * n_s, (n_c + 1) * n_s))

            # allocate a free database with number of countries increased by 1
            A_mr_disagg = np.zeros(((n_c + 1) * n_s, (n_c + 1) * n_s))
            A_mr[
                np.array(range(0, n_c_org * n_s))[:, None],
                np.array(range(0, n_c_org * n_s)),
            ] = A_mr_original
            A_mr_disagg[
                np.array(range(0, (n_c) * n_s))[:, None],
                np.array(range(0, (n_c) * n_s))
            ] = A_mr
            # duplicate the rows and the columns of country of interest

            # rows according to the output shares
            A_mr_disagg[Zrows_of_rof[:, None], range(0, (n_c) * n_s)] = A_mr[
                Zrows_of_rof, :
            ] * np.reshape(np.array((R_x[:, 0]) / (X_rof + 10 ** (-31))), (n_s, 1))
            A_mr_disagg[new_Zrows_of_region2[:, None], range(0, (n_c) * n_s)] = A_mr[
                Zrows_of_rof, :
            ] * np.reshape(np.array((R_x[:, 1]) / (X_rof + 10 ** (-31))), (n_s, 1))
            # columns stays the same product recipe

            A_mr_disagg[np.array(range(0, (n_c) * n_s))[:, None], Zcolumns_of_rof] = (
                A_mr[:, Zcolumns_of_rof])
            A_mr_disagg[
                np.array(range(0, (n_c) * n_s))[:, None], new_Zcolumns_of_region2
            ] = A_mr[:, Zcolumns_of_rof]

            # instead of the country of interest roc now we have the rest of that
            # country
            # region 1 puts into the previous place of rof
            A_r_check = A_r2r2 * location_quatients[:, 1]
            A_mr_disagg[Zrows_of_rof[:, None], Zcolumns_of_rof] = A_r1r1
            A_mr_disagg[new_Zrows_of_region2[:, None], new_Zcolumns_of_region2] = (
                A_r1r1 + A_r1r2
            )
            A_mr_disagg[Zrows_of_rof[:, None], new_Zcolumns_of_region2] = A_r1r2
            A_mr_disagg[new_Zcolumns_of_region2[:, None], Zcolumns_of_rof] = A_r2r1

            # duplication of y is similar to z but regional expend shares will come in
            Y_mr_disagg = np.zeros(((n_c + 1) * n_s, (n_c + 1) * n_y))
            Y_mr[
                np.array(range(0, n_c_org * n_s))[:, None],
                np.array(range(0, n_c_org * n_y)),
            ] = Y_mr_original
            Y_mr_disagg[
                np.array(range(0, (n_c) * n_s))[:, None],
                np.array(range(0, (n_y * (n_c))))
            ] = Y_mr

            Y_mr_disagg[np.array(range(0, (n_c) * n_s))[:, None], Ycolumns_of_rof] = (
                Y_mr[:, Ycolumns_of_rof] * np.array(reg_exp_shares[:, 0]))
            Y_mr_disagg[
                np.array(range(0, (n_c) * n_s))[:, None], new_Ycolumns_of_region2
            ] = Y_mr[:, Ycolumns_of_rof] * np.array(reg_exp_shares[:, 1])

            # rows according to the output shares
            Y_mr_disagg[Zrows_of_rof[:, None], np.array(range(0, (n_c) * n_y))] = Y_mr[
                Zrows_of_rof, :
            ] * np.reshape(np.array((R_x[:, 0]) / (X_rof + 10 ** (-31))), (n_s, 1))
            Y_mr_disagg[
                new_Zrows_of_region2[:, None], np.array(range(0, (n_c) * n_y))
            ] = Y_mr[Zrows_of_rof, :] * np.reshape(
                np.array((R_x[:, 1]) / (X_rof + 10 ** (-31))), (n_s, 1)
            )

            # plug in the regions
            Y_mr_disagg[Zrows_of_rof[:, None], Ycolumns_of_rof] = Y_r1r1
            Y_mr_disagg[new_Zrows_of_region2[:, None], new_Ycolumns_of_region2] = Y_r2r2
            Y_mr_disagg[Zrows_of_rof[:, None], new_Ycolumns_of_region2] = Y_r1r2
            Y_mr_disagg[new_Zrows_of_region2[:, None], Ycolumns_of_rof] = Y_r2r1

            # X_rr_list.append(X_rr)

            Region_data[id_Nuts2].append(reg_exp_shares[0][1])
            Region_data[id_Nuts2].append(Y_r1r2)
            Region_data[id_Nuts2].append(Y_r2r1)
            Region_data[id_Nuts2].append(Y_r1r1)
            Region_data[id_Nuts2].append(Y_r2r2)
            Region_data[id_Nuts2].append(new_Ycolumns_of_region2[0])
            Region_data[id_Nuts2].append(reg_emp_share[1])
            Region_data[id_Nuts2].append(A_r1r2)
            Region_data[id_Nuts2].append(A_r2r1)
            Region_data[id_Nuts2].append(A_r1r1)
            Region_data[id_Nuts2].append(A_r2r2)
            Region_data[id_Nuts2].append(A_mr_original[Zrows_of_rof[:, None],
                                                       Zcolumns_of_rof])

            reg_exp_shares_all = reg_exp_shares_all.rename(
                columns={0: "regions", 1: "value"}
            )
            reg_exp_shares_all = reg_exp_shares_all.set_index("regions")

            Region_data[id_Nuts2].append(reg_exp_shares_all["value"][id_Nuts2])

            Reg_exp_total.append(reg_exp_shares[0][1])
            Reg_emp_total.append(reg_emp_share[1])
            Excess_demand_list.append(excess_demand)

            B_mr_disagg = np.zeros((n_b, (n_c + 1) * n_s))
            B_mr_disagg[:, np.array(range(0, (n_c) * n_s))] = B_mr
            Zprev_row = Zrows_of_rof - n_sect
            B_mr_disagg[:, new_Zcolumns_of_region2] = B_mr[:, Zrows_of_rof]

        """
        This was the tricky part. Essentially you have to build the excess demands list
        of each region for each sector before assigning any values.
        By doing this you can see which regions have excess demand and which don't,
        based on that you can see which will export and which won't.
        This adjusts the ratio of the original total.
        This ratio is built based on the income % of each region
        (this could also be adjusted for jobs and we can compare the results)
        """

        for j in range(0, len(Excess_demand_list)):

            for i in range(0, len(excess_demand)):
                factor = 0

                if Excess_demand_list[j][i][0] == 0:
                    factor = Reg_exp_total[j]

                    for z in range(0, len(Excess_demand_list)):
                        if z == j:
                            continue

                        for k in range(0, len(excess_demand)):
                            if k == i:
                                if Excess_demand_list[z][k][0] == 0:
                                    factor += Reg_exp_total[z]

                    Excess_demand_list[j][i][1] = 1 / factor

        reg_count = 0
        for i in range(n_c_org * n_s, n_s * n_c, n_sect):
            # print(reg_count, i)
            # Add in the row data according to ratio of regions
            # that are expected to export based on demand.
            Y_mr_disagg[
                np.array(range(i, i + n_sect))[:, None],
                np.array(range(0, n_c_org * n_y))
            ] = Y_mr_original[
                Zrows_of_rof[:, None], np.array(range(0, n_c_org * n_y))
            ] * np.reshape(
                np.array(
                    Excess_demand_list[reg_count][:, 1] * Reg_exp_total[reg_count]),
                (n_s, 1),
            )

            reg_count += 1

        Y_mr_disagg_final = Y_mr_disagg
        Y_mr_disagg_final[
            np.array(range(0, n_c_org * n_s))[:, None],
            np.array(range(0, n_c_org * n_y))
        ] = Y_mr_original

        reg_count = 0
        for i in range(n_c_org * n_s, n_s * n_c, n_sect):
            A_mr_disagg[
                np.array(range(i, i + n_sect))[:, None],
                np.array(range(0, n_c_org * n_s))
            ] = A_mr_original[
                Zrows_of_rof[:, None], np.array(range(0, n_c_org * n_s))
            ] * np.reshape(
                np.array(
                    Excess_demand_list[reg_count][:, 1] * Reg_exp_total[reg_count]),
                (n_s, 1),
            )
            reg_count += 1
        A_mr_disagg_final = A_mr_disagg
        A_mr_disagg_final[
            np.array(range(0, n_c_org * n_s))[:, None],
            np.array(range(0, n_c_org * n_s))
        ] = A_mr_original
        # This builds out the interregional data according to
        # Yr1r2 and regional income relationships.
        count = n_c_org * n_s
        factor_list = []
        for i in Region_data:
            reg_count = 0
            for j in range(n_c_org * n_y, n_y * n_c, 7):

                num = Region_data[i][0]
                temp = Region_data[i][1]
                factor = (Reg_exp_total[reg_count]) / (1 - num)

                if j != Region_data[i][5]:
                    Y_mr_disagg_final[
                        np.array(range(count, count + n_sect))[:, None],
                        np.array(range(j, j + 7)),
                    ] = (temp * factor)
                reg_count += 1

            reg_count = 0
            for b in range(n_c_org * n_s, n_s * n_c, n_sect):
                num = Region_data[i][0]
                temp = Region_data[i][11]  # + Region_data[i][9]
                factor = (Reg_exp_total[reg_count]) / (1 - num)

                A_mr_disagg_final[
                    np.array(range(count, count + n_sect))[:, None],
                    np.array(range(b, b + n_sect)),
                ] = (temp * num)
                reg_count += 1

            count += n_sect

        # Delete original nation after all regions are built out
        # to avoid double counting.
        Y_mr_disagg_final[Zrows_of_rof, :] = 0
        Y_mr_disagg_final[:, Ycolumns_of_rof] = 0

        A_mr_disagg_final[Zrows_of_rof, :] = 0
        A_mr_disagg_final[:, Zcolumns_of_rof] = 0

        """ Check sum of regional Y values vs. orginal Y """
        Y_disagg_total = np.sum(np.sum(Y_mr_disagg_final, axis=0))
        Y_org_total = np.sum(np.sum(Y_mr_original, axis=0))
        # print("Y_disagg total: ", Y_disagg_total)
        # print("Y_origin total: ", Y_org_total)

        # Check the individual sector ratios of the disagg and orignial Y matrix
        Y_check_disagg = np.sum(Y_mr_disagg_final, axis=1)
        Y_check_org = np.sum(Y_mr_original, axis=1)

        Y_checks = pd.DataFrame()
        for i in range(n_c_org * n_s, (n_c * n_s), n_sect):
            Y_checks[i] = np.array(Y_check_disagg[i:i + n_sect])

        Y_check = Y_checks.sum(axis=1)

        """ Calculate the final final output product """
        desired_X_mr_final = calc_x(A_mr_disagg_final, Y_mr_disagg_final)

        """
        #Calculate the emission vector
        emissions_org = B_mr_original * original_X_mr

        emissions_old = emissions_org[:,np.array(range(3800,4000))]
        emissions_old_sum = np.sum(emissions_old, axis = 1)
        print(emissions_old_sum[4])

        CO2_dict['MT'] = emissions_old_sum[4]


        emissions_test = B_mr_disagg * final_output_product_disagg
        emissions_test = emissions_test[:,np.array(range(9800,10200))]
        emissions_test_sum = np.sum(emissions_test, axis = 1 )
        #print(emissions_old_sum[4])

        """

        user_selected_products = np.intc(np.array(range(0, n_sect)))
        user_selected_country = n_c + 1

        # calculate the exiobase internal id s (starting from 0) of the products
        user_selected_products_ids = np.intc(
            np.zeros((n_c, (user_selected_products).shape[0]))
        )

        """ Plotting """
        """
        green_diamond = dict(markerfacecolor='g', marker='D')
        plt.figure(figsize=((18,9)))
        fig, ax = plt.subplots(figsize = (8,4))
        #ax.boxplot(CO2_dict.values(), flierprops=green_diamond)
        #ax.set_xticklabels(CO2_dict.keys())

        ax.set_ylabel('kg CO2 eq')
        ax.set_xlabel('Country ID')
        ax.set_title('European NUTS2 Total GHG Emissions')

        #plt.savefig('Disagg_example.png', dpi = 300, bbox_inches='tight')
        plt.show()
        """
        B_mr_disagg_final = B_mr_disagg

        # add labels to data
        mi_y_col = pd.MultiIndex.from_tuples(l_y_col)
        mi_idx_nuts2 = pd.MultiIndex.from_tuples(l_idx_nuts2)
        mi_idx = pd.MultiIndex.from_tuples(l_idx)
        mi_v = df_v_mr.index

        df_a_mr_disagg_final = pd.DataFrame(A_mr_disagg_final,
                                            index=mi_idx_nuts2,
                                            columns=mi_idx_nuts2)
        df_y_mr_disagg_final = pd.DataFrame(Y_mr_disagg_final,
                                            index=mi_idx_nuts2,
                                            columns=mi_y_col)
        df_cv_mr_disagg_final = pd.DataFrame(B_mr_disagg_final,
                                             index=mi_v,
                                             columns=mi_idx_nuts2)
        df_x_mr_disagg_final = pd.Series(desired_X_mr_final,
                                         index=mi_idx_nuts2)

        # test if total output of IE is equal to IExx NUTS2 regions
        # df_x_ie = df_x_mr['IE']
        # l_ie_nuts2 = ['IE04', 'IE05', 'IE06']
        # df_x_ie_nuts2 = df_x_mr_disagg_final[l_ie_nuts2]

        df_x_cntr = df_x_mr[s_country_eb]
        df_x_nuts2 = df_x_mr_disagg_final[l_nuts2]

        # %%
        # """ Save output disagg data """
        # with open(data_folder+id_prev + "_A_matrix_S.npy", "wb") as handle:
        #     np.save(handle, A_mr_disagg_final, handle)

        # with open(data_folder+id_prev + "_Y_matrix_S.npy", "wb") as handle:
        #     np.save(handle, Y_mr_disagg_final)

        # %%
        # if source == 'eb_ixi':
        #     # Read value added in prices from baseline and EUCO3232.5.
        #     df_va_p_2030_base = rr.read_va_yr(
        #         cfg.DATA_SHARE_DIR_PATH +
        #         cfg.EXIOMOD_DIR_PATH +
        #         cfg.file_name_base_eu28,
        #         cfg.var_name_va_p_new,
        #         cfg.yr_end,
        #     )

        #     # Aggregate sectors to EXIOMOD classification
        #     df_eb_ind_code2em_ind_agg = (
        #         pd.read_csv(cfg.INPUT_DIR_PATH +
        #                     cfg.EB_IND_CODE2EM_IND_AGG_FILE_NAME,
        #                     sep='\t',
        #                     index_col=[0, 1],
        #                     header=[0]))
        #     df_eb_ind_code2em_ind_agg = df_eb_ind_code2em_ind_agg.droplevel(axis=0,
        #                                                                     level=0)

        #     df_x_ie_em = df_x_ie.dot(df_eb_ind_code2em_ind_agg)
        #     df_x_ie_nuts2_em = df_x_ie_nuts2.unstack().dot(df_eb_ind_code2em_ind_agg)

        #     df_x_ie_nuts2_em_rel = df_x_ie_nuts2_em.divide(df_x_ie_em)
        #     df_x_ie_nuts2_em_rel.fillna(0, inplace=True)

        #     df_va_p_2030_base_ie = df_va_p_2030_base['EU28_IE']

        #     df_x_ie_nuts2_em_rel = df_x_ie_nuts2_em_rel[df_va_p_2030_base_ie.index]
        #     df_va_p_2030_base_ie_diag = pd.DataFrame(np.diag(df_va_p_2030_base_ie),
        #                                              index=df_va_p_2030_base_ie.index,
        #                                              columns=df_va_p_2030_base_ie.index)

        #     df_va_p_2030_base_ie_nuts2 = (
        #         df_x_ie_nuts2_em_rel.dot(df_va_p_2030_base_ie_diag))

    return df_x_cntr, df_x_nuts2


###
p_x_file_path = '../input/d_x.pkl'
p_va_file_path = '../input/d_va.pkl'
if __name__ == '__main__':

    # Choose pxp or ixi, and incl. or excl. UK.
    # To reproduce circumat: pxp and excl. uk, for redii: ixi and incl. uk.

    source = 'eb_ixi'
    # source = 'eb_pxp'
    # source = 'cm'

    reg = 'world'
    # reg = 'eu28'
    # reg = 'eu28exuk'
    # reg = 'IE'

    df_a_mr, df_y_mr, df_v_mr, df_x_mr = load_data(source, reg)

    d_cm_reg_nuts2_start = get_cm_reg_nuts2_start()
    # d_x = {}

    with open(p_va_file_path, 'rb') as read_file:
        d_va = pickle.load(read_file)

    for eu28_cntr_cm in d_cm_reg_nuts2_start:
        eu28_cntr_start = d_cm_reg_nuts2_start[eu28_cntr_cm]
        eu28_cntr_eb = cfg.d_eu28_cm2eb[eu28_cntr_cm]
        eu28_cntr_em = cfg.d_eu28_cm2em[eu28_cntr_cm]
        if eu28_cntr_start >= 264:
            print(eu28_cntr_cm, eu28_cntr_eb, eu28_cntr_start)
            df_x_cntr, df_x_nuts2 = x_cntr2nuts2(source,
                                                 eu28_cntr_cm,
                                                 eu28_cntr_eb,
                                                 # eu28_cntr_es,
                                                 eu28_cntr_start,
                                                 df_a_mr,
                                                 df_y_mr,
                                                 df_v_mr,
                                                 df_x_mr)
            d_x[eu28_cntr_em] = {}
            d_x[eu28_cntr_em]['x_cntr'] = df_x_cntr
            d_x[eu28_cntr_em]['x_nuts2'] = df_x_nuts2
    with open(p_x_file_path, 'wb') as write_file:
        pickle.dump(d_x, write_file)

    d_va = {}
    for eu28_cntr_em in cfg.l_eu28:
        va_cntr, va_nuts2 = va_cntr2nuts2(eu28_cntr_em,
                                          d_x[eu28_cntr_em]['x_cntr'],
                                          d_x[eu28_cntr_em]['x_nuts2'])
        d_va[eu28_cntr_em] = {}
        d_va[eu28_cntr_em]['va_cntr'] = va_cntr
        d_va[eu28_cntr_em]['va_nuts2'] = va_nuts2

    with open(p_va_file_path, 'wb') as write_file:
        pickle.dump(d_va, write_file)
