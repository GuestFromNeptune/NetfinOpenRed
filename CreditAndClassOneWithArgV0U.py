# -*- coding: utf-8 -*-
"""
to process the INPUT FILEs or options, all OPTIONAL:
    -D : working directory, which by default will be the current One.
    -P : file Personal Customer Detail Daily. zip or text file.
    -A : file Total Personal Account Detail Daily. zip or text file.
    -T : file containing full customer telephone number list. xlsx file.'Tele.xlsx' by default.
    -B : file containing customers' belongs, Such as BRANCHES and Customer Managers. PrsnlCustOpenBranch.xlsx by defalut.'
    -O :  the OUTPUT file name, which will be xlsx file. OP_NetFinDptOpenRedData.xlsx by default.
to OUTPUT to FILE:
"""

#%%
#sector of importion

import os
import argparse

import pandas as pd
import sqlite3

#%%
#parse arguments
parser = argparse.ArgumentParser()
parser.description='Find the telephone numbers and cust belongs of  customers  \
    which have Class A accounts and activated credit cards. The parameters to process the INPUT FILEs are all OPTIONAL:'

parser.add_argument("-D", "--Dir", help="this parameter is to indicate the \
                    working directory, which by default will be the one containing this .py file. \
                        And it will be the OUTPUT directory.",  dest = "Dir", \
                        type=str, default=os.getcwd())
    
parser.add_argument("-P", "--PersonalCustDetailDaily", help="this parameter is to appoint \
                    the file Personal Customer Detail Daily. \
                        'FilePersonalCustomerDetial_DailyRpt_yyyy-mm-dd_.txt' by default. Support .zip or .txt Files.", \
                            dest="PersonalCustDetailDaily", \
                        type = str , default="FilePersonalCustomerDetial_DailyRpt_yyyy-mm-dd.txt")

parser.add_argument("-A", "--TotalPersonalAcctDetailDaily", help="this parameter is to appoint \
                    the file Total Personal Account Detail Daily. \
                        'FileFullPersonalAcctDetailTbl-DailyRpt_yyyy-mm-dd_.txt' by default. Support .zip or .txt Files.", \
                            dest="TotalPersonalAcctDetailDaily" ,\
                        type = str , default="FileFullPersonalAcctDetailTbl-DailyRpt_yyyy-mm-dd.txt")
    
parser.add_argument("-T", "--TelList", help="this parameter is to appoint \
                    the file containing full customer telephone number list. xlsx file.'Tele.xlsx' by default.", \
                         dest="TelList", type = str , default="Tele.xlsx")
    
parser.add_argument("-B", "--Belongs", help="this parameter is to appoint \
                    the file containing customers' belongs, Such as BRANCHES and Customer Managers.", \
                        dest="Belongs", type = str, default = 'PrsnlCustOpenBranch.xlsx')

parser.add_argument("-O", "--OutputFile", help="this parameter is to appoint \
                    the OUTPUT file name, which will be xlsx file and will be put into the --Dir directory.", \
                        dest="OutputFile", type = str, default = 'OP_NetFinDptOpenRedData.xlsx')
args = parser.parse_args()


#%%

con = sqlite3.connect(":memory:") # Connect to Database

#change the working directory
os.chdir(args.Dir)

#Load the files of Tele and PrsnlCustOpenBranch
#shall be excel files!!!!!

pdTeleList = pd.read_excel(args.TelList)
pdPrsnlCustBlg = pd.read_excel(args.Belongs)

pdTeleList.to_sql('tblTeleList',con)
pdPrsnlCustBlg.to_sql('tblPrsnlCustBlg',con)

#%%
#Load  PersonalCustomerDetial_DailyRpt  and  FullPersonalAcctDetailTbl-DailyRpt
#shall be .zip or .txt files!!!

#set the encoding arguments
pdPrsnlCusDtlDaily = pd.read_table(args.PersonalCustDetailDaily, sep='|', \
                                 header=0 ,encoding="gb18030")
pdTtlPsnlAcctDtlDaily = pd.read_table(args.TotalPersonalAcctDetailDaily, \
                                    sep='|',header=0 ,encoding="gb18030") 
