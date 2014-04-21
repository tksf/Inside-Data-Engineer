#!/usr/bin/python

import os
import time

from Cards import *

class Hand(Deck):
        # Hand of cards, inherits from Deck object
        #
        # Attributes:
        #   cards: list of card objects
        #   label: string to indicate which player (Dealer or Player in our case)
    
    def __init__(self, label=''):
        self.cards = []
        self.label = label

    def __str__(self):
        # human readbale string of the current hands
        res = []

        res.append('----------------------')
        res.append(self.label)
        res.append(super(Hand, self).__str__())

        value = self.count_hand()
        if ( value == -1 ):
            res.append('\tBusted')
        else:
            res.append('Value:  ' + str(value))

        return '\n'.join(res)

    def count_hand(self):
        # return the blackjack version of the value for the hand
        # returns -1 for chand that is over 21

        # has to logic to deal with Aces (can be counted either as 1 or 11)

        value = 0
        how_many_aces = 0

        for card in self.cards:
            if ( card.rank == 'A' ):
                # got an ace
                how_many_aces += 1
            else:
                value += Card.rank[card.rank]

        if ( how_many_aces > 0 ):
            if ( value > 10 ):
                # must count all aces as ones in order to avoid busting
                value +=  how_many_aces
            else:
                while ( how_many_aces > 0 ):
                    how_many_aces -= 1

                    if ( (value + 11) > 21 ):
                        value += 1
                    else:
                        value += 11
        if value > 21:
            return -1
        else:
            return value


class Dealers_shoe(Deck):
    # Deal shoe calss
    # in casinos, dealears have multiple dacks shuffeld togeter and hold in
    # machine called dealer shoe (or dealing machine)

    # inherit from Deck but use 5 decks of cards instead
   
    def __init__(self):

        self.cards = []
        deck_count = 5
        count = 0

        # instantiate each of the five deack and each of the suits and each of the cards
        while ( count < deck_count ):
            for suit in range(4):
                for rank in Card.rank.keys():
                    card = Card(suit, rank)
                    self.cards.append(card)
            count += 1



class Blackjack_game(object):

    # The Game itself. Will run deals until player runs out of chips or quits
    #   
    #
    # Attributes:
    #   game_chip_count: how many chips are left for the player, start with default of 100
    #   deck: the dealer shoe that has n decks of cuards (currently using 5 decks)
    #

    def __init__(self, chips=100):
        self.game_chip_count = chips
        self.deck = Dealers_shoe()
        self.deck.shuffle()
        

    def win(self, bet):
        self.game_chip_count += bet

    def loose(self, bet):
        self.game_chip_count -= bet

    def chip_count(self):
        return self.game_chip_count

    def run_game(self):

        while ( self.game_chip_count > 0 ):

            result = 0

            deal = Deal(self.deck)  
            bet_size = deal.get_bet(self.game_chip_count)

            result = deal.run_deal()

            self.game_chip_count += result
            raw_input("Press any key to continue...")

        print "Thanks for playing, that was fun!"


class Deal(object):

    # One deal in the game
    #
    # Attributes:
    #   bet: how many chips users ets for this hand
    #   deck: the deck where cards are drawn from
    #   player_hand: player's hand of cards
    #   dealer_hand: dealer's hand of cards   
    #

    def __init__(self, deck):
        self.bet = 0
        self.deck = deck

        self.player_hand = Hand("Player")
        self.dealer_hand = Hand("Dealer") 

        self.deck.draw_cards(self.player_hand, 2)
        self.deck.draw_cards(self.dealer_hand, 1)

    def __str__(self):
        # human readbale string of the current deals
        res = []

        bet_string = "Bet for the hand %s:" % self.bet
        res.append(bet_string)
        res.append(str(self.dealer_hand))
        res.append(str(self.player_hand))

        return '\n'.join(res)


    def get_bet(self, max_chips = 0):
        # get user's input for how many chips to bet
        # returns the size of the bet

        bet_size = -1

        while ( bet_size < 0 or bet_size > max_chips ):

            os.system('clear')
            print "You have %s chips to use." % max_chips

            try:
                bet_size = raw_input('How much would you like to bet (use 0 to exit)? ')
                bet_size = int(bet_size)
            except:
                print 'Not cool'

        self.bet = bet_size
        if ( bet_size == 0 ):
             exit(0)

        return(bet_size)


    def run_deal(self):
        # maun logic for running the deal

        play = 1
        dealer_play = 1

        while play == 1:

            user_action = ''

            os.system('clear')
            print self
            print('----------------------')

            try: 
                user_action = raw_input('Choose [Hh]it, [Ss]tand or [Qq]uit: ')
            except:
                print 'Not cool'

            if ( user_action == 'h' or user_action == 'H' ):

                self.deck.draw_cards(self.player_hand, 1, 1)

                if ( self.player_hand.count_hand() == -1 ):
                    print 'Player bust!'
                    time.sleep(1)

                    return(-self.bet)

            elif ( user_action == 'q' or user_action == 'Q' ):
                exit()
            elif ( user_action == 's' or user_action == 'S' ):
                play = 0


        # done with user choises, next is dealer

        print("Dealer turn")
        while dealer_play:

            os.system('clear')
            print self

            dealer_count = self.dealer_hand.count_hand()
            player_count = self.player_hand.count_hand()

            if (dealer_count < 0 ):
                # dealer is busted
                print 'Dealer busted, you won the hand'
                dealer_play = 0
                time.sleep(1)
                return(self.bet)

            elif ( dealer_count > player_count ):
                # dealer won the game
                print 'Dealer won the hand'
                time.sleep(1)
                return(-self.bet)

            elif ( dealer_count < 17 or dealer_count < player_count ):

                # get dealer more cards
                self.deck.draw_cards(self.dealer_hand, 1, 1)
                print self.dealer_hand

            elif ( dealer_count == player_count and dealer_count >= 17 ):
                print 'Draw'
                time.sleep(1)
                return(0)


        os.system('clear')
        print self
        raw_input("Press any key to continue...")



def main ():

    # main to start the game and ask for new one if user looses a game

    play = 1
    
    while ( play == 1 ):

        game = Blackjack_game(100)
        game.run_game()

        try:
            choice = raw_input('[Yy]es for another game?: ')
        except:
            print 'Not cool'

        if ( choice == 'Y' or choice == 'y' ):
            play = 1
        else:
            play = 0



if __name__ == '__main__':
  main()

