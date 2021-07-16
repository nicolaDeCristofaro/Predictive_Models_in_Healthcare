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

The dataset used in this project is MIMIC-3 (Medical Information Mart for Intensive Care 3) openly accessible, created by the Laboratory of Computational Physicology of The Massachusetts Institute for Technology (MIT) with the goal of providing tools for the creation of clinical knowledge through the application of data analysis techniques.

MIMIC-III is a large, freely-available relational database comprising deidentified health related data associated with over forty thousand patients who stayed in Intensive Care Units at Beth Israel Deaconess Medical Center (Boston, Massachusetts). The data spans June 2001 - October 2012.

MIMIC-III is structured in a relational manner and contains 26 linked tables through patient identifier:
- Each table contains each patient record (at each row) with specific field (columns).
- Tables start with ‘D_’ are dictionaries and provide definitions for identifiers.

figure of all tables from slidesd source

**General Information on tables**
- Each patient is unique with its own **"subject_id"**
- Each hospital admission of a patient is unique with **"hadm_id"**
- Each ICU (Intensive Care Unit) stay of a patient is unique with **"icustay_id"**
  
This means that:
- One **subject_id** can be associated with multiple **hadm_ids** when a patient had multiple admissions.
- One **hadm_id** can be linked to multiple **icustay_id** when a patient had a multiple ICU stays during an admission. (e.g., transferring between multiple ICUs)

Below we analyze some of the tables used in this project:

### Patient TABLE (It defines a single patient)
**Number of rows**: 46 520

**Table Columns**:
- SUBJECT_ID is a unique identifier which specifies an individual patient
- GENDER is the genotypical sex of the patient
- DOB is the date of birth of the given patient. (DOB has been shifted for patients older than 89 to obscure their age and comply with HIPAA. The median age for the patients whose date of birth was shifted is 91.4).
- DOD is the date of death for the given patient
- DOD_HOSP is the date of death as recorded in the hospital database
- DOD_SSN is the date of death from the social security database (Note that DOD merged together DOD_HOSP and DOD_SSN, giving priority to DOD_HOSP if both were recorded)
- EXPIRE_FLAG is a binary flag which indicates whether the patient died, i.e. whether DOD is null or not. These deaths include both deaths within the hospital (DOD_HOSP) and deaths identified by matching the patient to the social security master death index (DOD_SSN).

**Age of certain patient of a point of time in the record can be calculated by subtracting a certain record time – DOB.**

Patients table is linked:

- ADMISSIONS on SUBJECT_ID
- ICUSTAYS on SUBJECT_ID

so below we descrive attributes of these tables.

### Admissions TABLE (It defines a patient’s hospital admission)
**Number of rows**: 58 976

**Table Columns**:
- SUBJECT_ID, HADM_ID: each row of this table contains a unique HADM_ID, which represents a single patient’s admission to the hospital. HADM_ID ranges from 1000000 - 1999999. It is possible for this table to have duplicate SUBJECT_ID, indicating that a single patient had multiple admissions to the hospital.
- ADMITTIME provides the date and time the patient was admitted to the hospital
- DISCHTIME provides the date and time the patient was discharged from the hospital. 
- If applicable, DEATHTIME provides the time of in-hospital death for the patient. (Note that DEATHTIME is only present if the patient died in-hospital, and is almost always the same as the patient’s DISCHTIME. However, there can be some discrepancies due to typographical errors).
- ADMISSION_TYPE describes the type of the admission: ‘ELECTIVE’, ‘URGENT’, ‘NEWBORN’ or ‘EMERGENCY’. Emergency/urgent indicate unplanned medical care, and are often collapsed into a single category in studies. Elective indicates a previously planned hospital admission. Newborn indicates that the HADM_ID pertains to the patient’s birth.
- ADMISSION_LOCATION provides information about the previous location of the patient prior to arriving at the hospital.
- The INSURANCE, LANGUAGE, RELIGION, MARITAL_STATUS, ETHNICITY columns describe patient demographics. These columns occur in the ADMISSIONS table as they are originally sourced from the admission, discharge, and transfers (ADT) data from the hospital database. The values occasionally change between hospital admissions (HADM_ID) for a single patient (SUBJECT_ID). This is reasonable for some fields (e.g. MARITAL_STATUS, RELIGION), but less reasonable for others (e.g. ETHNICITY)
- EDREGTIME, EDOUTTIME: Time that the patient was registered and discharged from the emergency department.
- The DIAGNOSIS column provides a preliminary, free text diagnosis for the patient on hospital admission. The diagnoses can be very informative (e.g. chronic kidney failure) or quite vague (e.g. weakness). Final diagnoses for a patient’s hospital stay are coded on discharge and can be found in the DIAGNOSES_ICD table. While this field can provide information about the status of a patient on hospital admission, so it is not recommended using it to stratify patients.
- HOSPITAL_EXPIRE_FLAG: this indicates whether the patient died within the given hospitalization. 1 indicates death in the hospital, and 0 indicates survival to hospital discharge.

- **Organ donor accounts are sometimes created for patients who died in the hospital. These are distinct hospital admissions with very short, sometimes negative lengths of stay. Furthermore, their DEATHTIME is frequently the same as the earlier patient admission’s DEATHTIME.**
- **All text data, except for that in the INSURANCE column, is stored in upper case.**

For the complete descriptions of the table's structure here is the associated documentation -> https://mimic.mit.edu/docs/iii/tables/

Now, for each prediction we want to get, we go through the following steps:

- Problem Statement
- Type of model to use for prediction
- Metrics used for validation
- Data extraction, exploration and feature engineering
- Data cleaning
- Features Selection
- Split in training/test set
- Prediction Model choice
- Prediction Model validation
- Parameter Tuning
- Results discussion

## Hospital LOS (Length-of-Stay)
First of all what is LOS? **Hospital length-of-stay (LOS)** is defined as the time between hospital admission and discharge measured in days.

**1.Problem Statement**: The goal is to create a model that predicts the length-of-stay for each patient at time of admission.

In order to predict hospital LOS, the MIMIC data needed to be separated into terms of:
- dependent target variable (length-of-stay in this case) 
- and independent variables (features) to be used as inputs to the model. 

**2.Type of model used for prediction**
Since LOS is not a categorical but continuous variable (measured in days), a **regression model** will be used for prediction. 

**3.Metrics used for validation**
The expected outcome is that the model we use will be better at predicting hospital LOS than the industry standards of **median and average LOS**. The median LOS is simply the median LOS of past admissions to a hospital. Similarly, a second commonly used metric in healthcare is the average, or mean LOS. 

So, to measure performance of our model, we'll compare the prediction model against the median and average LOS using the root-mean-square error (RMSE). The RMSE is a commonly used measure of the differences between values predicted by a model and the values observed, where a *lower score implies better accuracy*. For example, a perfect prediction model would have an RMSE of 0. 

The RMSE equation for this work is given as follows, where (n) is the number of hospital admission records, (y-hat) the prediction LOS, and (y) is the actual LOS.




 I used the Pandas and scikit-learn libraries for Python.



## Data extraction, exploration and feature engineering
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

### LOS
U.S. hospital stays cost the health system at least $377.5 billion per year and recent Medicare legislation standardizes payments for procedures performed, regardless of the number of days a patient spends in the hospital. This incentivizes hospitals to identify patients of high LOS risk at the time of admission. Once identified, patients with high LOS risk can have their treatment plan optimized to minimize LOS and lower the chance of getting a hospital-acquired condition such as staph infection. Another benefit is that prior knowledge of LOS can aid in logistics such as room and bed allocation planning.