#%%
#TO CLEAN the DATA!!
#Trim them!
pdPrsnlCusDtlDaily['CustName'] = pdPrsnlCusDtlDaily['CustName'].str.strip()
pdPrsnlCusDtlDaily['CustGrade'] = pdPrsnlCusDtlDaily['CustGrade'].str.strip()
pdPrsnlCusDtlDaily['FirstLoginOfCreditCrdApp'] = pdPrsnlCusDtlDaily['FirstLoginOfCreditCrdApp'].str.strip()
pdPrsnlCusDtlDaily['MobiAppLastLogin'] = pdPrsnlCusDtlDaily['MobiAppLastLogin'].str.strip()
pdPrsnlCusDtlDaily['BirthDate'] = pdPrsnlCusDtlDaily['BirthDate'].str.strip()

#for col_pdPrsnlCusDtlDaily in pdPrsnlCusDtlDaily:
#    print(col_pdPrsnlCusDtlDaily)
pdPrsnlCusDtlDaily.applymap(lambda x:x.strip() if type(x) == str else x)
    
pdTtlPsnlAcctDtlDaily['ClientName'] = pdTtlPsnlAcctDtlDaily['ClientName'].str.strip()
pdTtlPsnlAcctDtlDaily['AcctOpenDate'] = pdTtlPsnlAcctDtlDaily['AcctOpenDate'].str.strip()
pdTtlPsnlAcctDtlDaily['AcctClas'] = pdTtlPsnlAcctDtlDaily['AcctClas'].str.strip()
pdTtlPsnlAcctDtlDaily['AcctOpenTeller'] = pdTtlPsnlAcctDtlDaily['AcctOpenTeller'].str.strip()
pdTtlPsnlAcctDtlDaily['AcctCancelDate'] = pdTtlPsnlAcctDtlDaily['AcctCancelDate'].str.strip()

pdTtlPsnlAcctDtlDaily.applymap(lambda x:x.strip() if type(x) == str else x)
#%%

#Load to the Database：

#PersonalCustomerDetial_DailyRpt
pdPrsnlCusDtlDaily.to_sql('tblPrsnlCusDtlDaily', con, if_exists='replace')
#FullPersonalAcctDetailTbl-DailyRpt
pdTtlPsnlAcctDtlDaily.to_sql('tblTtlPsnlAcctDtlDaily',con, if_exists='replace')

# Acct Class A
qryCustAcctClassOne = pd.read_sql_query("SELECT tblPrsnlCusDtlDaily.CustID, tblPrsnlCusDtlDaily.CustName, tblPrsnlCusDtlDaily.BelongToBranch, \
                                        tblPrsnlCusDtlDaily.AcctOpenDate, tblPrsnlCusDtlDaily.MobiBankStatus, tblPrsnlCusDtlDaily.MobiAppLastLogin, \
                                            tblPrsnlCusDtlDaily.NewVerMobiAppLastLogin, tblPrsnlCusDtlDaily.WechatBankStatus, tblPrsnlCusDtlDaily.FirstLoginOfCreditCrdApp,  \
                                                tblTtlPsnlAcctDtlDaily.AcctClas \
                                        FROM tblPrsnlCusDtlDaily, tblTtlPsnlAcctDtlDaily \
                                        WHERE  tblPrsnlCusDtlDaily.CustID=tblTtlPsnlAcctDtlDaily.CustID and trim(tblTtlPsnlAcctDtlDaily.AcctClas)='A' " ,con )
qryCustAcctClassOne.head()
qryCustAcctClassOne.to_sql('qryCustAcctClassOne', con, if_exists='replace')
qryM2_CustAcctClassOneTel = pd.read_sql_query("SELECT strftime('%Y',AcctOpenDate) AS AcctOpenYear, \
                                              qryCustAcctClassOne.CustID AS CustID, CustName, \
                                              BelongToBranch, tblTeleList.OPEN_br AS AcctOpenBranch, \
                                                  AcctOpenDate, MobiBankStatus, MobiAppLastLogin, NewVerMobiAppLastLogin, WechatBankStatus, FirstLoginOfCreditCrdApp, AcctClas, tblTeleList.Tele AS Tele \
                                              FROM qryCustAcctClassOne LEFT JOIN tblTeleList ON qryCustAcctClassOne.CustID = tblTeleList.CustID \
                                                  WHERE strftime('%Y',AcctOpenDate) >= 'YYYY' ", con)
#appender the filter of AcctOpenDate >= YYYY 
qryM2_CustAcctClassOneTel.to_sql('qryM2_CustAcctClassOneTel', con, if_exists='replace')

