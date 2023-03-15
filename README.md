# NetfinOpenRed
To calculate OpenRed Data for Netfin Department
to process the INPUT FILEs or options, all OPTIONAL:
    -D : working directory, which by default will be the current One.
    -P : file Personal Customer Detail Daily. zip or text file.
    -A : file Total Personal Account Detail Daily. zip or text file.
    -T : file containing full customer telephone number list. xlsx file.'Tele.xlsx' by default.
    -B : file containing customers' belongs, Such as BRANCHES and Customer Managers. PrsnlCustOpenBranch.xlsx by defalut.'
    -O :  the OUTPUT file name, which will be xlsx file. OP_NetFinDptOpenRedData.xlsx by default.

The programe will achieve the goal by using pandas and sqlite3.
