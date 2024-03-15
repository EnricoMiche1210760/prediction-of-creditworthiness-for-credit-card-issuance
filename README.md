# prediction-of-creditworthiness-for-credit-card-issuance

In this project we aim to predict the creditworthiness of clients who submited a credit card application to the Pro National Bank. The goal is to create a model capable of estimating the creditworthiness of a customer, in order to help the dedicated team understand whether or not to accept the application for a credit card and, possibly to provide an explanation for the decision.

The two datasets are composed by respectively 438557 and 13153 clients.
The application dataset contains the following features:
- `ID`: the unique identifier of the client;
- `CODE_GENDER`: the client gender;
- `FLAG_OWN_CAR`: whether the client owns a car or not;
- `FLAG_OWN_REALTY`: whether the client owns a realty or not;
- `CNT_CHILDREN`: the number of children the client has;
- `AMT_INCOME_TOTAL`: the total income of the client;
- `NAME_INCOME_TYPE`: the type of income of the client;
- `NAME_EDUCATION_TYPE`: the education level of the client;
- `NAME_FAMILY_STATUS`: the family status of the client;
- `NAME_HOUSING_TYPE`: the housing type of the client;
- `DAYS_BIRTH`: the age of the client in days, relative to the application date (negative value);
- `DAYS_EMPLOYED`: the number of days the client has been employed, relative to the application date (negative value if the client is employed);
- `FLAG_MOBIL`: whether the client provided a mobile phone number or not;
- `FLAG_WORK_PHONE`: whether the client provided a work phone number or not;
- `FLAG_PHONE`: whether the client provided a phone number or not;
- `FLAG_EMAIL`: whether the client provided an email or not;
- `OCCUPATION_TYPE`: the occupation of the client;
- `CNT_FAM_MEMBERS`: the number of family members of the client.<br><br>


The credit card dataset contains the following features:
- `ID`: the unique identifier of the client;
- `MONTHS_BALANCE`: the month of the record relative to the application date;
- `STATUS`: the status of the credit card of the client, where 0 means 1-29 days past due, 1 means 30-59 days past due, 2 means 60-89 days overdue, 
3 means 90-119 days overdue, 4 means 120-149 days overdue, 5 means over 150 days overdue, and C means paid off that month and X means no loan for the month.

The models trained in this project are:
- Logistic Regression;
- Random Forest;
- Gradient Boosting;
- Neural Network.