import sqlite3

DATABASE = "keywords (copie).db"
INPUTS  = "inputs-c.txt"


def sort_():
    with open(INPUTS, 'r') as f:
        contents = f.readlines()
        f.close()
        
    contents_ = list()
    refused = ["\n","\t"," ","\r"]
    for row in contents:
        row = row.lower()
        for i in refused:
            row = row.replace(i, "")
        contents_.append(row)
    contents_.sort()
    
    with open(INPUTS, 'w') as f:
        for row in contents_:
            f.write(row + "\n")
        f.close()

def load_items():
    with open(INPUTS, 'r') as f:
        contents = f.readlines()
        f.close()
    
    contents_ = list()
    for row in contents:
        row = row.replace("\n","")
        weight = 6
        contents_.append({'keyword':row, 'weight':weight})

    return contents_

#sort_()
connected = False
try:
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    connected = True

    items = load_items()
    request_x = "INSERT INTO languages(name) VALUES(?)"
    request_y = "INSERT INTO keywords(keyword,weight,language_id) VALUES(?,?,?)"
    request_z = "SELECT * FROM keywords WHERE keyword=?"
    request_a = "UPDATE keywords SET weight=? WHERE id=? AND keyword=?"

    cursor.execute(request_x, ['c'])
    for item in items:
        childs = cursor.execute(request_z, [item['keyword']])
        childs = childs.fetchall()

        if (childs is not None) and (len(childs) != 0):
            length = len(childs)
            item['weight'] = 6 - length
            for child in childs:
                weight = child['weight'] - 1
                id_ = child['id']
                keyword = child['keyword']
                
                cursor.execute(request_a,[weight,id_,keyword])

        item['language_id'] = 4
        cursor.execute(request_y, [item['keyword'],item['weight'],item['language_id']])
    
    conn.commit()

except Exception as err:
    raise(err)

finally:
    if connected:
        cursor.close()
        conn.close()