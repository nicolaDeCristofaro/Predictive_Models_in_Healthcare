## Length of Stay in Hospital (Hospital-LOS)
In order to predict hospital LOS, the MIMIC data needed to be separated into terms of a dependent target variable (length-of-stay in this case) and independent variables (features) to be used as inputs to the model. Since LOS is not a categorical but continuous variable (measured in days), a regression model will be used for prediction. It was likely (as turned out to be true) that the data needed significant cleanup and feature engineering to be in a format compatible with the learning model. For this project, I used the Pandas and scikit-learn libraries for Python.

**Metrics**
The expected outcome of this project is to develop a model that will be better at predicting hospital LOS than the industry standards of median and average LOS. The median LOS is simply the median LOS of past admissions to a hospital. Similarly, a second commonly used metric in healthcare is the average, or mean LOS. To measure performance, I’ll compare the prediction model against the median and average LOS using the root-mean-square error (RMSE). The RMSE is a commonly used measure of the differences between values predicted by a model and the values observed, where a lower score implies better accuracy. For example, a perfect prediction model would have an RMSE of 0. The RMSE equation for this work is given as follows, where (n) is the number of hospital admission records, (y-hat) the prediction LOS, and (y) is the actual LOS.

formula

The ultimate goal is to develop a prediction model that results in a lower RMSE than the average or median models.
There is a multitude of regression models available for predicting LOS. To determine the best regression model for this work (of the subset of models that will be evaluated), the R2 (R-squared) score will be used. The R2 is a measure of the goodness of the fit of a model. In other words, it is the proportion of the variance in the dependent variable that is predictable from the independent variables. R2 is defined as the following equation where (y_i) is an observed data point, (ŷ) is the mean of the observed data, and (f_i) the predicted model value.

formula

Best possible R2 score is 1.0 and a negative value means it is worse than a constant model, average or median in this case

**Data exploration and Feature Engineering**
After several iterations of reviewing the contents of the various tables in the MIMIC database, I ended up selecting the following tables and loading them into DataFrames using Pandas: ADMISSIONS.csv, PATIENTS.csv, DIAGNOSES_ICD.csv, and ICUSTAYS.csv.

The ADMISSIONS table gives information such as SUBJECT_ID (unique patient identifier), HADM_ID (hospital admission ID), ADMITTIME (admission date/time), DISCHTIME (discharge time), DEATHTIME, and more. The table had 58,976 admission events and 46,520 unique patients which seemed like a reasonable amount of data to do a prediction model study on.

To start with, I created a length-of-stay column by taking the difference between the admission and discharge time for each row. I opted to drop rows that had a negative LOS since those were cases where the patient died prior to admission.

Additionally, I found that 9.8% of the admission events resulted in death, so I removed these since they are not included as part of typical LOS metrics.

The distribution of the LOS in terms of days is right-skewed with a median of 10.13 days, a median of 6.56 days, and max of 295 days.

figure LOS INFOS

For the admission ethnicity column, there were 30+ categories that could be easily reduced to the five shown below. Interestingly, the Asian category has the lowest median LOS of the dataset.

figure Ethniciity

Hospital admissions were reduced down to four categories: urgent, newborn, emergency, elective. Newborns have the lowest median LOS whereas the urgent care category has the highest. Elective admissions have a tighter distribution that favors lower LOS, which makes sense since the severity of such conditions is usually less time-critical.

figure Admission type

There is an interesting insight for this dataset which shows that self-pay (often means no-pay) admissions have a much shorter LOS than the other insurance categories. Medicare and Medicaid take the top median LOS positions which could be related to the age of patients on those systems.

figure insurance

The PATIENTS table provided a de-identified date of birth and gender information. Because the MIMIC dataset does not provide a real date of birth to protect the identities of the patients, I needed to engineer the age feature using the following decoder: a patient’s age is given by the difference between their ‘DOB’ date of birth and the date of their first admission. This in mind, I merged the PATIENTS and ADMISSIONS DataFrames and used to pandas ‘groupby’ to extract the first admission time for each patient.

*df[[‘SUBJECT_ID’, ‘ADMITTIME’]].groupby(‘SUBJECT_ID’).min().reset_index()*

After taking the difference between the discharge time and first admission time, I was able to take a look at the age distribution of patients. It should be noted that patients >89 years old are put into the same age group in MIMIC.

figure age

Although newborn patient data is included in the MIMIC dataset, pediatric ages are not. To add a dimension to the age distribution plot, I looked that the LOS versus age. The plot highlights the MIMIC groups of newborns and >89 year olds, where there is an increasing amount of admissions going from 20 toward 80 years old. Because of the discrete-like distribution of data on the extremes of age, I decided to convert all ages into the categories of newborn, young adult, middle age, and senior for use in the prediction model.

figure age into categories

The DIAGNOSES_ICD table provided the largest challenge in terms of feature engineering. The table consists of the patient and admission IDs, and an ICD9-Code which is described as follows (source):

*International Classification of Diseases, Clinical Modification (ICD-9-CM) is an adaption created by the U.S. National Center for Health Statistics (NCHS) and used in assigning diagnostic and procedure codes associated with inpatient, outpatient, and physician office utilization in the United States.*

