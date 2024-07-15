from parser.main_func import main

# print(main("api/data/Resumes/resume22.pdf"))
from routes.resumeRoute import conn

# # import 
import traceback

# # current_directory = os.getcwd()
# # print(current_directory)


# def get_education():
#     try:
#         cursor = conn.cursor()
#         cursor.execute("""SELECT * FROM "Education" where "Education"."Degree"='afafafa';""")
#         records = cursor.fetchall()
#         cursor.close()
#         print("records got:", records)
#         #  records
#     except Exception as fetch_err:
#         print("Error fetching records:", fetch_err)
#     # todos = fetch_records()
#     return records


# # check User
def checkIfFileExistsInDB(filename):
    try:
        cursor = conn.cursor()

        # Step 1: Check if logs for that notification ID have count = fileCount
        query = 'SELECT COUNT(*) FROM "Resume" WHERE "Resume"."FileName" = %s;'
        cursor.execute(query, (filename,))
        total_count = cursor.fetchone()[0]
        print(total_count)
        if total_count>0:
            return True
    
    except Exception as e:
        traceback.print_exc()
        conn.rollback() 
        print(f"Error occurred: {str(e)}")
        return  False
 
# print(DuplicateDetection("ADITYA",'RAJ',[+91620187590,9897859860],['adityaraj.131103@gmail.com']))

# print(get_education())


filename = "[405]-636117b950128fc5b8e68116e010585e77483711a831b3adb82ce31db56c702f!@&1.VikramiOS.pdf"
print(checkIfFileExistsInDB(filename))





# arr = ['746', '748', '749', '754', '758', '825', '767', '768', '769', '775', '778', '781', '782', '783', '784', '826', '792', '793', '794', '801', '803', '804', '805', '806', '808', '829', '830', '821', '823', '824', '842', '844', '847', '854', '856', '857', '858', '860', '864', '866', '875', '876', '887', '889', '890', '891', '893', '894', '899', '905', '906', '1015', '919', '921', '922', '923', '924', '930', '931', '940', '942', '946', '951', '956', '959', '962', '963', '966', '967', '971', '973', '980', '988', '989', '992', '994', '995', '996', '997', '999', '1000', '1007', '1011', '1017', '1022', '1024', '1038', '1039', '1041', '1042', '1045', '1050', '1052', '1060', '1062', '1063', '1064', '1068', '1069', '1077', '1079', '1088', '1089', '1091', '1093', '1095', '1098', '1099', '1104', '1106', '1121', '1122', '1123', '1124', '1126', '1129', '1133', '1138', '1142', '1150', '1151', '1152', '1158', '1160', '1162', '1163', '1164', '1165', '1178', '1190', '1195', '1206', '1208', '1211', '1213', '1215', '1217', '1218', '1220', '1222', '1223', '1224', '1225', '1227', '1233', '1237', '1248', '1255', '1256', '1257', '1259', '1266', '1281', '1282', '1484', '1288', '1294', '1304', '1312', '1314', '1328', '1332', '1338', '1341', '1342', '1343', '1344', '1347', '1348', '1349', '1350', '1351', '1352', '1356', '1357', '1363', '1366', '1376', '1377', '1378', '1380', '1383', '1389', '1391', '1397', '1400', '1402', '1488', '1489', '1425', '1432', '1435', '1439', '1450', '1452', '1453', '1455', '1456', '1499', '1462', '1468', '1470', '1472', '1473', '1476', '1479', '1501', '1502', '1510', '1512', '1515', '1516', '1518', '1520', '1530', '1534', '1536', '1544', '1545', '1547', '1554', '1557', '1674', '1675', '1676', '1677', '1580', '1582', '1678', '1588', '1591', '1593', '1679', '1598', '1606', '1614', '1618', '1619', '1623', '1624', '1629', '1630', '1638', '1639', '1644', '1646', '1650', '1651', '1656', '1657', '1662', '1663', '1666', '1667']

# print(len(set(arr)))


# from fuzzywuzzy import fuzz

# string1 = "New York Jets"
# string2 = "New zork Jess"

# score = fuzz.partial_ratio(string1, string2)
# print(f"Similarity score: {score}")