from random import shuffle, randint


def _dummy0(hand):
    return _your_hand(hand)[0] * 5 - 10 + randint(11, 30)


def _dummy1(hand, bet):
    hand = sorted(hand, key=lambda x: int(x[1:]))
    if not str(_your_hand(hand)[0]) in '987653':
        if is_three(hand):
            if list(map(lambda x: int(x[1:]), hand)).count(int(hand[0][1:])) == 3:
                del hand[-2], hand[-1]
            else:
                del hand[0], hand[1]
            hand.extend([deck.pop(0), deck.pop(0)])
        elif is_pair(hand):
            if list(map(lambda x: int(x[1:]), hand)).count(int(hand[0][1:])) == 2:
                del hand[-3], hand[-2], hand[-1]
                hand.extend([deck.pop(0), deck.pop(0), deck.pop(0)])
            elif list(map(lambda x: int(x[1:]), hand)).count(int(hand[4][1:])) == 2:
                del hand[0], hand[1], hand[2]
                hand.extend([deck.pop(0), deck.pop(0), deck.pop(0)])
            else:
                del hand[0], hand[-1]
                hand.extend([deck.pop(0), deck.pop(0)])
        else:

            del hand[randint(0, 4)], hand[randint(0, 3)], hand[randint(0, 2)]
            hand.extend([deck.pop(0), deck.pop(0), deck.pop(0)])

    return [sorted(hand, key=lambda x: int(x[1:])), bet + _your_hand(hand)[0] * 7 - 15 + randint(11, 30)]


def _card_input():
    data = {'J': '11', 'Q': '12', 'K': '13', 'T': '14'}
    print("Enter your cards in the format\033[93m ♥J ♦4 ♥T ♣8 ♠10\033[0m")
    li = input().upper().split()
    for card in li:
        if card[1:] in data.keys():
            li[li.index(card)] = card[0] + data[card[1:]]
    return li

'''
def _card_print(li):
    data = {'11': 'J', '12': 'Q', '13': 'K', '14': 'T'}
    li = sorted(sorted(li, key=lambda x: x[0]), key=lambda x: int(x[1:]))
    for card in li:
        if card[1:] in data.keys():
            li[li.index(card)] = card[0] + data[card[1:]]

    for card in li:
        if card[0] in '♥♦':
            print(f'{"\033[91m"}{card}{"\033[0m"}', end=' ')
        else:
            print(f'{"\033[0m"}{card}{"\033[0m"}', end=' ')
    print()

    data = {'J': '11', 'Q': '12', 'K': '13', 'T': '14'}
    for card in li:
        if card[1:] in data.keys():
            li[li.index(card)] = card[0] + data[card[1:]]
'''

def _your_hand(hand):
    hand_ranks = [
        (is_straight(hand) and is_flush(hand), 9, 'Straight flush'),
        (is_four(hand), 8, 'Four of a kind'),
        (is_full_house(hand), 7, 'Full house'),
        (is_flush(hand), 6, 'Flush'),
        (is_straight(hand), 5, 'Straight'),
        (is_three(hand), 4, 'Three of a kind'),
        (is_two_pair(hand), 3, 'Two pair'),
        (is_pair(hand), 2, 'One pair'),
    ]

    for condition, rank, name in hand_ranks:
        if condition:
            return [rank, name]

    return [1, "High card You're a loser, bro"]


def is_flush(li): #4
    return all(map(lambda x: True if x[0] == li[0][0] else False, li))


def is_straight(li): #5
    li = sorted([int(i[1:]) for i in li])
    return li == list(range(min(li), max(li) + 1))


def is_four(li): #2
    li = [int(i[1:]) for i in li]
    return li.count(li[0]) == 4 or li.count(li[1]) == 4


def is_full_house(li): #3
    li = sorted([int(i[1:]) for i in li])
    return li.count(li[0]) == 3 and li.count(li[-1]) == 2 or li.count(li[0]) == 2 and li.count(li[-1]) == 3


def is_three(li):
    li = sorted([int(i[1:]) for i in li])
    return li.count(li[0]) == 3 or li.count(li[1]) == 3 or li.count(li[2]) == 3

def is_two_pair(li): #7
    li = sorted([int(i[1:]) for i in li])
    cnt = 0
    for i in li:
        if li.count(i) == 2:
            li.remove(i)
            cnt += 1
    return cnt == 2


def is_pair(li): #8
    li = sorted([int(i[1:]) for i in li])
    cnt = 0
    for i in li:
        if li.count(i) == 2:
            li.remove(i)
            cnt += 1
    return cnt == 1


deck = ['♥' + str(i) for i in range(1, 15)] + ['♦' + str(i) for i in range(1, 15)] + ['♣' + str(i) for i in range(1, 15)] + ['♠' + str(i) for i in range(1, 15)]
shuffle(deck)

#cards = _card_input() #♥J ♦J ♥T ♣J ♠J
player, bot0 = [[], 0], [[], 0]
for i in range(5):
    player[0].append(deck.pop(0))
'''
for i in range(5):
    bot0[0].append(deck.pop(0))
'''
bot0 = [['♦9', '♣11', '♥14', '♥8', '♦8'], 0]
bot0 = [sorted(bot0[0], key=lambda x: int(x[1:])), 0]
bot0[1] = _dummy0(bot0[0])
print(bot0, _your_hand(bot0[0]))
bot0 = _dummy1(bot0[0], bot0[1])
print(bot0, _your_hand(bot0[0]))
#_card_print(player[0])
#_card_print(bot0[0])
#_your_hand(player[0])
