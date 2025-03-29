from pymongo import MongoClient
import datetime

client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.4.2")

oplog = client.local.oplog.rs

last_timestamp = oplog.find().sort("$natural", -1).limit(1)[0]["ts"]

print("Monitorando alterações no MongoDB...")

while True:

    cursor = oplog.find({"ts": {"$gt": last_timestamp}}, cursor_type=2)

    for doc in cursor:
        last_timestamp = doc["ts"]

        operacao = doc.get("op", "N/A")
        banco = doc.get("ns", "N/A")
        documento = doc.get("o", {})
        timestamp = datetime.datetime.fromtimestamp(last_timestamp.time)

        print(f"[{timestamp}] Operação: {operacao} | Banco: {banco} | Dados: {documento}")