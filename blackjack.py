import socket
from ctypes import *

libc = CDLL("libc.so.6")
libc.srand(97*2**24 + 97*2**16 + 97*2**8 + 97)


def clean_cards(line):
  return line.split(":")[-1].strip().split(" ")


def decide(player_worth):
  if player_worth < 18:
    s.send("H\n")
    player_hand.append(libc.rand() % 13 + 1)
    print_hand("player", player_hand)
  else:
    s.send("S\n")


def parse_cash(line):
  return int(line.split("$")[-1])


def pretty_print_card(card):
  if card == 1:
    return "A"
  elif card == 0xB:
    return "J"
  elif card == 0xC:
    return "Q"
  elif card == 0xD:
    return "K"
  else:
    return str(card)


def print_hand(name, hand):
  print ("Predicted hand for %s: %s" %
         (name, map(pretty_print_card, hand)))


s = socket.socket(socket.AF_INET)
s.connect(("blackjack.shallweplayaga.me", 6789))

print s.recv(1024)
s.send("aaaa\n")


cash = parse_cash(s.recv(1024))
bet = 1

# ask for bet
print s.recv(1024)

while True:
  player_hand = []
  dealer_hand = []

  print "I have %d $" % cash

  #make bet
  print "Betting %d $" % bet
  s.send("%d\n" % bet)

  player_hand.append(libc.rand() % 13 + 1)
  dealer_hand.append(libc.rand() % 13 + 1)
  player_hand.append(libc.rand() % 13 + 1)
  dealer_hand.append(libc.rand() % 13 + 1)

  print_hand("player", player_hand)
  print_hand("dealer", dealer_hand)

  # first round get values from dealer too
  cards = s.recv(1024) + s.recv(1024)
  dealer, player, _ = map(clean_cards, cards.split("\n"))
  player_worth = int(player[-1][1:-1])
  player = player[:-1]
  print "Dealer has %s, player has %s worth %d" % (dealer, player, player_worth)
  decide(player_worth)

  while True:
    cards = s.recv(1024) + s.recv(1024)
    if "You" in cards:
      cash = parse_cash(next((line for line in cards.split("\n") if "$" in line), None))
      if "win" in cards:
        print "I won!"
        bet = 1
      elif "draw" in cards:
        print "It's a draw :-/"
      else:
        print "I lost :("
        bet = bet*2
      break

    player = clean_cards(cards.split("\n")[0])
    player_worth = int(player[-1][1:-1])
    player = player[:-1]
    print "player has %s worth %d" % (player, player_worth)
    decide(player_worth)
