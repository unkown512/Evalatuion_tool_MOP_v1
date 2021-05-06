# Evalatuion_tool_MOP_v1

This is a customized evaluation tool for the dataset presented in the paper: ["Semi-Automatic LaTeX-Based Labeling of Mathematical Objects in PDF Documents: MOP Data Set"](http://delivery.acm.org/10.1145/3350000/3345426/a35-Beyette.pdf?ip=128.194.140.216&id=3345426&acc=OPEN&key=B63ACEF81C6334F5%2E79B51EFA2DE92FE8%2E4D4702B0C3E38B35%2E6D218144511F3437&__acm__=1569945207_420f51e88cd9ce39a6b459f662efb32e). ACM DocEng 2019

Acknowledgment to the authors in ["Performance evaluation of mathematical formula identification"](https://www.researchgate.net/publication/239762668_Performance_Evaluation_of_Mathematical_Formula_Identification), who developed the original version of the evaluation tool for the Marmot dataset. Unlike Marmot tool, our dataset does not differentiate between Isolated mathematical objects (display) or Embedded mathematical objects (in-line). The reported results are adjusted accordingly.

# NOTE
 We are currently developing a new tool that will also test the performance of LaTeX generation and subject prediction.
### FOR PDF OFFSETS
Depending on what tool you use, you may have to subtract some offset from the cordinates. 
# HOW TO USE

1. Download the project with `git clone https://github.com/unkown512/Evalatuion_tool_MOP_v1.git`
2. From the root directory run `cd Evaluation_Tool`
3. To insure the project builds correctly, run `python evaluate.py` This should output the below information:
  
  
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

1. Correct
2. Miss
3. False
4. Partial
5. Expanded
6. Partial and Expanded
7. Merged
8. Split

### How to evaluate your performance?
 Create a XML file whose name schema consists of `<ID>_page_<#>.xml`, whose `ID` and `#` correspond to the PDF_File and Ground_Truth file name schema. See [MOP](https://www.kaggle.com/moptamu/moptamu) for more information.
  
For each extracted MO (mathematical object), insert a new element row as follows:

![alt text](https://github.com/unkown512/Evalatuion_tool_MOP_v1/blob/master/MOP_prediction_example.PNG)
 
  
  Note that for each <MO></MO> row, it is optional to add additional rows such as `<char BBox>`. However, these are currently ignored during evaluation.
  
Follow the examples in the data/prediction directory. NOTE: You can add additional information such as the BBox for each character, size, and value without affecting the result.
  
BBox values X1, Y1, X2, Y2 represent the full tight bounding box of the predicted MO in the PDF document:
  

- X1 = Left most x-coordinate
- Y1 = Lowest y-coordinate
- X2 = Right most x-coordinate
- Y2 = Highest y-coordinate

  For each file in the `data/pdf` directory ensure a file exists in both the `data/ground_truth` and `data/prediction` directories. There must be an equal number of files and each file should have a unique `<ID>` inside its own directory that corresponds to the other directories.

