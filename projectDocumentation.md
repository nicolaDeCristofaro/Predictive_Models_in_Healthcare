# Course Project: Predictive Models derived from Electronic Health record EHR

## Introduction & Objectives

The healthcare sector is one of the fundamental sectors of our society, and unfortunately it is often one of the most overloaded and full of problems. Especially in times like the one we are experiencing, the responsibility for this sector increases considerably and all the weak points are beginning to be noticed.

For this reason, one of the points from which we must start again to defeat the pandemic in progress is the strengthening of hospitals and all the systems that manage them.

One way that certainly manages to bring tangible benefits to the hospital sector is the use of Machine Learning. Machine Learning could be used to predict illness and treatment to help physicians and payers intervene earlier, predict population health risk by identifying patterns and surfacing high risk markers and model disease progression. Machine learning could also help pathologists make quicker and more accurate diagnoses as well as identify patients that might benefit from new types of treatments or therapies. These are just a few examples of the large set of benefits that Machine Learning can give to this sector.

In this project, making use of the EHR (Electronic Health Record) which is a systematic collection of information on the health of individuals in digital format, we focus on defining predictive models that allow us to predict:

- **In-hospital mortality**: death occurred during the hospital stay
- **Readmission within 30 days**: readmission to hospital within 30 days of last admission
- **Readmission within 90 days**: readmission to hospital within 90 days of last admission
- **Readmission within 365 days**: readmission to hospital within 365 days of last admission
- **Final discharge diagnosis of the patient**: final diagnosis outcome
- **Hospitalization time**: length of stay in hospital

## Dataset

- General description of MIMIC III

## Data extraction and exploration

- Merge all tables linked between them
- Explore data of tables obtained (info, describe, histograms) (if data is too large create a copy of the data for exploration so sample it down to a manageable size if necessary)
- Using a jupyter notebook to keep record of data exploration
- Study attributes and associated characteristics (name, type, % of missing values, useful for the task? and so on...)

## Supervised Learning

- What is Supervised Learning and why we choose it
- How should performances be measured?
- For each objective identify target attribute(s) and how you obtained it(them)
  - In-hospital mortality you could use, in addition to features saw in tutorials, also the lactate indices referring the paper 

## Study correlation between attributes

## Data Preparation

- Write functions for data transformations if necessary (why function?) (work on copies of the data to keep original dataset intact)
- Data cleaning: 
  - fix or remove outliers
  - fill in missing values (for example with zero, mean, median) or drop their rows (or columns)
- Feature Selection: drop the attributes that provide no useful information for the task
- Optional Features engineering to transform or decompose features when necessary
- Optional Features scaling

## Predictive Models selection, evaluation and comparison

## Parameters tuning

## Predictions and Results analysis

## Results discussion

- results discussion with graph representation

## Conclusions and Future Development

