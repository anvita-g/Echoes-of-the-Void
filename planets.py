import subprocess
import random
import torch
import os
import whisper
import pyaudio
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

OLLAMA_PATH = "C:\\Users\\Anvita\\AppData\\Local\\Programs\\Ollama\\ollama.exe"
MODEL = "mistral"

PLANET_TYPES = ["Jungle", "Desert", "Frozen", "Toxic", "Volcanic", "Oceanic"]
PLANET_IMAGES_PATH = "images/"

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
whisper_model = whisper.load_model("base")

llm = OllamaLLM(model="mistral")
hint_prompt = PromptTemplate(input_variables=["planet_type"], template="Generate three short survival tips for a {planet_type} planet.")
hint_chain = hint_prompt | llm

def generate_hint_with_langchain(planet_type):
    hints = hint_chain.invoke({"planet_type": planet_type}).strip()
    return hints.split("\n")[:3]

def generate_planet():
    planet_name = f"Planet-{random.randint(100, 999)}"
    planet_type = random.choice(PLANET_TYPES)
    prompt = f"Describe a {planet_type.lower()} planet in one sentence for a sci-fi survival game, including a hint of what resources or hazards await."
    try:
        process = subprocess.Popen(
            [OLLAMA_PATH, "run", MODEL, prompt.strip()],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8"
        )
        description = "".join(line.strip() + " " for line in process.stdout).strip()
        process.wait()
        if process.returncode != 0 or not description:
            description = f"A mysterious {planet_type.lower()} planet (AI error)."
    except Exception:
        description = f"A mysterious {planet_type.lower()} planet (AI call failed)."
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
        return processor.decode(out[0], skip_special_tokens=True)
    except Exception:
        return "No caption available."

def record_voice_input():
    print("🎤 Listening for voice input...")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    frames = [stream.read(1024) for _ in range(0, int(16000 / 1024 * 5))]
    stream.stop_stream()
    stream.close()
    p.terminate()
    with open("temp.wav", "wb") as f:
        f.write(b''.join(frames))
    return whisper_model.transcribe("temp.wav")['text']

def explore_planet(planet, player):
    print(f"\n🛬 Landing on {planet['name']}...")
    print(f"🌍 Planet Type: {planet['type']} - {planet['desc']}")
    image_filename = f"{planet['type'].lower()}.jpg"
    image_path = os.path.join(PLANET_IMAGES_PATH, image_filename)
    if os.path.exists(image_path):
        caption = generate_image_caption(image_path)
        print(f"🖼️ Planet Image Caption: {caption}")
        Image.open(image_path).show()
    else:
        print("⚠️ No image found for this planet type.")
    hints = generate_hint_with_langchain(planet["type"])
    print(f"💡 Survival Tips: {hints[0]} | {hints[1]} | {hints[2]}")
    if planet["hazard"] != "None":
        print(f"⚠️ HAZARD: {planet['hazard']} - You lose health!")
        player.update_health(-random.randint(5, 15))
    if planet["type"] == "Frozen":
        print("❄️ The cold is harsh. Your health takes a hit!")
        player.update_health(-random.randint(5, 15))
        if random.random() < 0.4:
            print("🌿 You discover a medicinal plant! Your health improves.")
            player.update_health(random.randint(10, 20))
    elif planet["type"] == "Desert":
        print("🌵 The desert is unforgiving. You risk dehydration!")
        player.update_health(-random.randint(5, 10))
        if random.random() < 0.5:
            print("👽 You encounter a merchant! Bartering for food.")
            player.barter_for_food(random.randint(1, 3))
    elif planet["type"] == "Jungle":
        print("🌿 The jungle is dense and dangerous. Watch your step!")
        if random.random() < 0.3:
            print("🗺️ You find an ancient ruin with clues that could help you.")
            player.update_health(random.randint(5, 15))
    elif planet["type"] == "Toxic":
        print("☣️ The air is filled with toxins! Your health is slowly draining.")
        player.update_health(-random.randint(5, 10))
        if random.random() < 0.4:
            print("💎 You find rare metals to improve your ship!")
            player.update_ship_build(random.randint(10, 20))
    elif planet["type"] == "Volcanic":
        print("🌋 The volcanic activity is intense! Be careful.")
        if random.random() < 0.3:
            print("⚡ You find geothermal energy sources that could power your ship.")
            player.update_ship_energy(random.randint(10, 20))
    elif planet["type"] == "Oceanic":
        print("🌊 The oceans are vast, but dangerous currents lurk.")
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

def show_help():
    print("\n=== HELP MENU ===")
    print("Commands:")
    print("- Type 'exit' anytime to quit.")
    print("- Type 'help' to see this menu.")
    print("- Type 'play' to start the game.")
    print("- Explore planets, manage resources, and survive!")
    print("=================\n")

while True:
    command = input("\n> Enter a command (Type 'help' for instructions or 'play' to continue): ").strip().lower()
    if command == "play":
        print("Starting game. Safe travels, Captain!")
        break
    elif command == "help":
        show_help()
    elif command == "exit":
        print("Exiting game. See you next time, Captain!")
        exit()
    else:
        response = input("Would you like to play with Audio? Enter (Y/N): ")
        if response.upper() == "Y":
            voice_input = record_voice_input()
            print(f"🎤 Voice Input: {voice_input}")
