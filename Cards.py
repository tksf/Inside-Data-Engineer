#!/usr/bin/python

import random
import time

class Card(object):

    # Playing card class
    
    # Attributes:
    #   suit: list of suits
    #   rank: dictionary of cards and their values
    

    suit = ["Clubs", "Diamonds", "Hearts", "Spades"]

    rank = {
        "A" : 1,
        "2" : 2,
        "3" : 3,
        "4" : 4,
        "5" : 5,
        "6" : 6,
        "7" : 7,
        "8" : 8,
        "9" : 9,
        "10" : 10,
        "J" : 10,
        "Q" : 10,
        "K" : 10       
    }


    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        # Readable string repsentation of the card
        return '\t%s of %s' % (self.rank,  Card.suit[self.suit])



class Deck(object):
    # Deck of cards.

    # Attributes:
    #   cards: list of card objects

    
    def __init__(self):
        self.cards = []

        for suit in range(4):
            for rank in Card.rank.keys():
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        # Readable string repsentation of the whole dec

        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

    def add_card(self, card):
        self.cards.append(card)

    def pop_card(self, i=-1):
        return self.cards.pop()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_cards(self, hand, num, verbose = 0):
        #  Draw cards from the deck

        # hand: Hand object to move the cards to
        # num: how many cards
        # verbose: print out the card drawn
        
        for i in range(num):
            card = self.pop_card()
            if ( verbose ):
                print "Drew: ", card
                time.sleep(1)
            hand.add_card(card)




if __name__ == '__main__':
  main()


