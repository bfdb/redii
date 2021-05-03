# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:04:16 2020

@author: navarrenhn
"""

import numpy as np
import pandas as pd
import pickle as pk
import matplotlib.pyplot as plt
from collections import defaultdict

import cfg

# with open('region_dict.pickle', 'rb') as handle:
#    region_dict = pk.load(handle)

# with open('CO2_dict.pickle', 'rb') as handle:
#    CO2_dict = pk.load(handle)

# with open('Total_dict.pickle', 'rb') as handle:
#    Total_dict = pk.load(handle)

# Pick countries you want to disaggregate
country_start = [183]
country = ["IE"]

for m, n in zip(country_start, country):
    print(m, n)
    # data_folder = "data/"

    # A_mr = np.load("A_v4.npy")
    # B_mr = np.load("B_v4.npy")
    # Y_mr = np.load("Y_v4.npy")

    data_folder = cfg.INPUT_DIR_PATH+'cm/'

    A_mr = np.load(data_folder+"A_v4.npy")
    B_mr = np.load(data_folder+"B_v4.npy")
    Y_mr = np.load(data_folder+"Y_v4.npy")

    # Remove non-EU countries.
    A_mr = np.delete(A_mr, np.s_[5400:9800], axis=1)
    A_mr = np.delete(A_mr, np.s_[5400:9800], axis=0)

    Y_mr = np.delete(Y_mr, np.s_[189:343], axis=1)
    Y_mr = np.delete(Y_mr, np.s_[5400:9800], axis=0)

    B_mr = np.delete(B_mr, np.s_[5400:9800], axis=1)

    A_mr_original = A_mr
    B_mr_original = B_mr
    Y_mr_original = Y_mr

    Y_mr_org = Y_mr
    A_mr_org = A_mr
    B_mr_org = B_mr

    # number of diferent parts in the final demand. THIS must be inputted
    n_y = 7
    # number of countries in the original mrio
    n_c = Y_mr.shape[1] / n_y  # number of countries in the original mrio
    n_c = int(n_c)
    n_c_org = n_c
    n_s = A_mr.shape[0] / n_c  # number of sectors (or products) in the original mrio
    n_s = int(n_s)
    n_b = B_mr.shape[0]  # number of environmental indicators
    n_b = int(n_b)
    n_v = 1  # number of diferent parts in the va
    n_v = int(n_v)
    n_r = 2  # this is always two, we will divide region into two parts

    X_rr_list = (
        []
    )  # this list will be used to recover the individual X_rr arrays of each region when calculating everything at once.
    L_mr_original = np.linalg.inv(np.identity(n_s * (n_c)) - A_mr_original)
    X_total_original = np.dot(L_mr_original, np.sum(Y_mr_original, axis=1))

    original_X_mr = np.dot(L_mr_original, np.sum(Y_mr_original, axis=1))
    Z_mr_original = np.dot(A_mr_original, np.array(np.diag(original_X_mr)))
    original_output_product = np.sum(Z_mr_original, axis=1) + np.sum(
        Y_mr_original, axis=1
    )

    VA_mr_original = np.array((original_X_mr) - np.sum(Z_mr_original, axis=0))

    regions = pd.read_excel(
        # data_folder + "circumat_regions_v3.xlsx"
        data_folder
        + "circumat_regions_v3.xls"
    )  # list including the table for country and its subnational details

    id_prev = 0
    Region_data = defaultdict(list)
    Reg_exp_total = []
    Reg_emp_total = []
    Excess_demand_list = []
    Region_names = []
    """ *** Pick any range of regions you'd like Check in the circumat_regions.xlsx for the numbers.
            266-311 (SK) is nice because it runs fairly quickly while having multiple regions.
            207-208 (LT) is also a good test...only has two regions, so it's easier to see the breakdown.
            ***"""

    """ *** INPUT: Adjust the start range of the for loop to equal the first subregion.
                   Update the if z> statement to match the start range.
                   Update the if id_rof != '' to be the country initials *** """

    for z in range(m, 311):

        """ *** This first portion focuses on importing the disaggregation data and building the national
                vs regional ratios, and finding the columns and rof of interest in the matrices. *** """

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
                np.array(range(0, 60))[:, None], np.array(range(0, n_c_org * n_s))
            ] = B_mr_original

            n_c = Y_mr.shape[1] / n_y  # number of countries in the original mrio
            n_c = int(n_c)

            n_s = (
                A_mr.shape[0] / n_c
            )  # number of sectors (or products) in the original mrio
            n_s = int(n_s)

            n_b = B_mr.shape[0]  # number of environmental indicators
            n_b = int(n_b)

        else:
            pass

        Nuts2 = z
        # find the region of interest =rof in the exiobase, i.e. the parent country of the region.
        # this is according to the exiobase numbering
        # here the exiobase starts from 1, parent id
        rof = int(regions.iloc[int(np.where(regions.iloc[:, 2] == Nuts2)[0]), 3])
        # find the name of the country
        name_rof = regions.iloc[int(np.where(regions.iloc[:, 2] == rof)[0]), 0]
        # find the  id  of the nuts2; the code of it
        id_Nuts2 = regions.iloc[int(np.where(regions.iloc[:, 2] == Nuts2)[0]), 1]
        # find the label of the country; the code of it. that is the frst two letter of above
        id_rof = id_Nuts2[0:2]

        # Stop the code from running on to a new nation.

        if id_rof != n:
            break

        id_prev = id_rof
        Region_names.append(id_Nuts2)
        print(id_Nuts2)

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

        """
        reg_exp_shares_all[0][0] = 'SL03'
        reg_exp_shares_all[0][1] = 'SL04'
        """

        # turn reg_exp_shares_all of the country into another matrix the rest of the country  as region 1 and the selected nuts 2 as region 2
        reg_exp_shares = np.zeros((n_y, n_r))
        # first fınd the nuts 2
        internal_id_Nuts2 = (np.where(reg_exp_shares_all.iloc[:, 0] == id_Nuts2)[0])[0]
        print(f"internal_id_Nuts2 {internal_id_Nuts2} id_Nuts2 {id_Nuts2}")
        # write the nuts 2 income data into the second column, and scale it with the sum of all income in the country
        reg_exp_shares[:, 1] = reg_exp_shares_all.iloc[internal_id_Nuts2, 1] / np.sum(
            reg_exp_shares_all.iloc[:, 1], axis=0
        )
        # then fll in the rest of the nation details i.e. all sum minus the nuts2 in the column 1
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
        # turn it into another matrix the rest of the country  as region 1 and the selected nuts 2 as region 2

        sbs_emp_numbers = np.zeros((sbs_emp_numbers_all.shape[1] - 1, n_r))
        # first fınd the nuts 2
        internal_id_Nuts2 = (np.where(sbs_emp_numbers_all.iloc[:, 0] == id_Nuts2)[0])[0]
        # first fill the nuts 2 region details
        sbs_emp_numbers[:, 1] = sbs_emp_numbers_all.iloc[
            internal_id_Nuts2, 1 : sbs_emp_numbers_all.shape[1]
        ]
        # then fll in the rest of the nation details i.e. all sum minus the nuts2
        sbs_emp_numbers[:, 0] = (
            np.sum(
                sbs_emp_numbers_all.iloc[:, 1 : sbs_emp_numbers_all.shape[1]], axis=0
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

        # conversıon of the sectors ın eurostat to exıobase starts..
        # for sbs
        conversion_matrix = pd.read_excel(
            # data_folder + "SBS_MATCH.xlsx", sheet_name="matrix", header=None
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

        # Why is convert_matrix calculated? It goes unused.
        convert_matrix = conversion_matrix * np.reshape(
            np.repeat(1 / (rowsum_conversion_matrix + +(10 ** (-31))), ncols),
            [nrows, ncols],
        )

        sbs_emp_numbers_all_in_exiobase = np.dot(
            np.transpose(sbs_emp_numbers), convert_matrix
        )
        sbs_emp_numbers_all_in_exiobase = np.transpose(sbs_emp_numbers_all_in_exiobase)

        reg_emp_numbers = sbs_emp_numbers_all_in_exiobase

        # convert them to numpy arrays
        reg_emp_numbers = np.array(reg_emp_numbers)
        reg_exp_shares = np.array(reg_exp_shares)

        # calculate the total  employment for each sector in whole country
        tot_emp = np.dot(reg_emp_numbers, np.ones((n_r, 1)))

        # calculate the employment shares in each region for each sector
        # what is the ratio between (sector S workers in region R) and (total employment of sector S)
        # it shows the share of that sector per region
        emp_shares = np.multiply(reg_emp_numbers, np.reciprocal(tot_emp + 10 ** (-31)))

        # calculate the location quotient in each region for each sector
        # what is the ratio between (employment share of sector S in region R)
        # and (employment share of S ?n all country)
        # share of people workin in that region as opposed to all country
        reg_emp_share = np.sum(reg_emp_numbers, axis=0) / (
            np.sum(np.sum(reg_emp_numbers, axis=0)) + 10 ** (-31)
        )
        # location_quatients=emp_shares./reg_emp_share
        location_quatients = emp_shares / (reg_emp_share + 10 ** (-31))

        # find the rows and column indices of the country in the exiobase in py (ie index starts from 0)
        Zcolumns_of_rof = np.array(range(rof * n_s - (n_s - 1) - 1, rof * n_s)) - 200
        Ycolumns_of_rof = np.array(range(rof * n_y - (n_y - 1) - 1, rof * n_y)) - 7
        Zrows_of_rof = np.array(range(rof * n_s - (n_s - 1) - 1, rof * n_s)) - 200

        """ *** The second partion of this code focuses on building the new regional matrix values according
                to the disaggregation calculations done before. Early in the code A_mr and Y_mr are updated
                to A_mr_disagg and Y_mr to include the previously disaggregated regions. *** """
        # calculate the leontief
        L_mr = np.linalg.inv(np.identity(n_s * n_c) - A_mr)

        X_total = np.dot(L_mr, np.sum(Y_mr, axis=1))
        X_total[range(0, n_c_org * n_s)] = X_total_original
        Z_mr = np.dot(A_mr, np.diag(X_total))

        # check whether this is correct.  this sum should be zero
        X_check = np.sum(Z_mr, axis=1) + np.sum(Y_mr, axis=1) - X_total

        X_rof = X_total[Zrows_of_rof]

        R_x = (
            np.transpose(np.tile(X_rof, (2, 1))) * emp_shares
        )  # it gives an ns by nr matrix
        X_rr = np.reshape(
            R_x, n_r * n_s, order="F"
        )  # thus reshape it to a column matrix. respahe function takes the first column first and etc.

        A_rof = A_mr[Zrows_of_rof[:, None], Zcolumns_of_rof]

        # for each sector in each new region: miller and blair- page 367
        basic_demand = np.minimum(location_quatients, 1)
        excess_demand = np.subtract(1, basic_demand)

        # find the technical coeff
        # what can the sector output to the sectors in the region
        A_r1r1 = A_rof * np.reshape(np.array(basic_demand[:, 0]), (n_s, 1))
        A_r2r2 = A_rof * np.reshape(np.array(basic_demand[:, 1]), (n_s, 1))

        # what is the trade between the sectors in rest of the nation and the nuts 2 region
        A_r1r2 = A_rof * np.reshape(np.array(excess_demand[:, 1]), (n_s, 1))
        A_r2r1 = A_rof * np.reshape(np.array(excess_demand[:, 0]), (n_s, 1))

        A_rr = np.concatenate(
            (
                np.concatenate((A_r1r1, A_r2r1), axis=1),
                np.concatenate((A_r1r2, A_r2r2), axis=1),
            ),
            axis=0,
        )

        Z_rr = np.dot(A_rr, np.diag(X_rr))

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

        # calculate regional value added
        VA_mr = np.array((X_total) - np.sum(Z_mr, axis=0))
        VA_rof = VA_mr[Zcolumns_of_rof]
        # so value of added are scaled according to the regional output shares
        VA_r1 = VA_rof * R_x[:, 0] / (X_rof + 10 ** (-31))
        VA_r2 = VA_rof * R_x[:, 1] / (X_rof + 10 ** (-31))
        VA_rr = np.concatenate((VA_r1, VA_r2))

        # lets go to the updated mr database
        # the new regıon 2 ıs added at the end of the natabase whereas ıts parent country stays the same
        new_Zcolumns_of_region2 = np.array(range((n_c) * n_s, (n_c + 1) * n_s))
        new_Ycolumns_of_region2 = np.array(range((n_c) * n_y, (n_c + 1) * n_y))
        new_Zrows_of_region2 = np.array(range((n_c) * n_s, (n_c + 1) * n_s))

        # allocate a free database with number of countrıes ıncreased by 1
        A_mr_disagg = np.zeros(((n_c + 1) * n_s, (n_c + 1) * n_s))
        A_mr[
            np.array(range(0, n_c_org * n_s))[:, None],
            np.array(range(0, n_c_org * n_s)),
        ] = A_mr_org
        A_mr_disagg[
            np.array(range(0, (n_c) * n_s))[:, None], np.array(range(0, (n_c) * n_s))
        ] = A_mr

        # dublicate the rows and the columns of country of interest

        # rows according to the output shares
        A_mr_disagg[Zrows_of_rof[:, None], range(0, (n_c) * n_s)] = A_mr[
            Zrows_of_rof, :
        ] * np.reshape(np.array((R_x[:, 0]) / (X_rof + 10 ** (-31))), (n_s, 1))
        A_mr_disagg[new_Zrows_of_region2[:, None], range(0, (n_c) * n_s)] = A_mr[
            Zrows_of_rof, :
        ] * np.reshape(np.array((R_x[:, 1]) / (X_rof + 10 ** (-31))), (n_s, 1))
        # columns stays the same product recipe

        A_mr_disagg[np.array(range(0, (n_c) * n_s))[:, None], Zcolumns_of_rof] = A_mr[
            :, Zcolumns_of_rof
        ]
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
        )  # A_r2r2#*np.reshape(location_quatients[:,1],(n_s,1))
        A_mr_disagg[Zrows_of_rof[:, None], new_Zcolumns_of_region2] = A_r1r2
        A_mr_disagg[new_Zcolumns_of_region2[:, None], Zcolumns_of_rof] = A_r2r1

        # for value added first dublicate the initial one
        # VA_mr_disagg=np.zeros(((n_c+1)*n_s ))
        # VA_mr_disagg[np.array(range(0,(n_c )*n_s )) ]=VA_mr
        # correct the values of the regions
        # VA_mr_disagg[Zcolumns_of_rof]=VA_r1
        # VA_mr_disagg[new_Zcolumns_of_region2]=VA_r2

        # dublication of y is similar to z but regional expend shares will come in
        Y_mr_disagg = np.zeros(((n_c + 1) * n_s, (n_c + 1) * n_y))
        Y_mr[
            np.array(range(0, n_c_org * n_s))[:, None],
            np.array(range(0, n_c_org * n_y)),
        ] = Y_mr_org
        Y_mr_disagg[
            np.array(range(0, (n_c) * n_s))[:, None], np.array(range(0, (n_y * (n_c))))
        ] = Y_mr

        Y_mr_disagg[np.array(range(0, (n_c) * n_s))[:, None], Ycolumns_of_rof] = Y_mr[
            :, Ycolumns_of_rof
        ] * np.array(reg_exp_shares[:, 0])
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

        # calculate new L
        desired_X_mr = np.array(np.zeros((n_s * (n_c + 1))))
        desired_X_mr[np.array(range(0, (n_c) * n_s))] = np.array(
            X_total[np.array(range(0, (n_c) * n_s))]
        )
        desired_X_mr[new_Zrows_of_region2] = np.array(X_rr[np.array(range(0, n_s))])
        desired_X_mr[Zrows_of_rof] = np.array(X_rr[np.array(range(n_s, 2 * n_s))])

        X_rr_list.append(X_rr)

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
        Region_data[id_Nuts2].append(A_mr_org[Zrows_of_rof[:, None], Zcolumns_of_rof])

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
        Zprev_row = Zrows_of_rof - 200
        B_mr_disagg[:, new_Zcolumns_of_region2] = B_mr[:, Zrows_of_rof]

    """This was the tricky part. Essentially you have to build the excess demands list of each region for each sector before assigning
       any values. By doing this you can see which regions have excess demand and which don't, based on that you can see which will
       export and which won't. This adjusts the ratio of the original total. This ratio is built based on the income % of each
       region (this could also be adjusted for jobs and we can compare the results)
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
    for i in range(n_c_org * n_s, n_s * n_c, 200):
        print(reg_count, i)
        # Add add in the row data according to ratio of regions that are expected to export based on demand.
        Y_mr_disagg[
            np.array(range(i, i + 200))[:, None], np.array(range(0, n_c_org * n_y))
        ] = Y_mr_org[
            Zrows_of_rof[:, None], np.array(range(0, n_c_org * n_y))
        ] * np.reshape(
            np.array(Excess_demand_list[reg_count][:, 1] * Reg_exp_total[reg_count]),
            (n_s, 1),
        )

        reg_count += 1

    Y_mr_disagg_final = Y_mr_disagg
    Y_mr_disagg_final[
        np.array(range(0, n_c_org * n_s))[:, None], np.array(range(0, n_c_org * n_y))
    ] = Y_mr_original

    reg_count = 0
    for i in range(n_c_org * n_s, n_s * n_c, 200):
        A_mr_disagg[
            np.array(range(i, i + 200))[:, None], np.array(range(0, n_c_org * n_s))
        ] = A_mr_org[
            Zrows_of_rof[:, None], np.array(range(0, n_c_org * n_s))
        ] * np.reshape(
            np.array(Excess_demand_list[reg_count][:, 1] * Reg_exp_total[reg_count]),
            (n_s, 1),
        )
        reg_count += 1
    A_mr_disagg_final = A_mr_disagg
    A_mr_disagg_final[
        np.array(range(0, n_c_org * n_s))[:, None], np.array(range(0, n_c_org * n_s))
    ] = A_mr_original
    # This builds out the interregional data according to Yr1r2 and regional income relationships.
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
                    np.array(range(count, count + 200))[:, None],
                    np.array(range(j, j + 7)),
                ] = (temp * factor)
            reg_count += 1

        reg_count = 0
        for b in range(n_c_org * n_s, n_s * n_c, 200):
            num = Region_data[i][0]
            temp = Region_data[i][11]  # + Region_data[i][9]
            factor = (Reg_exp_total[reg_count]) / (1 - num)

            A_mr_disagg_final[
                np.array(range(count, count + 200))[:, None],
                np.array(range(b, b + 200)),
            ] = (temp * num)
            reg_count += 1

        count += 200

    # Delete original nation after all regions are built out to avoid double counting.
    Y_mr_disagg_final[Zrows_of_rof, :] = 0
    Y_mr_disagg_final[:, Ycolumns_of_rof] = 0

    A_mr_disagg_final[Zrows_of_rof, :] = 0
    A_mr_disagg_final[:, Zcolumns_of_rof] = 0

    """ Check sum of regional Y values vs. orginal Y """
    Y_disagg_total = np.sum(np.sum(Y_mr_disagg_final, axis=0))
    Y_org_total = np.sum(np.sum(Y_mr_original, axis=0))
    print("Y_disagg total: ", Y_disagg_total)
    print("Y_origin total: ", Y_org_total)

    # Check the individual sector ratios of the disagg and orignial Y matrix
    Y_check_disagg = np.sum(Y_mr_disagg_final, axis=1)
    Y_check_org = np.sum(Y_mr_original, axis=1)

    Y_checks = pd.DataFrame()
    for i in range(n_c_org * n_s, (n_c * n_s), 200):
        Y_checks[i] = np.array(Y_check_disagg[i : i + 200])

    Y_check = Y_checks.sum(axis=1)
    # ratioY = Y_check/Y_check_org[3000:3200]

    """ Calculate the final final output product """
    L_mr_disagg_final = np.linalg.inv(np.identity(n_s * (n_c)) - A_mr_disagg_final)
    desired_X_mr_final = np.dot(L_mr_disagg_final, np.sum(Y_mr_disagg_final, axis=1))
    Z_mr_disagg_final = np.dot(A_mr_disagg_final, np.array(np.diag(desired_X_mr_final)))
    final_output_product_disagg = np.sum(Z_mr_disagg_final, axis=1) + np.sum(
        Y_mr_disagg_final, axis=1
    )

    # Caclculate final outputs with the finalized matrices
    # final_output_product_disagg = np.sum(Z_mr_disagg_final, axis=1) + np.sum(Y_mr_disagg_final, axis=1)
    # final_output_product_original = np.sum(Z_mr_original, axis=1) + np.sum(Y_mr_original, axis=1)

    # X_mr_disagg1 = np.dot(L_mr_disagg_final,np.sum(Y_mr_disagg_final,axis=1))
    # Z_mr_disagg1= np.dot(A_mr_disagg_final, np.array(np.diag(X_mr_disagg1)))
    # final_output_product_disagg1 = np.sum(Z_mr_disagg1, axis=1) + np.sum(Y_mr_disagg_final, axis=1)

    """Sum the regional output products and check if they match the orginal national acccount. """
    regional_final_output_all_disagg = pd.DataFrame()
    count = 0
    for i in range(n_c_org * n_s, (n_c * n_s), 200):
        regional_final_output_all_disagg[Region_names[count]] = np.array(
            final_output_product_disagg[i : i + 200]
        )
        count += 1

    regional_output_check = regional_final_output_all_disagg.sum(axis=1)
    national_output_check = original_output_product[Zrows_of_rof]
    ratioX = regional_output_check / original_output_product[Zrows_of_rof]

    #%%
    # Some metrics to get an idea of how different the final output totals are.
    print("Regions total output=", int(np.sum(regional_output_check)))
    print("Original nation output=", int(np.sum(original_output_product[Zrows_of_rof])))

    #%%
    regional_final_output_all_disagg.sum(axis=0)
    # region_dict[id_prev] = np.array(regional_final_output_all_disagg.sum(axis = 0))

    """
    #Calculate the emission vector
    emissions_org = B_mr_org * original_X_mr

    emissions_old = emissions_org[:,np.array(range(3800,4000))]
    emissions_old_sum = np.sum(emissions_old, axis = 1)
    print(emissions_old_sum[4])

    CO2_dict['MT'] = emissions_old_sum[4]


    emissions_test = B_mr_disagg * final_output_product_disagg
    emissions_test = emissions_test[:,np.array(range(9800,10200))]
    emissions_test_sum = np.sum(emissions_test, axis = 1 )
    #print(emissions_old_sum[4])

    """
    # Production Based Emissions
    # temp = np.dot(L_mr_disagg_final,np.diag(np.sum(Y_mr_disagg_final,axis=1)))
    # emissions = B_mr_disagg * np.dot(L_mr_disagg_final,np.diag(np.sum(Y_mr_disagg_final,axis=1)))

    user_selected_products = np.intc(np.array(range(0, 200)))
    user_selected_country = n_c + 1
    user_selected_emissions = np.intc(np.array(range(0, 60)))

    # calculate the exiobase internal id s (starting from 0) of the products
    user_selected_products_ids = np.intc(
        np.zeros((n_c, (user_selected_products).shape[0]))
    )
    # for i in range(0,user_selected_products.shape[0]):
    #    user_selected_products_ids[:,i]=np.array(range(user_selected_products[i]-1,n_s*(n_c+1),n_s))

    # take always the new nuts2 region
    # y_NUTS2=np.array(np.zeros((n_s*(n_c),n_y)))
    # only take the selected products
    # y_NUTS2[user_selected_products_ids.flatten()]=Y_mr_disagg[user_selected_products_ids.flatten()[:, None],np.array(range((user_selected_country-1)*n_y ,(user_selected_country)*n_y ))]

    # Consumer Based Emissions
    VA_mr_disagg = np.array((desired_X_mr_final - np.sum(Z_mr_disagg_final, axis=1)))
    final_input_mr_disagg = np.sum(Z_mr_disagg_final, axis=0) + VA_mr_disagg

    emissions = B_mr_disagg * final_input_mr_disagg

    with open(id_prev + "_Emissions.pk", "wb") as handle:
        pk.dump(emissions, handle, protocol=pk.HIGHEST_PROTOCOL)

    emissions_disagg = []
    emissions_dict = defaultdict(list)

    for i, j in zip(range(n_c_org * n_s, (n_c * n_s), 200), Region_data):

        emissions_reg = emissions[:, np.array(range(i, i + 200))]
        emissions_reg = np.sum(emissions_reg, axis=1)
        CO2_emissions = emissions_reg[5]
        emissions_disagg.append(CO2_emissions)
        emissions_dict[j].append(emissions_reg)
        emissions_dict[j].append(Region_data[j][12])
    # print(sum(emissions_disagg))

    with open(id_prev + "_Emissions_Cons_Data.pk", "wb") as handle:
        pk.dump(emissions_dict, handle, protocol=pk.HIGHEST_PROTOCOL)

    # print(sum(emissions_disagg))
    B_mr_disagg_final = B_mr_disagg
    #%%

    emissions = B_mr_disagg * desired_X_mr_final
    emissions_disagg = []
    emissions_dict = defaultdict(list)

    with open(id_prev + "_Emissions_Cons.pk", "wb") as handle:
        pk.dump(emissions, handle, protocol=pk.HIGHEST_PROTOCOL)

    for i, j, z in zip(
        range(n_c_org * n_s, (n_c * n_s), 200),
        Region_data,
        range(n_c_org * n_y, n_y * n_c, 7),
    ):

        y_NUTS2 = np.array(np.zeros((n_c * n_s, n_y)))
        y_NUTS2 = Y_mr_disagg[:, np.array(range(z, z + 7))]
        y_NUTS2 = y_NUTS2
        mtemp = np.dot(L_mr_disagg_final, np.diag(np.sum(y_NUTS2, axis=1)))
        mbtemp = B_mr_disagg
        # y_NUTS2[user_selected_products.flatten()]=Y_mr_disagg[user_selected_products.flatten()[:, None],np.array(range((z, z+7)))]
        emissions_reg = np.dot(
            B_mr_disagg, np.dot(L_mr_disagg_final, np.diag(np.sum(y_NUTS2, axis=1)))
        )
        emissions_reg = np.sum(emissions_reg, axis=1)
        # emissions_reg = B_mr_disagg[:,Zrows_of_rof] * np.dot(L_mr_disagg_final,np.diag(np.sum(Y_mr_disagg_final[:,np.array(range(z,z+7))],axis=1)))
        # emissions_reg = emissions[:,np.array(range(i,i+200))]
        # emissions_reg = np.sum(emissions_reg, axis = 1)
        CO2_emissions = emissions_reg[5]
        emissions_disagg.append(CO2_emissions)
        emissions_dict[j].append(emissions_reg)
        emissions_dict[j].append(Region_data[j][12])

    print(sum(emissions_disagg))
    # CO2_dict[id_prev] = emissions_disagg

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
    #%%
    """ Save output disagg data """

    # with open('region_dict.npy', 'wb') as handle:
    #    np.save(handle, region_dict)

    # with open(id_prev+'_Z_matrix.npy', 'wb') as handle:
    #    np.save(handle, Z_mr_disagg_final)

    with open(id_prev + "_A_matrix_S.npy", "wb") as handle:
        np.save(handle, A_mr_disagg_final, handle)

    with open(id_prev + "_Y_matrix_S.npy", "wb") as handle:
        np.save(handle, Y_mr_disagg_final)

    with open(id_prev + "_B_matrix_S.npy", "wb") as handle:
        np.save(handle, B_mr_disagg)

    with open(id_prev + "_EmissionsData.pk", "wb") as handle:
        pk.dump(emissions_dict, handle, protocol=pk.HIGHEST_PROTOCOL)

    #%%
    print("VA Disagg:", np.sum(VA_mr_disagg))
    print("VA Original:", np.sum(VA_mr_original))
    print("VA Disagg:", np.sum(VA_mr_disagg))
    print("VA Original:", np.sum(VA_mr_original))
    print("VA Disagg:", np.sum(VA_mr_disagg))
    print("VA Original:", np.sum(VA_mr_original))