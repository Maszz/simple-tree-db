from TreeDataBase import TreeDataBase


if __name__ == "__main__":
    db = TreeDataBase()
    db.create_tree_db("data.db", {}, "o=ผ้าปู")
    db.insert({"meta1": "meta_val"}, "o=ผ้าปู,m=cotton")
    db.insert({"meta1": "meta_val"}, "o=ผ้าปู,m=silk")
    db.insert({"meta1": "meta_val"}, "o=ผ้าปู,m=wool")
    db.insert({"meta1": "meta_val"}, "o=ผ้าปู,m=linen")
    db.insert({"meta1": "meta_val"}, "o=ผ้าปู,m=cotton,c=white")
    db.insert({"meta1": "meta_val"}, "o=ผ้าปู,m=cotton,c=black")
    db.insert({"meta1": "meta_val"}, "o=ผ้าปู,m=silk,c=red")
    db.insert({"meta1": "meta_val2"}, "o=ผ้าปู,m=cotton,c=white,s=king")
    db.insert({"meta1": "meta_val"}, "o=ผ้าปู,m=cotton,c=white,s=queen")
    db.insert({"meta1": "meta_val"}, "o=ผ้าปู,m=cotton,c=black,s=king")
