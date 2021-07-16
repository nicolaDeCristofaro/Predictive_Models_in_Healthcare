Natural language processing of MIMIC-III clinical
notes for identifying diagnosis and procedures with
neural networks ARTICLE.

Data primarily exists in two forms: structured and unstructured data with
diagnostics and laboratory results, medications present under structured data, whereas unstructured
data includes clinician progress notes and discharge summaries. The extraction of knowledge from
the structured data with the help of statistical tests and machine learning techniques is relatively easier
when compared with the unstructured text. Typically, several admission notes, clinical notes, transfer
notes and discharge summaries are associated with each patient’s history. Extracting knowledge
from this unstructured data has historically proven to be a difficult task as it requires a wide range
of manual feature engineering and mapping to ontologies [4], resulting in limited adoption of such
techniques.

Uses of NLP in healthcare

One of the recent advancements in Natural Language Processing (NLP) for healthcare is to use deep
learning to find associations between unstructured text with structured data in EHR [5]. This has
lead to a better understanding of the patient disease state and prognosis to improve patient outcomes
[6]. In a clinical setting, NLP can be used to convert data from provider notes such as clinical notes,
transfer notes, discharge notes into structured text in a predefined format which can be used for
analysis

Methodology
Overview We preprocessed and extracted the required data from the MIMIC-III dataset. Next, the
required features were extracted according to the requirements of the language model. Lastly, we
built the classifier models

Data preprocessing
We have selected the **noteevents** (containing the unstructured text) and **diagnosis_icd**
tables from the MIMIC-III database that are relevant to the research question, as shown in Figure 2.
We made use of columns such as subjectID, admissionID, discharge notes, ICD 9 codes. The selected
files contained clinical notes of patients, diagnosis and ICD codes with "HADM_ID"
column acting as a link for all the tables. After preprocessing the three datasets, it resulted in two
separate datasets.

The diagnosis table is merged with the note-events table containing 2.0M rows
which resulted in an unmanageable 800GB data which in turn was divided into multiple CSV files
with each file size ranging from 8 to 12GB. We chose a file with a 10GB size from this large number
of files and divided it into a train and test of 90:10. We trained the language model using this file and
it took 51 hours for 1 epoch on the GeForce GTX 1080. After we realized the potential problem with
the size of the data and with the constraints of time and resources, we stopped using the entire note
events, instead further filtering of the diagnosis and procedures tables was performed by us.