There were 6,984 unique codes used in the MIMIC dataset and 651,047 ICD-9 diagnoses given to patients since most were diagnosed with more than one condition. Looking at the table, you can see that the ICD9_CODE column code takes a variable character length approach.

figure diagnoses info table

After some investigation, I found that the true code syntax is three digits followed by a set of decimals for subcategories. For example, the code from the first row is 403.01 which falls in the range of diseases of the circulatory system and the .01 value further specifies hypertensive chronic kidney and related diseases. Additionally, I noticed that ICD-9 has 17 primary categories so I decided to sort all the unique codes per admission into these categories. My reasoning was that reducing the ICD-9 codes from 6,984 to 17 would make for a much more understandable ML model. Also, I didn’t want any ICD-9 codes to just have a single LOS target row since that would complicate training/testing. Finally, I transformed the sort ICD-9 codes into an admission-ICD9 matrix, grouped the diagnosis per admission, and merged the new columns back with the primary admissions DataFrame on the HADM_ID (admission ID). You can see that each row (admission) contains multiple diagnoses as they should.

figure admissions diagnosi matrix

Looking at the median LOS for each ICD-9 supercategory shows an impressive spread between pregnancy and skin diagnosis code groups. As will be shown later, the diagnosis categories are the most important features in predicting LOS.

figure comparison of diagnosis

**Data Preprocessing**

Even after completing the feature engineering for age and ICD-9, there were some loose ends that needed tidying up before the data could be used for the prediction model. First, I ensured that no admissions resulting in death were part the cleaned dataset. I dropped all unused columns and verified that no NaNs existed in the data.

For the admission type, insurance type, religion, ethnicity, age, and marital status columns, I performed the Pandas get_dummies command to convert these categorical variables into dummy/indicator variables. (???) -> OneHotEncoding alternative (???)

The final DataFrame size resulted in 48 feature columns and 1 target column with an entry count of 53,104.

**Prediction Model**

To implement the prediction model, I split the LOS target variable and features into training and test sets at an 80:20 ratio using the scikit-learn train_test_split function.

*X_train, X_test, y_train, y_test = train_test_split(features,LOS, test_size = .20)*

Using the training set, I fit five different regression models (from the scikit-learn library) using default settings and then compared the R2 scores on the testing set. The GradientBoostingRegressor took the win with an R2 score of ~37% with the testing set so I decided to focus on refining this particular model. Because of past success with the RandomForestRegressor, I played with that model’s parameters but was never able to exceed the GradientBoostingRegressor score. **(DO SOME RESEARCH WITH THESE MODELS)**

figure Comparison of regression Models

To refine the GradientBoostingRegressor model, I used the GridSearchCV function from scikit-learn to test out various permutations of parameters such as n_estimators, max_depth, and loss. The best estimator result from GridSearchCV was n_estimators=200, max_depth=4, and loss=ls. This resulted in a minor improvement with an R2 score of ~39% with the testing set.

**Results**

Before looking at the RMSE benchmark, I wanted to investigate what features were most important in predicting hospital length-of-stay when using the gradient boosting regression model. Diagnoses related to prenatal issues have the highest feature importance coefficient followed by respiratory and injury. As I alluded to earlier, the ICD-9 diagnoses categories are by far the most important features. In fact, in the top 20 top features, only emergency admission type, gender, and Medicaid insurance showed any importance outside of diagnosis groups.

figure top10 features for predicting LOS

In the metrics section, I stated that the RMSE would be used to compare the prediction model versus the industry-standard average and median LOS metrics. The gradient boosting model RMSE is better by more than 24% (percent difference) versus the constant average or median models.

figure RMSE comparison Models

While the RMSE trend is promising, I also wanted to evaluate the model from a few other perspectives. The following figure takes the first 20 admissions from the test set and directly compares the actual, predicted (gradient boosting model), average, and median LOS values. This gives a more convoluted picture of the prediction model; in some admissions, it predicts well but not as well in others. However, based on the RMSE score, the prediction model will still be generally more accurate than using the median or average LOS.

figure prediction LOS

The final way I wanted to look at the model was to plot the proportion of accurate predictions in the test set versus an allowed margin of error. Other studies qualify a LOS prediction as correct if it falls within a certain margin of error. It follows that as the margin of error allowance increases, so should the proportion of accurate predictions for all models. The gradient boosting prediction model performs better than the other constant models across the margin of error range up to 50%.

figure errorMargin

**Conclusions**
The MIMIC database offered surprisingly good depth and detail related to medical admissions which enabled me to create a hospital length-of-stay prediction model that considered a lot of interesting input features. The most surprising aspect of this work was how the patient ICD-9 diagnoses played a more important role than age when predicting the length-of-stay. By far, the most challenging aspect of this project was the feature engineering of the ICD-9 diagnoses into a more practical and interpretable form of supercategories. However, therein also lies the most obvious area for future improvement. Given that the diagnoses have such strong feature importance, it would be worth evaluating whether additional subdividing of the primary ICD-9 categories would yield a better prediction model. My theory is that the prediction model would become more accurate (lower RMSE) with this optimization, so long as there were enough admission records in the dataset to support reasonable diagnoses model training.
