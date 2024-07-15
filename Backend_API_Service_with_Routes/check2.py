from routes.resumeRoute import conn

import json
import traceback
def read_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def write_json_file(filename, data):
    # filename = f"{user_id}_output.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def edit_folder_name(data:dict):

    try:

        data = dict(data)
        old_name = data["PrevFolderName"]
        new_name = data["NewFolderName"]
        parent_folder = data["ParentFolder"]

        categoryFolders = read_json_file("data/SkillsData/Category.json")
        newDatamap = read_json_file("data/folders/newData.json")


        if parent_folder:
            # print(categoryFolders[parent_folder], old_name)
            
            categoryFolders[parent_folder].remove(old_name)
            categoryFolders[parent_folder].append(new_name)
            newDatamap[new_name] = newDatamap.pop(old_name)

        else:
            categoryFolders[new_name] = categoryFolders.pop(old_name)

        write_json_file("data/folders/newData.json",newDatamap)       
        write_json_file("data/SkillsData/Category.json", categoryFolders)

        return {"status":200, "action": "Folder name edited"}
    
    except Exception as e:
        traceback.print_exc()

        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error occurred: {str(e)}")
        return {"status":400, "action": "Error occured in folder name editing"}
            # return "Error occured in replacing file"
    

# data = {"filename1":"[144]-dac5810929ab8b463d2bb02014ebde714dac2a6e53bbf8f7c2066c78fcc9c3ad!@&DeepakChutani_Resume (1) (1).docx","filename2":"[144]-dac5810929ab8b463d2bb02014ebde714dac2a6e53bbf8f7c2066c78fcc9c3ad!@&DeepakChutani_Resume (1) (1) (1).docx","logId":2171}
# data1= ["[161]-bb69ea717a467a4ac7c6b40edf0e58a925c91840b9bf8e899f1095bd693f9ede!@&1+ year of frontend.pdf,[136]-bb69ea717a467a4ac7c6b40edf0e58a925c91840b9bf8e899f1095bd693f9ede!@&1+ year of frontend.pdf,2469"]
    
data1 = {
"PrevFolderName":"Art Director",
"NewFolderName":"Art Director 1",
"ParentFolder":"Creative & Design",
} 
print(edit_folder_name(data1))