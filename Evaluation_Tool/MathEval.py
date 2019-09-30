# -*- coding: utf-8 -*-
#################################################################################
#Program    :   MathEval.py                                                     #
#Version    :   20111123 (date of last modification)                            #
#Author     :   HuXuan (huxuan@icst.pku.edu.cn)                                 #
#               LinXiaoYan (lingxiaoyan@pku.edu.cn)                             #
#Usage      :                                                                   #
#   0)  Make sure your script is the latest version                             #
#   1)  Copy Ground Truth file in the folder 'GT'                               #
#       (the folder name can be changed by modify the source code)              #
#   2)  Copy Machine Detection file in the folder 'MD'                          #
#       (the folder name can also be changed)                                   #
#   3)  Make folder 'GT', folder 'MD' and 'MathEval.py' under the same folder   #
#   4)  Run the python script via command line or just double click it          #
#   5)  The result will be shown in 'MathEval.csv'                              #
#       Time used can be seen in the command line                               #
                                                                                #
#Some variable abbreviation:                                                    #
#   E: EmbeddedFormula, I: IsolatedFormula                                      #
#   l: left, r:right, t: top, b:bottom                                          #
#   p: path, dir: directory                                                     #
#   gt: Ground Truth, md: Machine Detection                                     #
#   cor: Correct, mis: Miss, fal: False, par: Partial                           #
#   exp: Expand, pae: Partial&Expand, mer: Merge, spl: Split                    #
#################################################################################

import os
import struct
import string
import datetime
import xml.dom.minidom
from bbox import BBox

weight_type = {'cor':1.0, 'mis':1.0, 'fal':1.0, 'par':1.0, 'exp':1.0, 'pae':1.0,
               'mer':1.0, 'spl':1.0} # Weight of various evaluation types

ratio_full = 0.95 # 0.95 # Lower bound ration indicates full overlap
ratio_none = 0.05 # Higher bound ratio indicates none overlap

path_sum = 'MathEval.csv' # Output file of statistical data

formula_type = ['E'] # Formula type: EmbeddedFormula and IsolatedFormula
eval_type = ['cor', 'mis', 'fal', 'par', 'exp', 'pae', 'mer', 'spl'] # Evaluation types:

tot_example = {'Ecor':0,'Emis':0,'Efal':0,'Epar':0,'Eexp':0,'Epae':0,'Emer':0,'Espl':0,
               'Icor':0,'Imis':0,'Ifal':0,'Ipar':0,'Iexp':0,'Ipae':0,'Imer':0,'Ispl':0,
               'tot':0} # Types for statistics
sum_tot = tot_example.copy() # Total number for each types
sco_tot = tot_example.copy() # Total score for each types

def float_max(num1, num2):
    """docstring for float_max
    Summary:
        Get the biggger one of two float
    Parameter:
        [input]     num1    -   the 1st float
        [input]     num2    -   the 2nd float
        [return]    the bigger float
    """
    return num1 - num2 > 1e-8 and num1 or num2

def float_min(num1, num2):
    """docstring for float_min
    Summary:
        Get the smaller on of two float
    Parmeter:
        [input]     num1    -   the 1st float
        [input]     num2    -   the 2nd float
        [retrun]    the smaller float
    """
    return num1 - num2 > 1e-8 and num2 or num1

def float_compare(num1, num2):
    """docstring for float_compare
    Summary:
        Compare two float
    Parameter:
        [input]     num1    -   the 1st float
        [input]     num2    -   the 2nd float
        [retrun]    result of comparation
                    1:the 1st is bigger, -1:the 2nd is bigger, 0: equal
    """
    if num1 - num2 > 1e-8:
        return 1
    elif num2 - num1 > 1e-8:
        return -1
    else:
        return 0

