# Predict Customer Personality to Boost Marketing Campaign

<div align="center">
<img src="https://img.freepik.com/free-vector/human-resourses-managers-doing-professional-staff-research-with-magnifier-human-resources-hr-team-work-headhunter-service-concept_335657-332.jpg?w=996&t=st=1703489108~exp=1703489708~hmac=b183c6a0282e1040b081bebe2af82f14d969249261220d311f5fc63f21b25e62" alt="customerpersonality" style="width:600px;height:400px;" align="center">
</div> 

<br>
A company can develop rapidly when it knows the personality behavior of its customers so that it can provide better services and benefits to customers who have the potential to become loyal customers. By processing historical marketing campaign data to improve performance and target the right customers so they can make transactions on the company's platform, from these data insights our focus is to create a cluster prediction model to make it easier for companies to make decisions.
<br> 

## Points to Analyze

- Conversion Rate Analysis Based On Income, Spending And Age
- Data Modeling
- Customer Personality Analysis for Marketing Retargeting
<br>

# Data Overview  

| Feature Name | Description |
| --- | --- |
***CUSTOMER ATTRIBUTES***
|**Unnamed : 0** | Index number |
|**ID** | Customer's unique identifier |
|**Year_Birth** | Customer's birth year|  
|**Education** |Customer's education level |
|**Marital_Status** | Customer's marital status|
|**Income** | Customer's yearly household income |
|**Kidhome**| Number of children in customer's household |
|**Teenhome** | Number of teenagers in customer's household  |
|**Dt_Customer** |Date of customer's enrollment with the company  |
|**Recency** | Number of days since customer's last purchase |
|**Complain** | 1 if the customer complained in the last 2 years, 0 otherwise |  
***PRODUCTS ATTRIBUTES***
|**MntCoke** | Amount spent on coke in last 2 years |
|**MntFruits** | Amount spent on fruits in last 2 years |
|**MntMeatProducts** | Amount spent on meat in last 2 years |  
|**MntFishProducts** | Amount spent on fish in last 2 years |
|**MntSweetProducts** | Amount spent on sweets in last 2 years|
|**MntGoldProds** | Amount spent on gold in last 2 years |
***PROMOTION ATTRIBUTES***
|**NumDealsPurchases** |Number of purchases made with a discount|
|**AcceptedCmp1** |1 if customer accepted the offer in the 1st campaign, 0 otherwise|
|**AcceptedCmp2** |1 if customer accepted the offer in the 2nd campaign, 0 otherwise|
|**AcceptedCmp3** |1 if customer accepted the offer in the 3rd campaign, 0 otherwise|
|**AcceptedCmp4** |1 if customer accepted the offer in the 4th campaign, 0 otherwise|
|**AcceptedCmp5** |1 if customer accepted the offer in the 5th campaign, 0 otherwise|
|**Response** |1 if the customer accepted the offer in the last campaign, 0 otherwise|
***PLACE ATTRIBUTES***
|**NumWebPurchases** |Number of purchases made through the company’s website|  
|**NumCatalogPurchases** |Number of purchases made using a catalog |
|**NumStorePurchases** |Number of purchases made directly in stores|  
|**NumWebVisitsMonth** |Number of visits to the company’s website in the last month|
|**Z_CostContact** | Cost to contact a customer |
|**Z_Revenue** |Revenue after client accepting campaign|
<br>

# Data Overview   
<br>
<img width="280" height="600" alt="image" src="https://github.com/Yunanouv/Predict-Customer-Personality/assets/146415555/25c0cdc0-23d1-4c68-bf14-a31c314cbdb6">

<br> 

- There are 2240 lines with 30 features  
- There is only 1 column with a null value, namely the Income column (24 null values)  
- The data type for the Dt_Customers column needs to be changed to DateTime  
- No duplicate data  
- There is a lot of numerical data but not many outliers  
- Perform feature extraction in the form of age features, number of children, number of transactions, number of expenses, conversion rate, etc. to become 36 features
<br>

# Exploratory Data Analysis   
<br>

**1. Data Distribution**  
<br>
<img width="850" height="400" alt="image" src="https://github.com/Yunanouv/Predict-Customer-Personality/assets/146415555/f0d5380e-f236-4e3f-b794-cf4287ce67bc">
<br>
From the data distribution, it can be seen that many features are close to a normal distribution, despite `Children` and `TotalAccCmp` having a small real value. Meanwhile, other features have right-skewed. 
<br>


**2. Outliers Checking**  
<br>
<img width="680" height="350" alt="image" src="https://github.com/Yunanouv/Predict-Customer-Personality/assets/146415555/838ee8ae-94ac-41d1-8af7-e659553c58e2">
<br>
Feature `Age`, `Income`, `TotalSpending`, `TotalTrx`, and `CVR` have outliers. If we look at the outlier for `Age`, it can be seen that the data does not make sense because it is more than 80 years old, so it is best to delete this row so that the clustering process avoids outliers. Likewise, the outliers in the Income column are worth more than 600,000,000. TotalSpending, TotalTrx, and CVR also show outliers so they need further handling.   
<br>

**3. Regression Plot of Features and Conversion Rate**  
<br>
<img width="1300"  height = "240" alt="image" src="https://github.com/Yunanouv/Predict-Customer-Personality/assets/146415555/9a8b46f2-d69c-4c70-9a23-8f9c4c4b2893">
<br>

**4. Categorical Features**  
The categorical features look neat and clean, but for `Marital Status` it can be simplified into some values. 

# Business Insight 
<br>
Conversion rate analysis is a search for insight into data on the percentage of website visitors what actions they take while visiting the site, and whether their actions result in a purchase transaction or not while visiting the website. This can be done by performing feature engineering on the data variables presented so that it can produce a new column, that is the Conversion Rate.  
<br>

### 1. Conversion Rate Based on Age
<br>
<img width="550" height="400" alt="image" src="https://github.com/Yunanouv/Predict-Customer-Personality/assets/146415555/7aa816ac-6b10-484b-ac15-28a8c004359f">
<br>
Based on the cleaned data, the youngest age is 27 and the eldest is 80. Late twenties to thirties are our potential customers as we can see on the graph shows the highest conversion rate. The least potential is from groups 41-50 which is the middle group. The graph moves lower from the highest to the lowest group and the conversion rate then starts to grow as they get older (>51 years old). 

### 2. Conversion Rate Based on Income 
<br>
<img width="565" alt="image" src="https://github.com/Yunanouv/Predict-Customer-Personality/assets/146415555/dcf802e2-052d-496c-abd7-c8560ef19d49">
<br> 
The conversion rate tends to increase along with higher income groups. The highest conversion rate comes from the 90-100M income group. It indicates that income has a linear correlation with the conversion rate.  
<br>

### 3. Conversion Rate Based on Total Transactions 
<br>
<img width="445" alt="image" src="https://github.com/Yunanouv/Predict-Customer-Personality/assets/146415555/d6615a40-9fa6-4a8e-a150-25fcf694c087">
<br>

