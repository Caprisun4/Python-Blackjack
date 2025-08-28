import time
import random

global cards
cards = {
    0: """
 _____
| XXX |
| XXX |
|_____|""",
    1: """
 _____
|     |
|  A  |
|_____|""",
    2: """
 _____
|     |
|  2  |
|_____|""",
    3: """
 _____
|     |
|  3  |
|_____|""",
    4: """
 _____
|     |
|  4  |
|_____|""",
    5: """
 _____
|     |
|  5  |
|_____|""",
    6: """
 _____
|     |
|  6  |
|_____|""",
    7: """
 _____
|     |
|  7  |
|_____|""",
    8: """
 _____
|     |
|  8  |
|_____|""",
    9: """
 _____
|     |
|  9  |
|_____|""",
    10: """
 ______
|      |
|  10  |
|______|""",
    11: """
 _____
|     |
|  J  |
|_____|""",
    12: """
 _____
|     |
|  Q  |
|_____|""",
    13: """
 _____
|     |
|  K  |
|_____|"""}

global slowPrint


def slowPrint(string):
    for char in string:
        print(char, end='')
        time.sleep(0.02)


class Game:
    def __init__(self):
        self.turns = 0

    def intro(self):
        slowPrint("Welcome to blackjack!\n\n")
        choice = 1
        while choice == 1:
            slowPrint("""Please select from -
    1: Play!
    2: Learn the rules.
    3: Quit.\n\n""")

            choice = int(input("Enter your number here:"))

            if (0 < choice < 4):
                if choice == 1:
                    if self.turns == 0: slowPrint("\nYou will start with £500.")
                    Player.play()
                if choice == 2:
                    self.rules()
                elif choice == 3:
                    self.quit()
                pass
            else:
                print("Please enter a number.")

    def rules(self):
        rules = ("""\nRules of blackjack -
    1. You will receive two cards with numerical values that add up.
    2. You may ask for more cards to be handed to you in increments of 1 or can stand. 
    3. You don't want your cards to add up more than 21 or you go 'bust' (lose).
    4. The dealer will also have cards, and if their cards add up to more than yours (but less than 22), you lose.
    5. Dealer will stand on 17 or above.
    6. You may bet money that will double with a win.""")

        slowPrint(rules)
        slowPrint("\nDo you understand? Y/N"
                  "\nEnter:")
        answer = input()
        if answer == "N":
            self.rules()
        elif answer == "Y":
            self.intro()

    def quit(self):
        quit()

    def createHand(self, who):
        card1 = random.randint(1, 13)
        card2 = random.randint(1, 13)

        if card1 > 10:
            who.hand.append([card1, 10])
        elif card1 == 1:
            who.hand.append([card1, 11])
            who.elevenAceAmount += 1
        else:
            who.hand.append([card1, card1])

        if card2 > 10:
            who.hand.append([card2, 10])
        elif card2 == 1:
            who.hand.append([card2, 11])
            who.elevenAceAmount += 1
        else:
            who.hand.append([card2, card2])
        who.total = who.hand[0][1] + who.hand[1][1]

    def createCard(self, who):
        newCard = random.randint(1, 13)
        slowPrint(cards[newCard])

        if newCard > 10:
            who.hand.append([newCard, 10])
        elif newCard == 1:
            who.hand.append([newCard, 11])
            who.elevenAceAmount += 1
        else:
            who.hand.append([newCard, newCard])
        who.total += who.hand[-1][1]
        self.elevenAceCheck(who)

    def elevenAceCheck(self, who):
        if who.elevenAceAmount > 0 and who.total > 21:
            aceNotChanged = True
            pos = 0
            while aceNotChanged:
                if who.hand[pos][1] == 11:
                    who.hand[pos][1] == 1
                    who.total -= 10
                    who.elevenAceAmount -= 1
                    aceNotChanged = False
                pos += 1


    def clear(self):
        Player.hand.clear()
        Dealer.hand.clear()
        Player.total = 0
        Dealer.total = 0
        Player.elevenAceAmount = 0
        Dealer.elevenAceAmount = 0


class Player:
    def __init__(self):
        self.hand = []
        self.total = 0
        self.balance = 500
        self.bet = 0
        self.elevenAceAmount = 0

    def play(self):

        slowPrint("\nEnter how much you would like to bet:")
        self.bet = int(input())
        if self.bet > self.balance:
            slowPrint("\nYou ain't rich enough!")
            self.play()
        elif self.bet < 0:
            slowPrint("\nPlease enter an amount you own.")
            self.play()

        slowPrint("\n\nYOUR HAND:\n")
        Game.createHand(self)
        self.showHand()
        slowPrint(f'\nYour total is: {self.total}')
        Dealer.SetUp()
        self.move()

    def move(self):
        slowPrint("""\nWould you like to -
    1. Hit
    2. Stand
    3. See your hand
    4. Show dealer's hand
    
    Enter:""")
        move = int(input())
        if move == 1:
            self.hit()
        elif move == 2:
            self.stand(False)
        elif move == 3:
            self.showHand()
            self.move()
        elif move == 4:
            Dealer.showDealerHand(False)
            self.move()

    def hit(self):
        Game.createCard(self)

        slowPrint(f"\nNew total is {self.total}\n")
        if self.total > 21:
            slowPrint("\nBUST\n")
            self.stand(True)
        else:
            self.move()


    def stand(self, bustStatus):
        Dealer.showDealerHand(True)

        if Dealer.total < 17 and not (bustStatus):
            Dealer.dealerHit()

        if Dealer.total <= self.total < 22 and Dealer.elevenAceAmount > 0:
            slowPrint("\nYOU WIN!")
            self.balance += self.bet
        elif Dealer.total > 21 and self.total < 22:
            slowPrint("\nYOU WIN!")
            self.balance += self.bet
        else:
            slowPrint("\nYOU LOSE")
            self.balance -= self.bet

        slowPrint(f"\nNew balance is {self.balance}")

        Game.clear()

        slowPrint("\nPlay again? Y/N:")
        again = input()
        if again == "Y":
            self.play()
        else:
            Game.intro()

    def showHand(self):
        for card in self.hand:
            slowPrint("\n" + cards[card[0]])


class Dealer:
    def __init__(self):
        self.card1 = 0
        self.card2 = 0
        self.hand = []
        self.total = 0
        self.elevenAceAmount = 0

    def SetUp(self):
        slowPrint("\n\nDEALER'S CARDS:\n")
        Game.createHand(self)
        self.showDealerHand(False)

    def showDealerHand(self, standBool):

        slowPrint(cards[self.hand[0][0]])
        if standBool:
            slowPrint(cards[self.hand[1][0]] + "\n")
            self.total = self.hand[0][1] + self.hand[1][1]
            slowPrint(f"\n Dealer's total is {self.total}")

        else:
            slowPrint(cards[0] + "\n")

    def dealerHit(self):
        while self.total < 17 and self.total < Player.total:
            Game.createCard(self)
            slowPrint(f"\n Dealer's new total is {self.total}")






Player = Player()
Dealer = Dealer()
Game = Game()
Game.intro()
