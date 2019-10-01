# Evalatuion_tool_MOP_v1

This is a customized evaluation tool for the dataset presented in the paper: "Labeling of Math Objects in PDF Documents Based on the LaTeX Source Files: Basic Methods and Initial Results".

Acknowledgment to the authors in "Performance evaluation of mathematical formula identification", who developed the original version of the evaluation tool for the Marmot dataset. Unlike Marmot tool, our dataset does not differentiate between Isolated mathematical objects (display) or Embedded mathematical objects (in-line). The reported results are adjusted accordingly.

To run the evaluation tool, see the file 'evaluate.py'. The 'data' folder gives an example of how the data should be organized. In 'data/pdf', individual pdf pages are saved. In 'data/ground_truth', ground truth files in json format are saved. In 'data/prediction', predictions files in xml format are saved.

This tool will report the following metrics: correct, miss, false, partial, expanded, partial and expanded, merged, split


# TESTING ---
Currently, the evaluation tool is a customized version of the tool presented in the paper: "Performance Evaluation of Mathematical Formula Identification" by Xiaoyan Lin, Liangcai Gao, Zhi Tang, Xiaofan Lin, and Xuan Hu. We are currently developing a new tool that will also test the performance of LaTeX generation and subject prediction.
  

To run the the tool, enter the command `python evaluate.py` This should output the below information:

`cor 0
mis 0
fal 1
par 0
exp 1
pae 0
mer 0
spl 0
cor 0
mis 0
fal 0
par 0
exp 1
pae 0
mer 0
spl 0
cor 1
mis 0
fal 0
par 0
exp 0
pae 0
mer 0
spl 0
cor 0
mis 1
fal 0
par 0
exp 0
pae 0
mer 0
spl 0
cor 1
mis 2
fal 8
par 0
exp 1
pae 1
mer 0
spl 0
MO False rate 0.6
MO Mis rate 0.333333333333
`
  

In total, the tool outputs 9 metrics:

- 1) Correct
- 2) Miss
- 3) False
- 4) Partial
- 5) Expanded
- 6) Partial and Expanded
- 7) Merged
- 8) Split

### How to evaluate your performance?
 Create a XML file whose name schema consists of `<ID>_page_<#>.xml`, whose `ID` and `#` correspond to the PDF_File and Ground_Truth file name schema.
  
For each extracted MO (mathematical object), insert a new element row as follows:

`<MO BBox="X1 Y1 X2 Y2"></MO>`
  
Follow the examples in the data/prediction directory. NOTE: You can add additional information such as the BBox for each character, size, and value without affecting the result.
  
BBox values X1, Y1, X2, Y2 represent the full tight bounding box of the predicted MO in the PDF document:
  

- X1 = Left most x-coordinate
- Y1 = Lowest y-coordinate
- X2 = Right most x-coordinate
- Y2 = Highest y-coordinate

  For each file in the `data/pdf` directory ensure a file exists in both the `data/ground_truth` and `data/prediction` directories. There must be an equal number of files and each file should have a unique `<ID>` inside its own directory that corresponds to the other directories.

