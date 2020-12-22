import tabula
import pymongo
import hashlib
import pandas

# common functions

def is_not_nan(val):
    return val == val

def concat_rows(tbl, common_col):
    tmp_df = pandas.DataFrame(columns=tbl.columns)
    ind = -1
    for index, row in tbl.iterrows():
        if(is_not_nan(row[common_col])):
            ind+=1
            tmp_df.loc[ind]=['']*len(tbl.columns)
        for col in tbl.columns:
            tmp_df.loc[ind][col]+=" "+str(row[col] if is_not_nan(row[col]) else "")
            tmp_df.loc[ind][col]=tmp_df.loc[ind][col].strip()
    return tmp_df

def merge_col_row(tbl, last_row):
    col = [str(i if is_not_nan(i) and i.find("Unnamed:") == -1 else "") for i in tbl.columns.to_list()]
    for row_ind in range(last_row+1):
        for col_ind in range(len(col)):
            row_item = tbl.loc[row_ind][col_ind]
            col[col_ind] += " " if len(col[col_ind]) > 0 and col[col_ind][-1]!="/" and col[col_ind][-1]!="(" and col[col_ind][-1]!="_" else ""
            col[col_ind] += str(row_item) if is_not_nan(row_item) else ""
            col[col_ind] = col[col_ind].strip()
    
    tbl.columns = col
    tbl = tbl.iloc[last_row+1:].reset_index(drop=True)
    return tbl

def fill_blank_cell(tbl, column_name):
    for index, row in tbl.iterrows():
        if tbl.loc[index][column_name] == "":
            if index != 0:
                tbl.loc[index][column_name] = tbl.loc[index-1][column_name]
            else:
                tbl.loc[index][column_name] = "-"
    return tbl

def populate_unnamed_col(tbl):
    col = [str(i if is_not_nan(i) and i.find("Unnamed:") == -1 else "") for i in tbl.columns.to_list()]
    ind = -1
    for i in range(0,len(col)):
        if col[i] == '':
            ind = i
        else:
            if ind != -1:
                col[i] = col[i]+"_"
                for j in range(ind, i):
                    col[j] = col[i]
                ind = -1
    tbl.columns = col
    return tbl

def remove_dots(tbl):
    col = [str(i if is_not_nan(i) and i.find("Unnamed:") == -1 else "") for i in tbl.columns.to_list()]
    for i in range(0,len(col)):
        col[i] = col[i].replace('.', '')
    tbl.columns = col
    return tbl

# establishing connection with database
client = pymongo.MongoClient(port=27017)
db=client.task3a # name of the database

try:

    filepath = input("Enter File Path: ")

    filemd5 = hashlib.md5(open(filepath,'rb').read()).hexdigest()

    # for 1c1edeee-a13e-4b2e-90be-eb1dd03c3384.pdf
    if filemd5 == "1140f720233a94542f842b3994de6267":
        print("Reading {}".format(filepath))

        tables =  tabula.read_pdf(filepath, pages="all")

        # first table
        t1 = tables[0]
        collection = db["tbl_{}_{}".format(1, filemd5)]
        collection.insert_many(t1.to_dict('records'))
        print("Successfully inserted tables in database")

    # for a6b29367-f3b7-4fb1-a2d0-077477eac1d9.pdf
    elif filemd5 == "cb7652530d59e55bd75181549fb77e45":
        print("Reading {}".format(filepath))

        tables =  tabula.read_pdf(filepath, pages="all")

        # first table
        t1 = tables[0]
        # merge rows based on a particular column
        t1 = concat_rows(t1, 'Type ofMeeting')
        # inserting into database
        collection = db["tbl_{}_{}".format(1, filemd5)]
        collection.insert_many(t1.to_dict('records'))
        print("Successfully inserted tables in database")

    # for d9f8e6d9-660b-4505-86f9-952e45ca6da0.pdf
    elif filemd5 == "43053a8e8020a8534c12a15d1bfa5a50":
        print("Reading {}".format(filepath))

        tables =  tabula.read_pdf(filepath, pages="1", area=(338.21617916107175, 55.43917568206787, 444.62963047027586, 527.2302814865112))

        # first table
        t1 = tables[0]
        # merge rows based on a particular column
        t1 = concat_rows(t1, 'Location')
        # populating empty cells from above cells
        t1 = fill_blank_cell(t1, 'Date')
        # manually cleaning data 
        t1.loc[1][1] = t1.loc[1][1][0:-2]
        # inserting into database
        collection = db["tbl_{}_{}".format(1, filemd5)]
        collection.insert_many(t1.to_dict('records'))
        print("Successfully inserted tables in database")

    # for EICHERMOT.pdf
    elif filemd5 == "5e4987f2216d7521a991778fd6e21a34":
        print("Reading {}".format(filepath))

        tables = tabula.read_pdf(filepath, pages="all", stream=True, guess=False, area=[(195.06903282165527, 306.93918800354004, 275.68719795227054, 550.25825340271), (263.7816779327393, 53.94688758850098, 343.3998430633545, 298.0100479888916), (578.5338634490967, 54.690982589721685, 667.8252635955811, 549.5141584014892)])

        # first table
        t1 = tables[0]
        # merge first row and column
        t1 = merge_col_row(t1, 0)
        # merge rows based on a particular column
        t1 = concat_rows(t1, 'Sl. No.')
        # remove dots from column name
        t1 = remove_dots(t1)
        # inserting into database
        collection = db["tbl_{}_{}".format(1, filemd5)]
        collection.insert_many(t1.to_dict('records'))

        # second table
        t2 = tables[1]
        # merge first two rows and column
        t2 = merge_col_row(t2, 1)
        # remove dots from column name
        t2 = remove_dots(t2)
        # manually cleaning data
        t2  = t2.rename(columns={'No of1 meetings attended': 'No of meetings attended'})
        # inserting into database
        collection = db["tbl_{}_{}".format(2, filemd5)]
        collection.insert_many(t2.to_dict('records'))

        # third table
        t3 = tables[2]
        # populating unnamed columns to deal witht subheadings
        t3 = populate_unnamed_col(t3)
        # if a subheading exists, it is going to be appended with a _ to heading
        # merge first row and column
        t3 = merge_col_row(t3, 0)
        # merge rows based on a particular column
        t3 = concat_rows(t3, 'Salary')
        # inserting into database
        collection = db["tbl_{}_{}".format(3, filemd5)]
        collection.insert_many(t3.to_dict('records'))
        print("Successfully inserted tables in database")

    else:
        print("Reading {}".format(filepath))

        tables =  tabula.read_pdf(filepath, pages="all")
        for i in range(0, len(tables)):
            t1 = table[i]
            collection = db["tbl_{}_{}".format(i, filemd5)]
            collection.insert_many(t1.to_dict('records'))
        if len(tables) > 0 :
            print("Successfully inserted tables in database")
        else:
            print("No tables found")
except IOError:
    print("Error! File not found")
except:
    print("Error while reading the file")
# Developed by: Shlok Pandey (@b30wulffz)