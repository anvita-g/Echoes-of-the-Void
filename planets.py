import subprocess
import random
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os
import whisper
import pyaudio

OLLAMA_PATH = "C:\\Users\\Anvita\\AppData\\Local\\Programs\\Ollama\\ollama.exe"
MODEL = "mistral"

PLANET_TYPES = ["Jungle", "Desert", "Frozen", "Toxic", "Volcanic", "Oceanic"]
PLANET_IMAGES_PATH = "images/"

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

whisper_model = whisper.load_model("base")

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

        error_output = ""
        for line in process.stderr:
            error_output += line.strip() + "\n"

        process.wait()

        if process.returncode != 0:
            description = f"A mysterious {planet_type.lower()} planet (AI error)."
            print(f"Error occurred during AI generation: {error_output}")

        description = description.strip()

        if not description:
            description = f"A mysterious {planet_type.lower()} planet with no clear details."

    except Exception as e:
        description = f"A mysterious {planet_type.lower()} planet (AI call failed)."
        print(f"Exception while generating planet description: {e}")

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

def generate_image_caption(image_path):
    try:
        image = Image.open(image_path)

        inputs = processor(images=image, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)

        return caption
    except Exception as e:
        print(f"Error generating caption: {e}")
        return "No caption available."

def record_voice_input():
    """Records voice input from the microphone and returns the transcribed text."""
    print("🎤 Listening for your voice input...")
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)

    print("🎤 Speak now...")
    frames = []
    for _ in range(0, int(16000 / 1024 * 5)):
        data = stream.read(1024)
        frames.append(data)

    print("🎤 Stop speaking.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_file = "temp.wav"
    with open(audio_file, "wb") as f:
        f.write(b''.join(frames))

    result = whisper_model.transcribe(audio_file)
    return result['text']

def explore_planet(planet, player):
    print(f"\n🛬 Landing on {planet['name']}...")
    print(f"🌍 Planet Type: {planet['type']} - {planet['desc']}")

    image_filename = f"{planet['type'].lower()}.jpg"
    image_path = os.path.join(PLANET_IMAGES_PATH, image_filename)

    if os.path.exists(image_path):
        caption = generate_image_caption(image_path)
        print(f"🖼️ Planet Image Caption: {caption}")
        image = Image.open(image_path)
        image.show()
    else:
        print("⚠️ No image found for this planet type.")

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
        print("🌿 The jungle is dense and dangerous. Watch your step!")
        jungle_hazard = random.choice(["Venomous creature", "Poisonous plant", "Quick sand", "None"])
        if jungle_hazard != "None":
            print(f"⚠️ A {jungle_hazard} attacks you! You lose health.")
            player.update_health(random.randint(10, 20))

        if random.random() < 0.3:
            print("🗺️ You find an ancient ruin with clues that could help you.")
            player.update_health(random.randint(5, 15))

    elif planet["type"] == "Toxic":
        print("☣️ The air is filled with toxins! Your health is slowly draining.")
        toxicity_loss = random.randint(5, 10)
        player.update_health(-toxicity_loss)

        if random.random() < 0.4:
            print("💎 You find rare metals to improve your ship!")
            player.update_ship_build(random.randint(10, 20))

    elif planet["type"] == "Volcanic":
        print("🌋 The volcanic activity is intense! Be careful.")
        volcanic_risk = random.choice(["Lava flow", "Erupting geyser", "None"])
        if volcanic_risk != "None":
            print(f"⚠️ A {volcanic_risk} damages your health!")
            player.update_health(random.randint(10, 25))

        if random.random() < 0.3:
            print("⚡ You find geothermal energy sources that could power your ship.")
            player.update_ship_energy(random.randint(10, 20))

    elif planet["type"] == "Oceanic":
        print("🌊 The oceans are vast, but dangerous currents lurk.")
        ocean_risk = random.choice(["Shark attack", "Tidal wave", "None"])
        if ocean_risk != "None":
            print(f"⚠️ A {ocean_risk} harms your health.")
            player.update_health(random.randint(10, 20))

        if random.random() < 0.5:
            print("🛠️ You salvage old tech from the ocean floor to improve your ship!")
            player.update_ship_build(random.randint(10, 25))

    if player.health <= 0:
        print("\n💀 You have succumbed to the dangers of the planet. GAME OVER.")
        return False

    if player.ship_integrity <= 0:
        print("\n🚨 Your ship is beyond repair. GAME OVER.")
        return False

    return True


response = input("Would you like to play with Audio? Enter (Y/N): ")
if response.upper() == "Y":
    voice_input = record_voice_input()
    print(f"🎤 Voice Input: {voice_input}")
