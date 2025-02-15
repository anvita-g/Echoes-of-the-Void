def trade_with_aliens(player):
    print("\n👾 Alien Merchant: 'Trade? You give food, I give map!'")

    choices = {
        "1": ("Give food (-10%)", "Receive map clue", "maps"),
        "2": ("Give old ship parts", "Receive food (+10%)", "food"),
        "3": ("Leave without trading", None, None)
    }

    for key, (offer, receive, _) in choices.items():
        print(f"{key}. {offer} -> {receive}")

    choice = input("\n> Choose trade option (1-3): ").strip()
    if choice in choices and choices[choice][2]:
        item = choices[choice][2]
        if item == "maps":
            player.inventory["maps"] += 1
        elif item == "food":
            player.health += 10

        print(f"✅ TRADE SUCCESSFUL! You received {choices[choice][1]}")
    else:
        print("👾 The alien grumbles and leaves.")

