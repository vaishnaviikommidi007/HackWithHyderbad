from memory import client

try:
    client.create_bank(bank_id="demo-fresh", name="Demo Fresh")
except Exception as e:
    print("Bank note:", e)
client.close()