#select the activated Credit cards
qryCreditActivated = pd.read_sql_query("SELECT tblPrsnlCusDtlDaily.CustID, tblPrsnlCusDtlDaily.CustName, tblPrsnlCusDtlDaily.BelongToBranch, \
                                       tblPrsnlCusDtlDaily.AcctOpenDate, \
                                           tblPrsnlCusDtlDaily.MobiBankStatus, tblPrsnlCusDtlDaily.MobiAppLastLogin, tblPrsnlCusDtlDaily.NewVerMobiAppLastLogin, \
                                               tblPrsnlCusDtlDaily.WechatBankStatus, tblPrsnlCusDtlDaily.FirstLoginOfCreditCrdApp , 'cre' as AcctClas\
                                                   FROM tblPrsnlCusDtlDaily where tblPrsnlCusDtlDaily.IfCreditCardActivated='1'" ,con)
qryCreditActivated.head()
qryCreditActivated.to_sql('qryCreditActivated', con, if_exists='replace')
#To find their telephone numbers with LEFT JOINS
qryM2_CreditActivated = pd.read_sql_query("SELECT strftime('%Y',AcctOpenDate) AS AcctOpenYear, \
                                          qryCreditActivated.CustID AS CustID, CustName, \
                                          BelongToBranch, tblTeleList.OPEN_BR AS AcctOpenBranch, \
                                              AcctOpenDate, MobiBankStatus, MobiAppLastLogin, NewVerMobiAppLastLogin, WechatBankStatus, FirstLoginOfCreditCrdApp, AcctClas, tblTeleList.Tele AS Tele \
                                          FROM qryCreditActivated LEFT JOIN tblTeleList ON qryCreditActivated.CustID = tblTeleList.CustID \
                                              WHERE strftime('%Y',AcctOpenDate) >= 'YYYY' ", con)
#appender the filter of AcctOpenDate >= YYYY 
qryM2_CreditActivated.to_sql('qryM2_CreditActivated', con, if_exists='replace')

#Merge above
qryM2_UnionCreditAndClassOne_YYYY = pd.read_sql_query("SELECT CustID, CustName, BelongToBranch, AcctOpenBranch, \
                                                          AcctOpenDate, MobiBankStatus, \
                                                              MobiAppLastLogin, NewVerMobiAppLastLogin, WechatBankStatus, FirstLoginOfCreditCrdApp,  \
                                                                  AcctClas, Tele \
                                                              FROM qryM2_CustAcctClassOneTel \
                                                                  UNION ALL \
                                                      SELECT CustID, CustName, BelongToBranch, AcctOpenBranch, \
                                                          AcctOpenDate, MobiBankStatus, \
                                                              MobiAppLastLogin, NewVerMobiAppLastLogin, WechatBankStatus, FirstLoginOfCreditCrdApp,  \
                                                                  AcctClas,  Tele \
                                                            FROM qryM2_CreditActivated ", con)
                                                            
qryM2_UnionCreditAndClassOne_YYYY.to_sql('qryM2_UnionCreditAndClassOne_YYYY', con, if_exists='replace')
#%%
#To get which the branch that customers belong to
qryM2_CdtClassOneTelBlg = pd.read_sql_query("SELECT [qryM2_UnionCreditAndClassOne_YYYY].CustID AS CustID, [qryM2_UnionCreditAndClassOne_YYYY].CustName, Tele , \
                                                BelongToBranch, \
                                                    tblPrsnlCustBlg.employeeBelongBranch AS BelongBranch, tblPrsnlCustBlg.EmployeeName AS CustManager, \
                                                    AcctOpenDate, MobiBankStatus, \
                                                    MobiAppLastLogin, NewVerMobiAppLastLogin, WechatBankStatus, FirstLoginOfCreditCrdApp,  \
                                                    AcctClas \
                                            FROM qryM2_UnionCreditAndClassOne_YYYY LEFT JOIN tblPrsnlCustBlg ON tblPrsnlCustBlg.CustID=qryM2_UnionCreditAndClassOne_YYYY.CustID \
                                                ORDER BY [qryM2_UnionCreditAndClassOne_YYYY].CustID, Tele \
                                            ", con)
qryM2_CdtClassOneTelBlg.to_sql('qryM2_CdtClassOneTelBlg', con, if_exists='replace')

#Try to delete the duplicated records...
qryM2_CdtClassOneTelBlg_Idt = pd.read_sql_query("SELECT DISTINCT * FROM qryM2_CdtClassOneTelBlg ", con)

#%%
#Prepare to output
qryM2_CdtClassOneTelBlg_Idt.to_excel(args.OutputFile)
