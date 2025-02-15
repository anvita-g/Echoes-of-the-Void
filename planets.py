import subprocess
import random


# modify the path according to you ollama settings
OLLAMA_PATH = "C:\\Users\\Anvita\\AppData\\Local\\Programs\\Ollama\\ollama.exe"
MODEL = "mistral" 

PLANET_TYPES = ["Jungle", "Desert", "Frozen", "Toxic", "Volcanic", "Oceanic"]

def generate_planet():
    """Generates a short, concise planet description with strategic hints."""
    planet_name = f"Planet-{random.randint(100, 999)}"
    planet_type = random.choice(PLANET_TYPES)

    prompt = f"Describe a {planet_type.lower()} planet in one sentence for a sci-fi survival game, including a hint of what resources or hazards await."

    try:
        process = subprocess.Popen(
            [OLLAMA_PATH, "run", MODEL, prompt.strip()],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8"
        )

        description = ""
        for line in process.stdout:
            line = line.strip()
            if line:
                description += line + " "

        for line in process.stderr:
            pass

        process.wait()

        if process.returncode != 0:
            description = f"A mysterious {planet_type.lower()} planet (AI error)."

        description = description.strip()

        if not description:
            description = f"A mysterious {planet_type.lower()} planet with no clear details."

    except Exception as e:
        description = f"A mysterious {planet_type.lower()} planet (AI call failed)."

    hint = ""
    impact = ""

    if planet_type == "Frozen":
        hint = "Frozen wastes hide hidden energy sources, but watch out for deadly blizzards."
        impact = "A rare medicinal plant might restore some health, but the cold cuts down your resources."
    elif planet_type == "Desert":
        hint = "Scarcity of water and extreme temperatures make survival challenging here."
        impact = "You can barter with a merchant for food, but it will cost you valuable supplies."
    elif planet_type == "Jungle":
        hint = "Teeming wildlife offers both danger and valuable resources if you can survive."
        impact = "Ancient ruins may provide a clue that leads you toward Haven-1, but the creatures are dangerous."
    elif planet_type == "Toxic":
        hint = "High toxicity levels threaten your health, but rare metals can be found."
        impact = "Toxic fumes drain your health, but scavenging rare materials could improve your ship's build."
    elif planet_type == "Volcanic":
        hint = "Volcanic activity could be deadly, but there’s abundant geothermal energy."
        impact = "You might find geothermal power sources that could help your ship's energy reserves."
    elif planet_type == "Oceanic":
        hint = "Vast oceans hide underwater cities and potential salvage, but currents are deadly."
        impact = "You can salvage old tech from the ocean floor, improving your ship's build, but the currents are perilous."

    description += " " + hint + " " + impact

    return {
        "name": planet_name,
        "type": planet_type,
        "desc": description,
        "hazard": random.choice(["Low Oxygen", "Extreme Radiation", "Unstable Terrain", "None"])
    }


import random

def explore_planet(planet, player):
    """Handles the logic when the player lands on a planet."""
    print(f"\n🛬 Landing on {planet['name']}...")
    print(f"🌍 Planet Type: {planet['type']} - {planet['desc']}")

    if planet["hazard"] != "None":
        print(f"⚠️ HAZARD: {planet['hazard']} - You lose health!")
        damage = random.randint(5, 15)
        player.update_health(-damage)

    if planet["type"] == "Frozen":
        print("❄️ The cold is harsh. Your health takes a hit!")
        health_loss = random.randint(5, 15)
        player.update_health(-health_loss)

        if random.random() < 0.4:
            print("🌿 You discover a medicinal plant! Your health improves.")
            player.update_health(random.randint(10, 20))

    elif planet["type"] == "Desert":
        print("🌵 The desert is unforgiving. You risk dehydration!")
        hydration_loss = random.randint(5, 10)
        player.update_health(-hydration_loss)

        if random.random() < 0.5:
            print("👽 You encounter a merchant! Bartering for food.")
            food = random.randint(1, 3)
            player.barter_for_food(food)

    elif planet["type"] == "Jungle":
        print("🌳 The jungle is teeming with life, both dangerous and useful.")
        creature_encounter = random.random()

        if creature_encounter < 0.3:
            print("🐍 You are attacked by wildlife! Your health is damaged.")
            player.update_health(-random.randint(5, 15))

        if creature_encounter < 0.5:
            print("🗺️ You discover ancient ruins! A clue leads you closer to Haven-1.")
            player.add_clue("A clue to Haven-1 discovered in the jungle ruins!")

    elif planet["type"] == "Toxic":
        print("☠️ The air is toxic. You feel the strain on your health.")
        toxic_damage = random.randint(10, 20)
        player.update_health(-toxic_damage)

        if random.random() < 0.3:
            print("⚙️ You find rare materials that can help upgrade your ship.")
            player.upgrade_ship(random.randint(1, 3))

    elif planet["type"] == "Volcanic":
        print("🌋 The volcanic environment is dangerous, but energy-rich.")
        lava_damage = random.randint(10, 15)
        player.update_health(-lava_damage)

        if random.random() < 0.4:
            print("⚡ You discover a geothermal vent! Your ship’s energy reserves improve.")
            player.upgrade_ship(2)

    elif planet["type"] == "Oceanic":
        print("🌊 The oceans are vast and perilous, with hidden dangers.")
        water_damage = random.randint(5, 10)
        player.update_health(-water_damage)

        if random.random() < 0.3:
            print("🛠️ You salvage useful tech from the ocean floor, improving your ship.")
            player.upgrade_ship(random.randint(1, 2))

    if player.health <= 0:
        print("\n💀 You have succumbed to the dangers of the planet. GAME OVER.")
        return False

    if player.ship_integrity <= 0:
        print("\n🚨 Your ship is beyond repair. GAME OVER.")
        return False 
    return True