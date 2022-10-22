import scripts.create_vehicles
import scripts.create_users

USERS_AMOUNT = 100
VEHICLES_AMOUNT = 40

scripts.create_users.create(USERS_AMOUNT)
scripts.create_vehicles.create(VEHICLES_AMOUNT)