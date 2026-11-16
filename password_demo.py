from werkzeug.security import generate_password_hash, check_password_hash

password = "CorrectHorseBatteryStaple!" # demo only, don't reuse this in real life

stored_hash = generate_password_hash(password)
print("STORED HASH:", stored_hash)

print("RIGHT:", check_password_hash(stored_hash, "CorrectHorseBatteryStaple!"))
print("WRONG:", check_password_hash(stored_hash, "CorrectHorseBatteryStaplee"))
