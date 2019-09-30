"""
Evaluation Tool for the dataset
"""

import glob
import json
import numpy as np

from file_util import get_file_name_prefix
import MathEval as me
from MathEval import get_info, formula_type, eval_type

PDF_PATH = 'data/pdf/'
PRED_PATH = 'data/prediction/'
GT_PATH = "data/ground_truth/"


def get_ground_truth(pdf):
    pdf_id = pdf.split("_")
    pdf_id = pdf_id[0]
    pdf_page = pdf.split("page_")
    pdf_page = pdf_page[1]

    # generate ground truth filename
    groundtruth_file = "page_" + pdf_page + "_" + pdf_id + "_ground_truth.json"
    list_of_mo = []

    with open(GT_PATH + groundtruth_file) as infile:
        data = json.load(infile)
        for ME in data["FULL_BBOX"]:
            tmp = {}
            tmp["type"] = "E"
            if (float(ME[2]) < float(ME[0])):
                print "FLAG"
            tmp["rect"] = {"r": ME[0], "b": ME[1], "l": ME[2], "t": ME[3]}
            if (tmp["rect"]["r"] < tmp["rect"]["l"]):
                tmp["rect"]["r"] = ME[2]
                tmp["rect"]["l"] = ME[0]
            height = abs(tmp["rect"]["t"] - tmp["rect"]["b"])
            width = abs(tmp["rect"]["r"] - tmp["rect"]["l"])
            tmp['area'] = height * width
            list_of_mo.append(tmp)
    return list_of_mo


def eval_one(gd_path, pred_path):
    """
    sum is a list of measurement

    :param gd_path:
    :param pred_path:
    :return:
    """
    gt_formulas = get_ground_truth(gd_path)

    md_flag, md_formulas = get_info(pred_path)
    if not md_flag:
        return None

    sum = me.eval(gt_formulas, md_formulas)

    for i in formula_type:
        for j in eval_type:
            print j, sum[i + j]

    return sum

def evaluate():
    """

    :return:
    """

    pdf_path_rate_list = []
    total_res_dict = {}
    res_dict_list = []
    for pdf_path in glob.glob("{}*.pdf".format(PDF_PATH)):

        pdf_path = pdf_path.replace("\\", "/")
        file_name_prefix = get_file_name_prefix(pdf_path)

        pd_path = PRED_PATH + file_name_prefix + '.xml'

        gd_path = file_name_prefix

        res_dict = eval_one(gd_path, pd_path)
        md_flag, md_formulas = get_info(pd_path)
        if res_dict != None:
            for k, v in res_dict.items():
                if k.startswith('I') or k.startswith('E'):
                    if k not in total_res_dict:
                        total_res_dict[k] = 0
                    total_res_dict[k] += v

        if len(md_formulas) == 0:
            continue
        res_dict['file_name'] = file_name_prefix
        res_dict_list.append(res_dict)
        rank_criteria = - res_dict['E'+'mis']
        pdf_path_rate_list.append((pdf_path, rank_criteria))

    total_e_count1 = np.sum([total_res_dict['E'+et] for et in eval_type])
    false_rate = float(total_res_dict['Efal']) / (total_e_count1 - total_res_dict['Emis'])
    mis_rate = float(total_res_dict['Emis']) / (total_e_count1 - total_res_dict['Efal'])
    print("MO False rate {}".format(false_rate))
    print("MO Mis rate {}".format(mis_rate))

    return total_res_dict


if __name__ == "__main__":
    evaluate()