def cal_common_area(rect1, rect2):
    """docstring for cal_common_area
    Summary:
        Calculate the common area of two rects
    Parameter:
        [input]     rect1   -   the 1st rect
        [input]     rect2   -   the 2nd rect
        [retrun]    the area of overlap
    """
    # Get the bound of common area
    l = float_max(rect1['l'], rect2['l'])
    t = float_min(rect1['t'], rect2['t'])
    r = float_min(rect1['r'], rect2['r'])
    b = float_max(rect1['b'], rect2['b'])
    # Common area is valid only when r>l and t>b, otherwise 0 should be returned
    return (0, (r-l)*(b-t))[float_compare(r,l)==1 and float_compare(b,t)==1]

def cal_relation(area, area1, area2):
    """docstring for cal_relation
    Summary:
        Calculate the relation between the rects
    Parameter:
        [input]     area    -   common area of the two rects
        [input]     area1   -   area of 1st rect
        [input]     area2   -   area of 2nd rect
        [return]    the number indicates the relation
                    0 : the relation hasn't been calculated yet
                    1 : rect1 and rect2 are fully overlapped
                    2 : rect1 and rect2 are not overlaped at all
                    3 : rect1 is the sub-rect of rect2
                    4 : rect2 is the sub-rect of rect1
                    5 : rect1 and rect2 BOTH have overlapping and seperate part
    """
    if area > area1 * ratio_full and area > area2 * ratio_full:
        return 1
    # TODO, the logic here might not be very correct
    # could be both overlaping and separate, buth the threshold is key here.
    if area < area1 * ratio_none and area < area2 * ratio_none:
        return 2
    if area > area1 * ratio_full and area < area2 * ratio_full:
        return 3
    if area < area1 * ratio_full and area > area2 * ratio_full:
        return 4
    return 5


def add_value(sum, type, num = 1, sco=0.0):
    """docstring for add_value
    Summary:
        Add value for statistics
    Parameter:
        [input]     sum     -   the sum for each page
        [input]     type    -   the Formula+Evaluation type
        [input]     num     -   the number to be add
        [input]     sco     -   the score to be add
    """
    global sum_tot
    sum_tot[type] += num
    sum_tot['tot'] += num
    sco_tot[type] += sco

    sum[type] += num
    sum['tot'] += num


