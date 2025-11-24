#!/usr/bin/env python3
"""
Homeless Guy Survival Simulator
You are a homeless person on the streets. Survive is the key!
"""

import random
import sys


class HomelessGuy:
    """The player character - a homeless person trying to survive."""
    
    def __init__(self):
        self.health = 100
        self.hunger = 50  # 0 = starving, 100 = full
        self.energy = 75
        self.money = 0.50  # Start with 50 cents
        self.warmth = 50  # 0 = freezing, 100 = warm
        self.day = 1
        self.has_shelter = False
        self.inventory = []
        
    def is_alive(self):
        """Check if the player is still alive."""
        return self.health > 0
    
    def get_status(self):
        """Return the current status of the player."""
        shelter_status = "Yes" if self.has_shelter else "No"
        items = ", ".join(self.inventory) if self.inventory else "Nothing"
        return f"""
╔══════════════════════════════════════════╗
║          DAY {self.day} - STATUS                 
╠══════════════════════════════════════════╣
║  Health:  {self.health:3d}/100  {'█' * (self.health // 10)}{'░' * (10 - self.health // 10)}
║  Hunger:  {self.hunger:3d}/100  {'█' * (self.hunger // 10)}{'░' * (10 - self.hunger // 10)}
║  Energy:  {self.energy:3d}/100  {'█' * (self.energy // 10)}{'░' * (10 - self.energy // 10)}
║  Warmth:  {self.warmth:3d}/100  {'█' * (self.warmth // 10)}{'░' * (10 - self.warmth // 10)}
║  Money:   ${self.money:.2f}
║  Shelter: {shelter_status}
║  Items:   {items}
╚══════════════════════════════════════════╝
"""


