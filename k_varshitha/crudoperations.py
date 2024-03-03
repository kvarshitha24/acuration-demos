from pymongo import MongoClient
def connect_to_mongodb(uri):
    return MongoClient(uri)

def insert_prompt(client, prompt_text, tags, prompt_id):
    db = client.my_database
    prompts_collection = db.prompts
    prompt_doc = {"prompt_text": prompt_text, "tags": tags, "id": prompt_id}
    prompts_collection.insert_one(prompt_doc)

def insert_tag(client, tag_name, tag_id):
    db = client.my_database
    tags_collection = db.tags
    tag_doc = {"tag_name": tag_name, "id": tag_id}
    tags_collection.insert_one(tag_doc)

def query_tag(client, tag_name):
    db = client.my_database
    tags_collection = db.tags
    query = {"tag_name": tag_name}
    return tags_collection.find(query)

def update_tag(client, old_tag_name, new_tag_name):
    db = client.my_database
    tags_collection = db.tags
    query = {"tag_name": old_tag_name}
    new_values = {"$set": {"tag_name": new_tag_name}}
    tags_collection.update_one(query, new_values)

def delete_tag(client, tag_name):
    db = client.my_database
    tags_collection = db.tags
    query = {"tag_name": tag_name}
    tags_collection.delete_one(query)

if __name__ == "__main__":
    client = connect_to_mongodb("mongodb+srv://akkuluri66:Mahesh%404444@cluster0.lrkegak.mongodb.net/Ecommers")