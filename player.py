class Player:
    def __init__(self):
        self.health = 100 
        self.fuel = 5
        self.ship_integrity = 100
        self.inventory = {"food": 2, "ship_parts": 1, "maps": 0}

    def update_health(self, amount):
        self.health = max(0, min(100, self.health + amount))
        print(f"❤️ Health updated: {self.health}%")

    def update_fuel(self, amount):
        self.fuel = max(0, self.fuel + amount)
        print(f"⛽ Fuel updated: {self.fuel} jumps remaining.")

    def repair_ship(self, amount):
        if self.inventory["ship_parts"] > 0:
            self.inventory["ship_parts"] -= 1
            self.ship_integrity = min(100, self.ship_integrity + amount)
            print(f"🛠️ Ship repaired! Integrity now at {self.ship_integrity}%.")
        else:
            print("❌ No ship parts available for repairs!")

    def check_status(self):
        print(f"\n=== Captain's Status ===")
        print(f"❤️ Health: {self.health}%")
        print(f"🛠️ Ship Integrity: {self.ship_integrity}%")
        print(f"⛽ Fuel: {self.fuel} jumps")
        print(f"🎒 Inventory: {self.inventory}")
        print("=====================\n")

    def is_alive(self):
        return self.health > 0

    def has_fuel(self):
        return self.fuel > 0
