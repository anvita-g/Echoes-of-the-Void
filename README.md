# Echoes of the Void

**A sci-fi survival game powered by local AI models. Explore, barter, and survive in the depths of space.** <br>
EECS 449 Extra Credit Assignment

---

## Overview

Echoes of the Void is a command-line survival game where players navigate a mysterious universe in a mission to find Haven-7, exploring generated planets, managing resources, and interacting with alien traders. The game integrates AI models to create dynamic storytelling and strategic decision-making.

## Features

- **Procedurally Generated Planets** – Each planet has unique descriptions, hazards, and survival challenges.
- **AI-Driven Survival Tips** – LangChain generates context-aware survival advice upon landing.
- **Bartering System** – Interact with alien traders to exchange resources.
- **Voice & Text Input** – Play using text commands or voice through Whisper.
- **Dynamic Game Events** – Planet hazards, resource discoveries, and strategic choices impact your survival.

## Gameplay

1. **Start the Game** – Begin your journey and receive three planet options.
2. **Choose a Destination** – Each planet has distinct challenges and potential rewards.
3. **Survive the Landing** – Encounter hazards and adjust your strategy.
4. **Gather Resources** – Find ship parts, food, and maps to improve your chances.
5. **Trade with Aliens** – Barter supplies to gain crucial advantages.
6. **Navigate the Unknown** – Explore until you reach Haven-7 or succumb to the void.

## Technical Details

### AI Integration

- **Ollama** – Runs AI models locally for generating planets and story elements.
- **LangChain** – Manages game logic, interactions, and survival tip generation.
- **Whisper** – Enables voice commands for hands-free gameplay.
- **BLIP** -  Generates captions for image processing.

### Offline Functionality

- **No external API calls** – Everything runs on local models.
- **Local AI processing** – Ensures fast, responsive gameplay.

## Setup & Installation

1. Install and run **Ollama**.
2. Download and configure the **Mistral** and **Whisper** models.
3. Edit **Ollama** path in Planets.py to your path.
4. Run `python game.py` to start playing.

## Game

### Captain's Status
_A live update of your health, ship integrity, fuel, and inventory._
![image](https://github.com/user-attachments/assets/cfc9f53f-8cec-449f-a15a-710cd4a09f44)

### Planet Generation
_Procedurally generated planets with unique environments and survival challenges._
![image](https://github.com/user-attachments/assets/cb1d5e8e-aeca-4078-961e-8e18fa60afd3)


### Alien Barter
_Trade resources with alien merchants to improve your survival chances._
![image](https://github.com/user-attachments/assets/577452c8-242f-4901-b5b5-fbcb4e2f054c)


## Commands

- `help` – Displays gameplay instructions.
- `exit` – Ends the game.
- `play` – Starts the adventure.

## Future Enhancements

- Expanded AI interactions with a conversational assistant.
- More diverse alien encounters and bartering mechanics.
- Additional gameplay events and strategic elements.
