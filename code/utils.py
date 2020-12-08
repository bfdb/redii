# -*- coding: utf-8 -*-
""" Utils module for paper on
    global employment and GDP impact of Renewable Energy Directive II
    Copyright (C) 2020

    Bertram F. de Boer
    Faculty of Science
    Institute of Environmental Sciences (CML)
    Department of Industrial Ecology
    Einsteinweg 2
    2333 CC Leiden
    The Netherlands

    +31 (0)71 527 1478
    b.f.de.boer@cml.leidenuniv.nl

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import csv
import os

import cfg


def log(str_log):
    """ Log console output to file.

    """
    print('\n{}'.format(str_log))
    with open(cfg.LOG_DIR_PATH+cfg.LOG_FILE_NAME, cfg.log_mode) as write_file:
        csv_file = csv.writer(write_file,
                              delimiter='\t',
                              lineterminator='\n')
        csv_file.writerow([str_log])


def makedirs():
    """ Make directories for results, tests, and logs.

    """
    list_log_makedirs = []
    list_log_makedirs.append('Making output directories in:')
    list_log_makedirs.append('    {}'.format(cfg.OUTPUT_DIR_PATH))
    for output_dir_path in cfg.LIST_OUTPUT_DIR_PATH:
        try:
            os.makedirs(output_dir_path)
        except FileExistsError:
            list_log_makedirs.append(
                '    Output directory already exists:')
            list_log_makedirs.append(
                '    {}'.format(output_dir_path))
            list_log_makedirs.append(
                '    This run will overwrite previous output.')
    for log_makedirs in list_log_makedirs:
        log(log_makedirs)
        cfg.log_mode = 'a'


def cntr2reg(dict_code2cntr, dict_code2reg):
    dict_cntr2reg = {}
    for code in dict_code2cntr:
        if code in dict_code2reg:
            cntr = dict_code2cntr[code]
            reg = dict_code2reg[code]
            dict_cntr2reg[cntr] = reg
