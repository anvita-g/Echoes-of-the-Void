import random
from planets import generate_planet
from player import Player
from trade import trade_with_aliens
from clues import get_random_clue

def main():
    print("\n=== 🚀 Welcome to Echoes of the Void ===")
    player = Player()

    while True:
        player.check_status()

        print("\nNOVA: 'Captain, we have 3 possible destinations. Choose wisely!'")

        planets = [generate_planet() for _ in range(3)]

        for i, planet in enumerate(planets, 1):
            print(f"{i}. {planet['name']} ({planet['type']}) - {planet['desc']}")

        choice = input("\n> Choose a planet (1-3) or type 'exit' to quit: ").strip().lower()

        if choice == "exit":
            print("NOVA: 'Ending mission. Safe travels, Captain.'")
            break
        if choice in ["1", "2", "3"]:
            planet = planets[int(choice) - 1]
            print(f"\n🛬 Landing on {planet['name']}...")

            if planet["hazard"] != "None":
                print(f"⚠️ HAZARD: {planet['hazard']} - You lose health!")
                player.update_health(-random.randint(5, 15))

        else:
            print("❌ Invalid choice. Try again.")
            continue

        if not player.is_alive():
            print("\n💀 Your health has dropped to 0. GAME OVER.")
            break

        if random.random() < 0.5:
            print("\n👾 You encounter a traveling alien merchant!")
            trade_with_aliens(player)

        if random.random() < 0.3:
            clue = get_random_clue()
            print(f"\n🔍 CLUE DISCOVERED: {clue}")

        player.ship_integrity -= random.randint(1, 3)
        if player.ship_integrity <= 0:
            print("\n🚨 Your ship has fallen apart. GAME OVER.")
            break

        if not player.has_fuel():
            print("\n⛽ You have run out of fuel. GAME OVER.")
            break

if __name__ == "__main__":
    main()
