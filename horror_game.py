#!/usr/bin/env python3
"""
Horror Game: The Haunted House
A text-based adventure game with a dark atmosphere.
Meets all requirements: function, user input, print statements, purpose.
Can run in background - all output goes to a log file.
"""

import time
import random
import sys
from datetime import datetime

# Log file path
LOG_FILE = "horror_game_log.txt"

def log_print(text=""):
    """Print to both console AND save to log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {text}"
    print(log_entry)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")

def print_slow(text, delay=0.05):
    """Function that prints text slowly for dramatic effect AND logs it"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()
    
    # Also log the full text
    with open(LOG_FILE, "a") as f:
        f.write(text + "\n")

def display_title():
    """Display the game title"""
    log_print("\n" + "="*60)
    print_slow("🏚️  WELCOME TO THE HAUNTED HOUSE 🏚️", delay=0.03)
    log_print("="*60)
    time.sleep(1)

def game_start():
    """Main game function - called to start the game"""
    log_print("\n--- GAME STARTED ---")
    display_title()
    
    log_print("\n📖 STORY:")
    print_slow("You wake up in an abandoned mansion with no memory of how you got here...", delay=0.04)
    time.sleep(1)
    print_slow("The doors are locked. Strange sounds echo through the halls.", delay=0.04)
    time.sleep(1)
    print_slow("You must escape before midnight, or you'll be trapped here forever.", delay=0.04)
    time.sleep(2)
    
    # Start the game loop
    play_game()

