> # 1. Load the data table exported from your Python data pipeline
> welfare_data <- read.csv("real_interstate_welfare_data.csv")
>
> # 2. Inspect the structure to confirm all 112 counties loaded smoothly
> head(welfare_data)
                            NAME median_gross_rent median_income labor_force unemployed_count snap_households total_households state county snap_participation_rate
1     Adams County, Pennsylvania              1060         78975       53817             1832            2849            40006    42      1                7.121432
2 Allegheny County, Pennsylvania              1050         72537      673356            33317           67094           545637    42      3               12.296454
3 Armstrong County, Pennsylvania               777         61011       31799             1614            4081            27767    42      5               14.697303
4    Beaver County, Pennsylvania               830         67194       85062             4760            9905            71999    42      7               13.757136
5   Bedford County, Pennsylvania               727         58337       23210              990            2568            19571    42      9               13.121455
6     Berks County, Pennsylvania              1078         74617      223434            12012           22293           161174    42     11               13.831635
  unemployment_rate minimum_wage wage_to_rent_ratio
1          3.404129         7.25        0.006839623
2          4.947903         7.25        0.006904762
3          5.075631         7.25        0.009330759
4          5.595918         7.25        0.008734940
5          4.265403         7.25        0.009972490
6          5.376084         7.25        0.006725417
> summary(welfare_data)
        NAME     median_gross_rent median_income     labor_force     unemployed_count snap_households  total_households     state           county
 Length   :112   Min.   : 657.0    Min.   : 46186   Min.   :  1703   Min.   :   73    Min.   :   188   Min.   :  1844   Min.   :24.00   Min.   :  1.00
 N.unique :112   1st Qu.: 797.5    1st Qu.: 59442   1st Qu.: 22985   1st Qu.: 1040    1st Qu.:  2449   1st Qu.: 19166   1st Qu.:34.00   1st Qu.: 19.00
 N.blank  :  0   Median :1055.0    Median : 71722   Median : 60180   Median : 2984    Median :  5952   Median : 50132   Median :42.00   Median : 38.00
 Min.nchar: 21   Mean   :1124.4    Mean   : 77738   Mean   :133110   Mean   : 7460    Mean   : 11161   Mean   : 97768   Mean   :36.64   Mean   : 53.65
 Max.nchar: 35   3rd Qu.:1411.8    3rd Qu.: 86858   3rd Qu.:184502   3rd Qu.: 9696    3rd Qu.: 12649   3rd Qu.:134343   3rd Qu.:42.00   3rd Qu.: 79.50
                 Max.   :1957.0    Max.   :140971   Max.   :806458   Max.   :69721    Max.   :172146   Max.   :659129   Max.   :42.00   Max.   :510.00
 snap_participation_rate unemployment_rate  minimum_wage    wage_to_rent_ratio
 Min.   : 2.738          Min.   :2.185     Min.   : 7.250   Min.   :0.004528
 1st Qu.: 8.098          1st Qu.:4.380     1st Qu.: 7.250   1st Qu.:0.007384
 Median :12.321          Median :5.134     Median : 7.250   Median :0.008656
 Mean   :12.323          Mean   :5.236     Mean   : 9.453   Mean   :0.008728
 3rd Qu.:15.202          3rd Qu.:5.985     3rd Qu.:12.500   3rd Qu.:0.009807
 Max.   :26.117          Max.   :8.645     Max.   :13.000   Max.   :0.018355
>
> # 3. RUN THE REGRESSION MODEL (Ordinary Least Squares - OLS)
> # We test if our Wage-to-Rent Ratio significantly predicts SNAP rates
> # controlling for Median Income and Unemployment
> policy_model <- lm(snap_participation_rate ~ wage_to_rent_ratio + median_income + unemployment_rate, data = welfare_data)
>
> # 4. OUTPUT THE ECONOMETRIC METRICS
> # This calculates your coefficients, standard errors, t-statistics, and p-values
> summary(policy_model)

Call:
lm(formula = snap_participation_rate ~ wage_to_rent_ratio + median_income +
    unemployment_rate, data = welfare_data)

Residuals:
    Min      1Q  Median      3Q     Max
-7.7206 -1.8506 -0.2476  1.7626  7.9320

Coefficients:
                     Estimate Std. Error t value Pr(>|t|)
(Intercept)         1.642e+01  2.288e+00   7.180 9.33e-11 ***
wage_to_rent_ratio  2.619e+02  1.442e+02   1.816   0.0721 .
median_income      -1.523e-04  1.359e-05 -11.207  < 2e-16 ***
unemployment_rate   1.042e+00  2.044e-01   5.096 1.48e-06 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 2.818 on 108 degrees of freedom
Multiple R-squared:  0.7016,    Adjusted R-squared:  0.6933
F-statistic: 84.64 on 3 and 108 DF,  p-value: < 2.2e-16

>
> 
