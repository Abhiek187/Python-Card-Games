"""Blackjack in Python"""
import random

SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
VALUES = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
chips_count = 100


class Card:
    """Representation of cards"""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    """Deck (list) of cards"""
    def __init__(self):
        self.deck = []  # start with an empty list

        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        res = "["

        for index, card in enumerate(self.deck):
            res += str(card)

            if index < len(self.deck) - 1:
                res += ", "

        return res + "]"

    def shuffle(self):
        """Shuffle the cards"""
        random.shuffle(self.deck)

    def deal(self):
        """Remove card from the top of deck
        :return card"""
        return self.deck.pop()


class Hand:
    """List of cards the player is currently holding"""
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        """Add card to hand
        :param card"""
        self.cards.append(card)
        self.value += VALUES[card.rank]

        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        """Reduce aces to 1 if needed"""
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


class Chips:
    """Chips used to bet"""
    def __init__(self):
        self.total = chips_count  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        """Gain chips from winning a bet"""
        self.total += self.bet

    def lose_bet(self):
        """Lose chips from losing a bet"""
        self.total -= self.bet


def take_bet(chips):
    """Ask player how much they'd like to bet
    :param chips"""
    while True:
        try:
            chips.bet = int(input(f"You have {chips.total} chip(s). How much would you like to bet? "))

            if chips.bet < 0 or chips.bet > chips.total:
                print("You can't bet that much.")
            else:
                break
        except ValueError:
            print("That is not a number.")


def hit(deck, hand):
    """Receive a card from the deck
    :param deck
    :param hand"""
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    """Ask player if they'd like more cards or not
    :param deck
    :param hand"""
    global playing  # to control an upcoming while loop

    while True:
        choice = input("Will you hit or stand? ").lower()

        if choice not in ("hit", "stand"):
            print("Please enter hit or stand.")
        else:
            break

    if choice == "hit":
        hit(deck, hand)
    else:
        playing = False


def show_some(deal):
    """Hide the first card (dealer only)
    :param deal"""
    print("The dealer has these cards:")
    for card in deal.cards[1:]:
        print(card)


def show_all(play, deal=None):
    """Show all cards
    :param play
    :param deal"""
    if deal:
        print("The dealer has these cards:")
        for card in deal.cards:
            print(card)

    print("You have these cards:")
    for card in play.cards:
        print(card)


def player_busts():
    """Player's value exceeds 21"""
    print("Whoops! You busted!")


def player_wins(chips):
    """Player wins chips"""
    print("Congratulations! You win!")
    chips.win_bet()


def dealer_busts():
    """Dealer's value exceeds 21"""
    print("The dealer busted.")


def dealer_wins(chips):
    """Player loses chips"""
    print("The dealer won.")
    chips.lose_bet()


def push():
    """A tie game"""
    print("It's a tie.")


while True:
    # Print an opening statement
    print("Welcome to Blackjack!")
    # Create & shuffle the deck, deal two cards to each player
    game_deck = Deck()
    game_deck.shuffle()
    dealer = Hand()
    player = Hand()

    for i in range(0, 2):
        dealer.add_card(game_deck.deal())
        player.add_card(game_deck.deal())

    # Set up the Player's chips
    player_chips = Chips()
    # Prompt the Player for their bet
    take_bet(player_chips)
    # Show cards (but keep one dealer card hidden)
    show_some(dealer)
    show_all(player)
    playing = True

    while playing:  # recall this variable from our hit_or_stand function
        # Prompt for Player to Hit or Stand
        hit_or_stand(game_deck, player)
        # Show cards (but keep one dealer card hidden)
        show_some(dealer)
        show_all(player)
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            player_busts()
            dealer_wins(player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player.value <= 21:
        while dealer.value < 17:
            dealer.add_card(game_deck.deal())

        # Show all cards
        show_all(player, dealer)
        # Run different winning scenarios
        if dealer.value > 21 or player.value > dealer.value:
            if dealer.value > 21:
                dealer_busts()
            player_wins(player_chips)
        elif player.value < dealer.value:
            dealer_wins(player_chips)
        else:
            push()

    # Inform Player of their chips total
    chips_count = player_chips.total
    print(f"You now have {chips_count} chip(s) in total.")

    if chips_count == 0:
        print("You're broke. You can't play anymore.")
        break
    # Ask to play again
    while True:
        play_again = input("Would you like to play again? (y/n): ").lower()

        if play_again in ('y', 'n'):
            break
        else:
            print("Please enter y or n")

    if play_again == 'n':
        break