def eval(gt, md):
    """

    :param gt:
    :param md:
    :param filename:
    :return:
        return the count under each matching categories
    """
    # update the area if not have
    for gt_idx in range(len(gt)):
        if 'area' not in gt[gt_idx]:
            gt[gt_idx]['area'] = (gt[gt_idx]['rect']['r'] - gt[gt_idx]['rect']['l']) * \
                                 (gt[gt_idx]['rect']['t'] - gt[gt_idx]['rect']['b'])
    for md_idx in range(len(md)):
        if 'area' not in md[md_idx]:
            md[md_idx]['area'] = (md[md_idx]['rect']['r'] - md[md_idx]['rect']['l']) * \
                                 (md[md_idx]['rect']['t'] - md[md_idx]['rect']['b'])

    sum = tot_example.copy()  # Initialize the sum for current page

    # Calculate the common area and relation among all rects
    common_area = [[0 for j in range(len(md))] for i in range(len(gt))]
    relation = [[0 for j in range(len(md))] for i in range(len(gt))]
    for i in range(len(gt)):
        for j in range(len(md)):
            common_area[i][j] = cal_common_area(gt[i]['rect'], md[j]['rect'])
            relation[i][j] = cal_relation(common_area[i][j], gt[i]['area'], md[j]['area'])

    # Mark wheather the rect has been used for evaluation
    gt_mark = [True for i in range(len(gt))]
    md_mark = [True for j in range(len(md))]

    debug_j_idx = 27

    sum['partial_bbox_list'] = []
    for j in range(len(md)):
        # from view of prediction.

        if j == debug_j_idx:
            for i in range(len(gt)):
                print i, j, relation[i][j]
            pass

        # correct
        for i in range(len(gt)):
            if relation[i][j] == 1:
                gt_mark[i] = False
                md_mark[j] = False
                add_value(sum, md[j]['type'] + 'cor', 1)
        if not md_mark[j]:
            continue

        # expand and merge
        indexs_exp = []
        area_sum = 0
        for i in range(len(gt)):
            if relation[i][j] == 3:
                indexs_exp.append(i)
                area_sum += common_area[i][j]
                gt_mark[i] = False
        if indexs_exp:
            md_mark[j] = False
            if j == debug_j_idx:
                pass
            if area_sum > md[j]['area'] * ratio_full:
                add_value(sum, md[j]['type'] + 'mer', 1, 1.0 / len(indexs_exp))
            else:
                add_value(sum, md[j]['type'] + 'exp', 1, area_sum / md[j]['area'])
        if not md_mark[j]:
            continue

        # partial split/expand
        # first get the gt contain the current j
        # then check the number of total contain

        contain_i = None
        for i in range(len(gt)):
            if relation[i][j] == 4:
                contain_i = i
                break
        if contain_i is not None:
            md_mark[j] = False
            pd_j_list = []
            area_sum = 0
            for tmp_j in range(len(md)):
                if relation[contain_i][tmp_j] == 4:
                    pd_j_list.append(tmp_j)
                    area_sum += common_area[contain_i][tmp_j]

            if len(pd_j_list) == 0:
                raise Exception("SHould at least have something")
            elif len(pd_j_list) > 1 and area_sum > gt[contain_i]['area']*ratio_full:
                # split is about the ground truth
                gt_mark[contain_i] = False
                add_value(sum, gt[contain_i]['type'] + 'spl', 1, 1.0 / len(pd_j_list))
            else:
                gt_mark[contain_i] = False
                add_value(sum, md[pd_j_list[0]]['type'] + 'par', 1,
                          area_sum / gt[contain_i]['area'])
                #for tmp_j in pd_j_list:
                #    sum['partial_bbox_list'].append(md[tmp_j])
                sum['partial_bbox_list'].append(md[j])

        if not md_mark[j]:
            continue

        # the last PAE checking
        for i in range(len(gt)):
            if relation[i][j] not in [1, 2]:
                gt_mark[i] = False
                md_mark[j] = False
                add_value(sum, md[j]['type'] + 'pae', 1, common_area[i][j] / md[j]['area'])


    # for the gt that overlaps, marked as pae
    for i in range(len(gt)):
        if gt_mark[i]:
            for j in range(len(md)):
                if relation[i][j] not in [1, 2]:
                    gt_mark[i] = False
                    add_value(sum, md[j]['type'] + 'pae', 1, common_area[i][j] / md[j]['area'])

    # by the end
    # False
    # for later stage of statistics
    sum['false_bbox_list'] = []
    sum['false_case_list'] = []
    for j in range(len(md)):
        if md_mark[j]:
            md_mark[j] = False
            if j == debug_j_idx:
                pass

            add_value(sum, md[j]['type'] + 'fal', 1)

            tmp_str = ""
            for i in range(len(gt)):
                tmp_str += "{}:{}:{}, ".format(
                    i, common_area[i][j], relation[i][j])

            sum['false_bbox_list'].append(BBox([
                md[j]['rect']['l'],
                md[j]['rect']['b'],
                md[j]['rect']['r'],
                md[j]['rect']['t']
            ]))
            sum['false_case_list'].append(md[j])

    # Miss
    sum['miss_bbox_list'] = []
    for i in range(len(gt)):
        if gt_mark[i]:  # true means not used
            gt_mark[i] = False
            add_value(sum, gt[i]['type'] + 'mis', 1)

            # the missing
            sum['miss_bbox_list'].append(BBox([
                gt[i]['rect']['l'],
                gt[i]['rect']['b'],
                gt[i]['rect']['r'],
                gt[i]['rect']['t']
            ]))

    # f = file(path_sum, 'a')
    # print >> f, filename,
    # for i in formula_type:
    #     for j in eval_type:
    #         print >> f, ',', sum[i + j],
    # print >> f, ',', sum['tot']
    # f.close()
    return sum