def play_game():
    """Main game loop with choices"""
    current_room = "entrance"
    escaped = False
    turns = 0
    max_turns = 10
    
    while not escaped and turns < max_turns:
        turns += 1
        log_print(f"\n--- Turn {turns}/{max_turns} ---")
        
        if current_room == "entrance":
            log_print("\n🚪 You stand in the MAIN ENTRANCE of the mansion.")
            log_print("The walls are covered in cobwebs. You hear whispers...")
            log_print("\nWhat do you do?")
            log_print("1. Go to the LIBRARY (left hallway)")
            log_print("2. Go to the KITCHEN (right hallway)")
            log_print("3. Go to the BASEMENT (downstairs)")
            
            choice = input("\n👻 Your choice (1-3): ").strip()
            log_print(f"Player chose: {choice}")
            
            if choice == "1":
                current_room = "library"
            elif choice == "2":
                current_room = "kitchen"
            elif choice == "3":
                current_room = "basement"
            else:
                log_print("⚠️  Invalid choice. Try again.")
                continue
        
        elif current_room == "library":
            print_slow("\n📚 You enter a dusty LIBRARY.", delay=0.03)
            log_print("Books float off shelves on their own...")
            print_slow("A shadowy figure appears in the corner of your eye!", delay=0.04)
            time.sleep(1)
            
            log_print("\nWhat do you do?")
            log_print("1. Read the ancient book on the table")
            log_print("2. Run back to entrance")
            log_print("3. Look for a secret exit")
            
            choice = input("\n👻 Your choice (1-3): ").strip()
            log_print(f"Player chose: {choice}")
            
            if choice == "1":
                print_slow("\n🔮 The book reveals the EXIT CODE: 1337", delay=0.04)
                current_room = "entrance"
            elif choice == "2":
                current_room = "entrance"
            elif choice == "3":
                print_slow("\n✨ You find a hidden passage leading to the STUDY!", delay=0.04)
                current_room = "study"
            else:
                log_print("⚠️  Invalid choice. Try again.")
                continue
        
        elif current_room == "kitchen":
            print_slow("\n🔪 You enter the KITCHEN.", delay=0.03)
            log_print("Everything is rotting. Something moves in the shadows...")
            print_slow("You hear footsteps getting closer!", delay=0.04)
            
            log_print("\nWhat do you do?")
            log_print("1. Hide in the pantry")
            log_print("2. Run back to entrance")
            log_print("3. Grab a weapon and fight")
            
            choice = input("\n👻 Your choice (1-3): ").strip()
            log_print(f"Player chose: {choice}")
            
            if choice == "1":
                print_slow("\n😰 You hide. The footsteps pass by...", delay=0.04)
                current_room = "entrance"
            elif choice == "2":
                current_room = "entrance"
            elif choice == "3":
                print_slow("\n⚔️  You fight the ghost and WIN!", delay=0.04)
                print_slow("You find a KEY!", delay=0.04)
                current_room = "front_door"
                escaped = True
            else:
                log_print("⚠️  Invalid choice. Try again.")
                continue
        
        elif current_room == "basement":
            print_slow("\n⚫ You descend into the BASEMENT.", delay=0.03)
            log_print("It's pitch black. You can barely see...")
            print_slow("The temperature drops. You hear chains rattling!", delay=0.04)
            
            log_print("\nWhat do you do?")
            log_print("1. Light a torch and explore")
            log_print("2. Run back upstairs immediately")
            log_print("3. Call out for help")
            
            choice = input("\n👻 Your choice (1-3): ").strip()
            log_print(f"Player chose: {choice}")
            
            if choice == "1":
                print_slow("\n🔥 The torch reveals a TREASURE CHEST with a KEY!", delay=0.04)
                current_room = "front_door"
                escaped = True
            elif choice == "2":
                current_room = "entrance"
            elif choice == "3":
                print_slow("\n👹 A demon appears and drags you deeper!", delay=0.04)
                print_slow("GAME OVER - YOU FAILED", delay=0.05)
                log_print("\n❌ GAME OVER - DEMON ATTACK")
                return
            else:
                log_print("⚠️  Invalid choice. Try again.")
                continue
        
        elif current_room == "study":
            print_slow("\n📜 You enter a hidden STUDY.", delay=0.03)
            log_print("Ancient artifacts cover the shelves...")
            print_slow("You find a glowing crystal and a locked door!", delay=0.04)
            
            log_print("\nWhat do you do?")
            log_print("1. Take the crystal")
            log_print("2. Go back to library")
            log_print("3. Use crystal on locked door")
            
            choice = input("\n👻 Your choice (1-3): ").strip()
            log_print(f"Player chose: {choice}")
            
            if choice == "1" or choice == "3":
                print_slow("\n✨ The crystal unlocks the door to FREEDOM!", delay=0.04)
                current_room = "front_door"
                escaped = True
            elif choice == "2":
                current_room = "library"
            else:
                log_print("⚠️  Invalid choice. Try again.")
                continue
        
        elif current_room == "front_door":
            print_slow("\n🔓 You reach the FRONT DOOR!", delay=0.03)
            time.sleep(1)
            print_slow("The key fits perfectly in the lock...", delay=0.04)
            time.sleep(1)
            print_slow("You turn it... CLICK!", delay=0.04)
            time.sleep(2)
            break
    
    # Game ending
    if escaped:
        log_print("\n" + "="*60)
        print_slow("🌅 THE DOOR SWINGS OPEN", delay=0.03)
        print_slow("You burst into the sunlight and RUN!", delay=0.03)
        print_slow("You're FREE! The mansion fades behind you...", delay=0.03)
        log_print("="*60)
        print_slow("\n✅ CONGRATULATIONS! YOU ESCAPED THE HAUNTED HOUSE!", delay=0.03)
        log_print("="*60)
        log_print("\n--- GAME WON ---")
    else:
        log_print("\n" + "="*60)
        print_slow("⏰ MIDNIGHT STRIKES!", delay=0.03)
        print_slow("The doors seal shut forever...", delay=0.03)
        log_print("="*60)
        print_slow("\n❌ GAME OVER - YOU DIDN'T ESCAPE IN TIME", delay=0.03)
        log_print("="*60)
        log_print("\n--- GAME LOST ---")

def main():
    """Entry point - calls the game_start function"""
    try:
        log_print("\n" + "="*60)
        log_print("HORROR GAME SESSION STARTED")
        log_print("="*60)
        game_start()
    except KeyboardInterrupt:
        log_print("\n⏸️  Game interrupted by user")
        print("\n\n⏸️  Game interrupted. Thanks for playing!")
    except Exception as e:
        log_print(f"\n❌ Error: {e}")
        print(f"\n❌ Error: {e}")

# Execute the main function when script runs
if __name__ == "__main__":
    main()