class SurvivalGame:
    """Main game engine for the homeless survival simulator."""
    
    def __init__(self):
        self.player = HomelessGuy()
        self.game_over = False
        self.weather = "cloudy"
        self.time_of_day = "morning"
        
    def intro(self):
        """Display the game introduction."""
        print("""
╔══════════════════════════════════════════════════════════════╗
║     HOMELESS GUY SURVIVAL SIMULATOR                          ║
║     You are a homeless person on the streets.                ║
║     SURVIVE IS THE KEY!                                      ║
╚══════════════════════════════════════════════════════════════╝

You wake up on a cold park bench with nothing but the clothes 
on your back and a few coins in your pocket.

The streets are unforgiving. You must find food, shelter, and 
money to survive. Make wise choices - every decision matters.

Your goal: Survive for 30 days and save enough money ($100) 
to get back on your feet.

Good luck out there...
""")
        
    def get_actions(self):
        """Return available actions for the player."""
        actions = {
            "1": ("Beg for money", self.action_beg),
            "2": ("Search for food", self.action_search_food),
            "3": ("Find shelter", self.action_find_shelter),
            "4": ("Rest", self.action_rest),
            "5": ("Do odd jobs", self.action_odd_jobs),
            "6": ("Collect cans/bottles", self.action_collect_recyclables),
            "7": ("Check status", self.action_check_status),
            "8": ("End day", self.action_end_day),
            "9": ("Quit game", self.action_quit),
        }
        return actions
    
    def display_actions(self):
        """Display available actions to the player."""
        print("\n┌─────────────────────────────────────┐")
        print("│ What would you like to do?          │")
        print("├─────────────────────────────────────┤")
        actions = self.get_actions()
        for key, (name, _) in actions.items():
            print(f"│ {key}. {name:32s} │")
        print("└─────────────────────────────────────┘")
        
    def action_beg(self):
        """Beg for money from passersby."""
        self.player.energy -= 10
        
        outcomes = [
            (0.4, 0, "People walk by ignoring you."),
            (0.25, 0.25, "A kind stranger gives you a quarter."),
            (0.15, 0.50, "Someone hands you 50 cents."),
            (0.10, 1.00, "A generous person gives you a dollar!"),
            (0.05, 5.00, "A wealthy person feels generous - $5!"),
            (0.05, -0.25, "Someone steals some of your coins!"),
        ]
        
        roll = random.random()
        cumulative = 0
        for prob, money, message in outcomes:
            cumulative += prob
            if roll <= cumulative:
                self.player.money = max(0, self.player.money + money)
                print(f"\n{message}")
                if money > 0:
                    print(f"You now have ${self.player.money:.2f}")
                break
                
    def action_search_food(self):
        """Search for food in dumpsters and around the city."""
        self.player.energy -= 15
        
        outcomes = [
            (0.3, 0, "You find nothing edible.", -5),
            (0.25, 15, "You find some stale bread.", 0),
            (0.2, 25, "You find leftover restaurant food!", 0),
            (0.1, 35, "You hit the jackpot - fresh food from a food bank!", 5),
            (0.1, 0, "You eat something bad and feel sick.", -15),
            (0.05, 50, "A restaurant gives you a full meal!", 10),
        ]
        
        roll = random.random()
        cumulative = 0
        for prob, food, message, health_change in outcomes:
            cumulative += prob
            if roll <= cumulative:
                self.player.hunger = min(100, self.player.hunger + food)
                self.player.health = max(0, min(100, self.player.health + health_change))
                print(f"\n{message}")
                break
                
    def action_find_shelter(self):
        """Try to find a place to sleep for the night."""
        self.player.energy -= 10
        
        if self.player.has_shelter:
            print("\nYou already have shelter for tonight.")
            return
            
        outcomes = [
            (0.4, True, "You find a dry spot under a bridge.", 10),
            (0.25, True, "An abandoned building provides cover.", 15),
            (0.15, True, "A homeless shelter has space!", 25),
            (0.15, False, "No luck finding shelter tonight.", 0),
            (0.05, True, "A church opens its doors to you.", 30),
        ]
        
        roll = random.random()
        cumulative = 0
        for prob, found, message, warmth_bonus in outcomes:
            cumulative += prob
            if roll <= cumulative:
                self.player.has_shelter = found
                self.player.warmth = min(100, self.player.warmth + warmth_bonus)
                print(f"\n{message}")
                break
                
    def action_rest(self):
        """Rest and recover energy."""
        energy_gain = 20 if self.player.has_shelter else 10
        warmth_change = 5 if self.player.has_shelter else -10
        
        self.player.energy = min(100, self.player.energy + energy_gain)
        self.player.warmth = max(0, min(100, self.player.warmth + warmth_change))
        self.player.hunger = max(0, self.player.hunger - 5)
        
        if self.player.has_shelter:
            print("\nYou rest comfortably in your shelter.")
        else:
            print("\nYou rest on a cold bench. It's not great but it helps.")
            
    def action_odd_jobs(self):
        """Try to find small jobs for money."""
        self.player.energy -= 25
        self.player.hunger -= 10
        
        if self.player.energy < 30:
            print("\nYou're too tired to work. Rest first.")
            self.player.energy += 25
            self.player.hunger += 10
            return
            
        outcomes = [
            (0.35, 0, "No one needs help today."),
            (0.25, 3.00, "You help unload a truck - $3!"),
            (0.20, 5.00, "You wash some cars - $5!"),
            (0.10, 10.00, "You help a shop owner all day - $10!"),
            (0.10, 2.00, "You hold a sign for a business - $2."),
        ]
        
        roll = random.random()
        cumulative = 0
        for prob, money, message in outcomes:
            cumulative += prob
            if roll <= cumulative:
                self.player.money += money
                print(f"\n{message}")
                if money > 0:
                    print(f"You now have ${self.player.money:.2f}")
                break
                
    def action_collect_recyclables(self):
        """Collect cans and bottles to recycle for money."""
        self.player.energy -= 20
        
        outcomes = [
            (0.3, 0.50, "You find a few cans - 50 cents."),
            (0.3, 1.00, "A decent haul of bottles - $1!"),
            (0.2, 2.00, "Great finds today - $2!"),
            (0.15, 0.25, "Slim pickings, only 25 cents."),
            (0.05, 5.00, "Someone threw out a bag of cans - $5!"),
        ]
        
        roll = random.random()
        cumulative = 0
        for prob, money, message in outcomes:
            cumulative += prob
            if roll <= cumulative:
                self.player.money += money
                print(f"\n{message}")
                print(f"You now have ${self.player.money:.2f}")
                break
                
    def action_check_status(self):
        """Display current player status."""
        print(self.player.get_status())
        
    def action_end_day(self):
        """End the current day and move to the next."""
        print(f"\n{'='*45}")
        print(f"  Day {self.player.day} comes to an end...")
        print(f"{'='*45}")
        
        # Night effects
        if not self.player.has_shelter:
            cold_damage = random.randint(5, 15)
            self.player.health -= cold_damage
            self.player.warmth = max(0, self.player.warmth - 20)
            print(f"You spent the night in the cold. Lost {cold_damage} health.")
        else:
            self.player.health = min(100, self.player.health + 5)
            print("You slept safely in your shelter.")
            
        # Daily hunger
        self.player.hunger = max(0, self.player.hunger - 15)
        if self.player.hunger <= 0:
            starvation_damage = 10
            self.player.health -= starvation_damage
            print(f"You're starving! Lost {starvation_damage} health.")
            
        # Reset for new day
        self.player.day += 1
        self.player.has_shelter = False
        
        # Random events
        self.random_event()
        
        # Check win/lose conditions
        self.check_game_over()
        
    def random_event(self):
        """Trigger a random event at the start of a new day."""
        events = [
            (0.7, None),  # No event
            (0.1, self.event_police),
            (0.05, self.event_charity),
            (0.05, self.event_theft),
            (0.05, self.event_weather),
            (0.05, self.event_kind_stranger),
        ]
        
        roll = random.random()
        cumulative = 0
        for prob, event in events:
            cumulative += prob
            if roll <= cumulative:
                if event:
                    event()
                break
                
    def event_police(self):
        """Police move you along, costing energy."""
        print("\n[EVENT] Police tell you to move. You lose energy walking away.")
        self.player.energy = max(0, self.player.energy - 15)
        
    def event_charity(self):
        """A charity gives you supplies."""
        print("\n[EVENT] A local charity gives you food and supplies!")
        self.player.hunger = min(100, self.player.hunger + 30)
        self.player.health = min(100, self.player.health + 10)
        
    def event_theft(self):
        """Someone steals some of your money."""
        stolen = min(self.player.money, random.uniform(1, 5))
        self.player.money = max(0, self.player.money - stolen)
        print(f"\n[EVENT] Someone stole ${stolen:.2f} while you were sleeping!")
        
    def event_weather(self):
        """Bad weather affects your warmth and health."""
        print("\n[EVENT] A cold front moves in. It's going to be a tough night.")
        self.player.warmth = max(0, self.player.warmth - 20)
        self.player.health = max(0, self.player.health - 5)
        
    def event_kind_stranger(self):
        """A stranger helps you out."""
        money = random.uniform(5, 20)
        self.player.money += money
        print(f"\n[EVENT] A kind stranger gives you ${money:.2f}!")
        
    def check_game_over(self):
        """Check if the game has ended."""
        if not self.player.is_alive():
            self.game_over = True
            print("\n" + "="*50)
            print("  GAME OVER")
            print("="*50)
            print(f"  You survived {self.player.day - 1} days on the streets.")
            print("  The harsh reality of homelessness claimed another soul.")
            print("="*50)
            return
            
        if self.player.day > 30 and self.player.money >= 100:
            self.game_over = True
            print("\n" + "="*50)
            print("  CONGRATULATIONS! YOU WON!")
            print("="*50)
            print("  You survived 30 days and saved enough money!")
            print(f"  Final savings: ${self.player.money:.2f}")
            print("  You can now afford a room and get back on your feet!")
            print("="*50)
            return
            
        if self.player.day > 30:
            self.game_over = True
            print("\n" + "="*50)
            print("  TIME'S UP")
            print("="*50)
            print("  You survived 30 days but didn't save enough money.")
            print(f"  Final savings: ${self.player.money:.2f}")
            print("  You needed $100 to get back on your feet.")
            print("  The struggle continues...")
            print("="*50)
            return
            
    def action_quit(self):
        """Quit the game."""
        print("\nThanks for playing Homeless Guy Survival Simulator!")
        print("Remember: homelessness is a real issue. Consider helping your local community.")
        self.game_over = True
        
    def play(self):
        """Main game loop."""
        self.intro()
        
        while not self.game_over and self.player.is_alive():
            self.action_check_status()
            self.display_actions()
            
            try:
                choice = input("\nEnter your choice (1-9): ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\nGame interrupted. Goodbye!")
                break
                
            actions = self.get_actions()
            if choice in actions:
                _, action_func = actions[choice]
                action_func()
            else:
                print("\nInvalid choice. Please enter a number 1-9.")
                
            # Check if player died from action
            if not self.player.is_alive():
                self.check_game_over()


def main():
    """Main entry point for the game."""
    game = SurvivalGame()
    game.play()


if __name__ == "__main__":
    main()