def parse_xml(p_xml):
    """docstring for parse_xml
    Summary:
        Parse the xml just handle some exceptions
    Parameter:
        [input]     p_xml   -   path of the xml file
        [returm]    flag    -   boolean to indicate wheather parsed successfully
        [return]    xmldoc  -   xml document variable of the xml file, None for failing to parse
    """
    flag = True
    try:
        xmldoc = xml.dom.minidom.parse(p_xml)
    except:
        try:
            # Try to replace unprintable chars and parse via string
            f = file(p_xml, 'rb')
            s = f.read()
            f.close()

            ss = s.translate(None, string.printable)
            s = s.translate(None, ss)

            xmldoc = xml.dom.minidom.parseString(s)
        except:
            xmldoc = None
            flag = False
    return flag, xmldoc

def hexlongbits2double(str):
    """docstring for hexlongbits2double
    Summary:
        Conver the longbits in hex to double

        Q is the unsigned long long
        d is double
    Parameter:
        [input]     str     -   string of the longbits in hex
        [return]    the double result of the convert
    """
    return struct.unpack('d', struct.pack('Q', int(str, 16)))[0]

def rect2bbox(rect):
    return [rect['l'], rect['b'], rect['r'], rect['t']]

def bbox2rect(bbox):
    """docstring for bbox2rect
    Summary:
        convert bbox string (in the xml file) to rect and calculate the area at the same time
    Parameter:
        [input]     bbox    -   the bbox string
        [return]    a dict with 'area' and 'rect' keys to indicate each
    """
    rect = {}
    rect['l'] = float(bbox[0])#hexlongbits2double(bbox[0])
    rect['t'] = float(bbox[1])#hexlongbits2double(bbox[1])
    rect['r'] = float(bbox[2])#hexlongbits2double(bbox[2])
    rect['b'] = float(bbox[3])#hexlongbits2double(bbox[3])
    area = abs((rect['r'] - rect['l']) * (rect['t'] - rect['b']))
    return {'area':area, 'rect':rect}


def get_me_str(f_node):
    """
    given a formula node,
    get the Char children,
    and get the text
    """

    s = ""
    for c in f_node.getElementsByTagName('Char'):
        s += c.getAttribute('Text')
    #print s
    return s


def get_info(p_xml):
    """docstring for get_info
    Summary:
        Get all needed info from xml file
    Parameter:
        [input]     p_xml       -   path of xml file
        [return]    formulas    -   needed infomation of all formulas
    """
    #print "load ground truth from ", p_xml
    formulas = []
    flag, xmldoc = parse_xml(p_xml)
    if flag:

        for i in xmldoc.getElementsByTagName('MO'):
            #print i
            formula = {}
            formula.update(bbox2rect(i.getAttribute('BBox').split())) # update rect and area info
            formula['type'] = 'E'  # add formula type info
            formula['str'] = get_me_str(i)
            if formula['area'] > 0:
                formulas.append(formula)
        '''
        # foreach all the Embedded Formulas
        for i in xmldoc.getElementsByTagName('EmbeddedFormula'):
            #print i
            formula = {}
            formula.update(bbox2rect(i.getAttribute('BBox').split())) # update rect and area info
            formula['type'] = 'E'  # add formula type info
            formula['str'] = get_me_str(i)
            if formula['area'] > 0:
                formulas.append(formula)

        # foreach all the Isolated Formulas
        for i in xmldoc.getElementsByTagName('IsolatedFormula'):
            #print i
            formula = {}
            formula.update(bbox2rect(i.getAttribute('BBox').split())) # update rect and area info
            # formula['type'] = 'I'  # add formula type info
            formula['type'] = 'E' # add formula type info
            formula['str'] = get_me_str(i)

            if formula['area'] > 0:
                formulas.append(formula)
        '''

    return flag, formulas

