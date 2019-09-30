# Evalatuion_tool_MOP_v1

/* Copyright (c) 2017-2019, Texas Engineering Experiment Station (TEES), a

component of the Texas A&M University System.
All rights reserved.
The information and source code contained herein is the exclusive
property of TEES and may not be disclosed, examined or reproduced
in whole or in part without explicit written authorization from TEES. */
This is a customized evaluation tool for the dataset presented in the paper: "Labeling of Math Objects in PDF Documents Based on the LaTeX Source Files: Basic Methods and Initial Results".

Acknowledgment to the authors in "Performance evaluation of mathematical formula identification", who developed the original version of the evaluation tool for the Marmot dataset. Unlike Marmot tool, our dataset does not differentiate between Isolated mathematical objects (display) or Embedded mathematical objects (in-line). The reported results are adjusted accordingly.

To run the evaluation tool, see the file 'evaluate.py'. The 'data' folder gives an example of how the data should be organized. In 'data/pdf', individual pdf pages are saved. In 'data/ground_truth', ground truth files in json format are saved. In 'data/prediction', predictions files in xml format are saved.

This tool will report the following metrics: correct, miss, false, partial, expanded, partial and expanded, merged, split
