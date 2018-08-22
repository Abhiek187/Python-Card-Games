"""Go Fish in Python"""
import random

SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen',
         'King', 'Ace')
playing = True


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
        self.deck = []

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
    """Dictionary of cards the player is currently holding"""
    def __init__(self):
        # Assign all card ranks to 0
        self.cards = dict.fromkeys((rank for rank in RANKS), 0)
        self.books = 0

    def __str__(self):
        res = "You have:\n"

        for key, value in self.cards.items():
            if value in range(1, 4):
                res += f"{value} {key}"

                if value > 1:
                    res += "s"

                res += "\n"

        return res

    def add_card(self, card, turn):
        """Add card to hand
        :param card
        :param turn"""
        self.cards[card.rank] += 1
        self.check_for_books(card.rank, turn)

    def check_for_books(self, rank, turn):
        """Check if there are 4 of a card
        :param rank
        :param turn"""
        if self.cards[rank] == 4:
            if turn:
                res = f"You got a book of {rank}"
                if rank == "Six":
                    res += "e"
                print(res + "s!")
            else:
                res = f"Your opponent got a book of {rank}"
                if rank == "Six":
                    res += "e"
                print(res + "s!")

            self.books += 1

    def has_card(self, rank):
        """Check if player has the card in their hand
        :param rank
        :return True or False"""
        return self.cards[rank] > 0


def ask_opponent(player, opponent, deck):
    """See if opponent has the card desired
    :param player
    :param opponent
    :param deck
    :return True or False"""
    while True:
        request = input("Which card would you like? ").capitalize()

        if request not in player.cards.keys():
            print("That's not a valid card.")
        elif player.cards[request] not in range(1, 4):
            print("You must choose from your own hand.")
        else:
            break

    if opponent.has_card(request):
        resp = f"You got {opponent.cards[request]} {request}"
        if opponent.cards[request] > 1:
            if request == "Six":
                resp += "e"
            resp += "s"
        print(resp + " from your opponent.")
        player.cards[request] += opponent.cards[request]
        player.check_for_books(request, True)
        opponent.cards[request] = 0
        return True

    print("Go fish!")
    next_card = deck.deal()
    player.add_card(next_card, True)
    if next_card.rank == request:
        print("You got the same card you asked for. Go again!")
        return True

    return False


def ask_player(player, opponent, deck):
    """See if player has the card desired
    :param player
    :param opponent
    :param deck
    :return True or False"""
    possible_cards = [key for key in opponent.cards.keys() if opponent.cards[key] in range(1, 4)]
    rand_index = random.randint(0, len(possible_cards) - 1)
    request = possible_cards[rand_index]
    res = f"Do you have any {request}"
    if request == "Six":
        res += "e"
    print(res + "s?")

    if player.has_card(request):
        resp = f"You gave {player.cards[request]} {request}"
        if player.cards[request] > 1:
            if request == "Six":
                resp += "e"
            resp += "s"
        print(resp + " to your opponent.")
        opponent.cards[request] += player.cards[request]
        opponent.check_for_books(request, False)
        player.cards[request] = 0
        return False

    print("Go fish!")
    next_card = deck.deal()
    opponent.add_card(next_card, False)
    if next_card.rank == request:
        print("Your opponent got the same card he asked for. He goes again.")
        return False

    return True


def play_again():
    """Ask if player wants to play again
    :return True or False"""
    while True:
        response = input("Do you want to play again (y/n)? ").lower()

        if response not in ("y", "n"):
            print("Please enter y or n")
        else:
            return response == "y"


while playing:
    # Introduce the game
    print("Welcome to Go Fish!")
    # Create the deck, shuffle, and deal 7 cards to each player
    game_deck = Deck()
    game_deck.shuffle()
    player_hand = Hand()
    opponent_hand = Hand()

    for i in range(0, 7):
        player_hand.add_card(game_deck.deal(), True)
        opponent_hand.add_card(game_deck.deal(), False)

    # Keep track of whose turn it is
    player_turn = True
    # Keep playing until all books are made
    while True:
        if player_turn:
            # Show player's cards
            print(player_hand)
            # Ask for one of opponent's cards
            player_turn = ask_opponent(player_hand, opponent_hand, game_deck)
            # If player runs out of cards, grab one from the deck, else end the game
            player_cards = [key for key in player_hand.cards.keys()
                            if player_hand.cards[key] in range(1, 4)]
            if not player_cards and game_deck.deck:
                player_hand.add_card(game_deck.deal(), player_turn)
            elif not game_deck.deck:
                break
        else:
            # Have opponent ask for card
            player_turn = ask_player(player_hand, opponent_hand, game_deck)
            # If opponent runs out of cards, grab one from the deck, else end the game
            opponent_cards = [key for key in opponent_hand.cards.keys()
                              if opponent_hand.cards[key] in range(1, 4)]
            if not opponent_cards and game_deck.deck:
                opponent_hand.add_card(game_deck.deal(), player_turn)
            elif not game_deck.deck:
                break

    # Compare books of both players
    print(f"The deck is empty. You have {player_hand.books} book(s) "
          + f"and your opponent has {opponent_hand.books} book(s).")
    if player_hand.books > opponent_hand.books:
        print("You win!")
    else:
        print("You lose.")

    # Ask if player wants to play again
    playing = play_again()
