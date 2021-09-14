##################################################################################################################
############################################# CLTV WITH SALES SAMPLE DATA ########################################
##################################################################################################################

##################################################################################################################
# Libraries
##################################################################################################################
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 20)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

data = pd.read_csv("Ders Notları/sales_data_sample.csv", encoding = "Latin-1")
df = data.copy()
df.columns

def cltv_calculator(df, segment_checker = False):

    # Descriptive Statistics

    print("###########################################################")
    print("READING DATA")
    print("###########################################################")
    print(df.columns)
    print("################")
    print(df.index)
    print("################")
    print(df.shape)
    print("################")
    print(df.info())
    print("################")
    print(df.describe().T)
    print("################")

    # Missing Values

    print("###########################################################")
    print("MISSING VALUE ANALYSIS")
    print("###########################################################")
    print("Is there any missing value?")
    print(df.isnull().values.any())
    missing = df.isnull().values.any()
    if (missing == True):
        print(df.isnull().sum())
    else:
        print("There is no missing value on the dataset")

    print("###########################################################")
    print("IDENTFYING VARIABLE TYPES")
    print("###########################################################")

    cat_cols = [i for i in df.columns if df[i].dtype == "O" and df[i].nunique() <= 20]

    num_but_cat = [i for i in df.columns if df[i].dtype != "O" and df[i].nunique() <= 20]

    cat_cols = cat_cols + num_but_cat

    cat_but_car = [i for i in df.columns if df[i].dtype == "O" and df[i].nunique() > 20]

    num_cols = [i for i in df.columns if df[i].dtype in [int, float] and i not in num_but_cat]

    print("Categorical Varibles: ", cat_cols)
    print("Numerical Varibles: ", num_cols)
    print("Categoric But Cardinal Variables: ", cat_but_car)

    print("###########################################################")
    print("PREPROCESSING")
    print("###########################################################")

    df = df[~df["STATUS"].isin(["Cancelled", "Disputed"])]
    print("It has done :)")

    print("###########################################################")
    print("CLTV METRICS")
    print("###########################################################")

    today_date = dt.datetime(2005, 6, 2)
    cltv_df = df.groupby("CUSTOMERNAME").agg({"ORDERNUMBER": lambda x: x.nunique(),
                                          "QUANTITYORDERED": lambda x: x.nunique(),
                                          "SALES": lambda x: x.sum()})

    cltv_df.columns = ["Total_Transaction", "Total_Unit", "Total_Price"]

    # Customer Value Calculation

    cltv_df["Average_Order_Value"] = cltv_df["Total_Price"] / cltv_df["Total_Transaction"]
    cltv_df["Purchase_Frequency"] = cltv_df["Total_Transaction"] /  cltv_df.shape[0]
    cltv_df["Customer_Value"] = cltv_df["Average_Order_Value"] * cltv_df["Purchase_Frequency"]

    # Churn Rate Calculation

    repeat_rate = cltv_df[cltv_df["Total_Transaction"] > 1].shape[0] / cltv_df.shape[0]
    churn_rate = 1 - repeat_rate

    # Profit Margin Calculation

    cltv_df["Profit_Margin"] = cltv_df["Total_Price"] * 0.1

    # CLTV CALCULATION

    cltv_df["CLTV"] = (cltv_df["Average_Order_Value"] / churn_rate) * cltv_df["Profit_Margin"]
    cltv_df = cltv_df.reset_index()

    # SCALING CLTV VALUES

    scaler = MinMaxScaler(feature_range = (0,1))
    scaler.fit(cltv_df[["CLTV"]])
    cltv_df["Scaled_CLTV"] = scaler.transform(cltv_df[["CLTV"]])

    # CLTV SEGMENTATION

    cltv_df["Segmentation"] = pd.qcut(cltv_df["Scaled_CLTV"], 4, labels = ["D", "C", "B", "A"])

    # FINAL

    print(cltv_df.groupby("Segmentation").agg(["mean", "count"]))

    ### cltv_df.to_excel("cltv_df.xlsx")


cltv_calculator(df, segment_checker = True)