def tot_output():
    """docstring for tot_output
    Summary:
        Just for print the statistics
        No conection with any others
    """
    f = file(path_sum, 'a')
    print >>f, 'N_tot',
    for i in formula_type:
        for j in eval_type:
            print >>f, ',', sum_tot[i+j],
    print >>f, ',', sum_tot['tot']
    print >>f, 'S_tot',
    for i in formula_type:
        for j in eval_type:
            if j in ['cor','mis','fal']:
                print >>f, ', 1',
            elif sum_tot[i+j] > 0:
                print >>f, ',', sco_tot[i+j] / sum_tot[i+j],
            else:
                print >>f, ', 0',

            if j in ['cor']:
                sco_tot['tot'] += weight_type[j] * sum_tot[i+j]
            elif j in ['mis', 'fal']:
                sco_tot['tot'] -= weight_type[j] * sum_tot[i+j]
            elif j in ['par', 'exp', 'pae', 'mer', 'spl']:
                sco_tot['tot'] += weight_type[j] * sco_tot[i+j]

    weight_tot = 0
    for j in eval_type:
        if sum_tot['E'+j] + sum_tot['I'+j] > 0:
            weight_tot += weight_type[j]

    if sum_tot['tot'] > 0:
        print >>f, ',', sco_tot['tot'] / sum_tot['tot'] / weight_tot
    else:
        print >>f, ', 0'
    f.close()

def main():
    """docstring for main
    Summary:
        Traversal the xml files for evaluation
    """
    # print the first line of statistics file
    f = file(path_sum, 'w')
    for i in formula_type:
        for j in eval_type:
            print >>f, ', N_' + i + j,
    print >>f, ', Total'
    f.close()

    # Get all Ground Truth xmls
    gts = []
    try:
        gts = os.listdir(dir_gt)
    except:
        print '[Error]: The Ground Truth folder:', dir_gt, 'is not found'
        raw_input()
        return

    if not gts:
        print '[Warning]: No files found in the Ground Truth'
        raw_input()

    # Get all Machine Detection xmls
    mds = []
    try:
        mds = os.listdir(dir_md)
    except:
        print '[Error]: The Machine Detection folder:', dir_md, 'is not found'
        raw_input()
        return

    t = datetime.datetime.utcnow() # calculate time used for evaluation of all files

    # traversal the xml files
    for gt in gts:
        p_gt = os.path.join(dir_gt, gt)
        p_md = os.path.join(dir_md, gt)
        if not os.path.exists(p_md):
            print '[Error]:', p_md, 'not found!'
            raw_input()
        else:
            gt_flag, gt_formulas = get_info(p_gt)
            if not gt_flag:
                print '[Error]:', p_gt, 'is invalid!'
                raw_input()
                continue
            md_flag, md_formulas = get_info(p_md)
            if not md_flag:
                print '[Error]:', p_md, 'is invalid!'
                raw_input()
                continue
            t1 = datetime.datetime.utcnow() # calculate time used for evaluation of each file
            eval(gt_formulas, md_formulas, gt)
            print gts.index(gt), gt, datetime.datetime.utcnow() - t1

    print 'Total Time Used:', datetime.datetime.utcnow() - t
    raw_input() # to see the time statistics

    tot_output()


# Functions add by Xing
def double2hexlongbits(double):
    i = struct.unpack('Q', struct.pack('d', double))
    #print i, format(i, 'x')
    res = format(int(i[0]), 'x')
    return res

def do_stat():
    """
    true positive :
    false negative
    sensitivity : true positive rate , true positive / positive
    specificity : true negative rate, true negative / negative
    """
    t_FP, t_FN, t_TP = 0., 0., 0.
    for fname in os.listdir("Dataset/predict"):
        if not fname.endswith("xml"):
            continue
        prefix = fname[:fname.rindex('.xml')]
        res = eval_one(prefix)
        if res:
            FP = res['Ifal']
            FN = res['Imis']
            TP = sum([res['I'+j] for j in eval_type if j not in ['fal', 'mis']])
            print FP, FN, TP
            t_FN += FN
            t_FP += FP
            t_TP += TP
    print t_FP, t_FN, t_TP
    print 'recall', t_TP / (t_FN+ t_TP)
    print 'precision', t_TP/(t_FP+ t_TP)

