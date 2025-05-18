from random import shuffle, randint
from time import sleep

def _winner_is(hand0, hand1):
    combination = _your_hand(hand0)[0]
    high = []
    if combination in [1, 5, 6, 9]:
        if max(hand0, key=lambda x: int(x[1:])) > max(hand1, key=lambda x: int(x[1:])):
            return 0 #Выигрыш игрока
        elif max(hand0, key=lambda x: int(x[1:])) < max(hand1, key=lambda x: int(x[1:])):
            return 1 #Выигрыш бота
        else:
            return -1 #Ничья

    elif combination in [2, 3]:
        hand0, hand1 = sorted([int(i[1:]) for i in hand0]), sorted([int(i[1:]) for i in hand1])

        for i in hand0:
            if hand0.count(i) == 2 and i not in high:
                high.append(i)
        if len(high) == 2:
            high[0] = max(high)
            del high[1]

        for i in hand1:
            if hand1.count(i) == 2 and i not in high:
                high.append(i)
        if len(high) == 3:
            high[1] = max(high[1:])
            del high[2]

        if high[0] == high[1]:
            return -1
        elif max(high) == high[0]:
            return 0
        else:
            return 1

    elif combination in [4, 7]:
        hand0, hand1 = sorted([int(i[1:]) for i in hand0]), sorted([int(i[1:]) for i in hand1])

        for i in hand0:
            if hand0.count(i) == 3 and i not in high:
                high.append(i)
                break

        for i in hand0:
            if hand0.count(i) == 3 and i not in high:
                high.append(i)
                break

        if max(high) == high[0]:
            return 0
        else:
            return 1

    elif combination == 8:
        hand0, hand1 = sorted([int(i[1:]) for i in hand0]), sorted([int(i[1:]) for i in hand1])

        for i in hand0:
            if hand0.count(i) == 4:
                high.append(i)
                break

        for i in hand0:
            if hand0.count(i) == 4:
                high.append(i)
                break

        if max(high) == high[0]:
            return 0
        else:
            return 1

def _dummy0(hand):
    return _your_hand(hand)[0] * 5 - 10 + randint(11, 30)


def _dummy1(hand, bet, id):
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
                del hand[-2], hand[-1]
            elif list(map(lambda x: int(x[1:]), hand)).count(int(hand[4][1:])) == 2:
                del hand[0], hand[1]
            else:
                del hand[0], hand[-1]
            hand.extend([deck.pop(0), deck.pop(0)])
        else:

            del hand[randint(0, 4)], hand[randint(0, 3)], hand[randint(0, 2)]
            hand.extend([deck.pop(0), deck.pop(0), deck.pop(0)])

    quick_bet = _your_hand(hand)[0] * 7 - 30 + randint(0, 50)
    while bet - quick_bet < 10 or quick_bet < 0:
        quick_bet = _your_hand(hand)[0] * 7 - 30 + randint(0, 50)
    print(f"The bot{id} made a bet of {quick_bet} points")

    return [sorted(hand, key=lambda x: int(x[1:])), bet - quick_bet]


def _card_input():
    data = {'J': '11', 'Q': '12', 'K': '13', 'T': '14'}
    print("Enter your cards in the format\033[93m ♥J ♦4 ♥T ♣8 ♠10\033[0m")
    li = input().upper().split()
    for card in li:
        if card[1:] in data.keys():
            li[li.index(card)] = card[0] + data[card[1:]]
    return li


def _card_print(li):
    data = {'11': 'J', '12': 'Q', '13': 'K', '14': 'T'}
    li = sorted(sorted(li, key=lambda x: x[0]), key=lambda x: int(x[1:]))
    for card in li:
        if card[1:] in data.keys():
            li[li.index(card)] = card[0] + data[card[1:]]

    for card in li:
        if card[0] in '♥♦':
            print(f'\033[91m{card}\033[0m', end=' ')
        else:
            print(f'\033[0m{card}\033[0m', end=' ')
    print()

    data = {'J': '11', 'Q': '12', 'K': '13', 'T': '14'}
    for card in li:
        if card[1:] in data.keys():
            li[li.index(card)] = card[0] + data[card[1:]]


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

    return [1, "High card."]


def is_flush(li):  # 4
    return all(map(lambda x: True if x[0] == li[0][0] else False, li))


def is_straight(li):  # 5
    li = sorted([int(i[1:]) for i in li])
    return li == list(range(min(li), max(li) + 1))


def is_four(li):  # 2
    li = [int(i[1:]) for i in li]
    return li.count(li[0]) == 4 or li.count(li[1]) == 4


def is_full_house(li):  # 3
    li = sorted([int(i[1:]) for i in li])
    return li.count(li[0]) == 3 and li.count(li[-1]) == 2 or li.count(li[0]) == 2 and li.count(li[-1]) == 3


def is_three(li):
    li = sorted([int(i[1:]) for i in li])
    return li.count(li[0]) == 3 or li.count(li[1]) == 3 or li.count(li[2]) == 3


def is_two_pair(li):  # 7
    li = sorted([int(i[1:]) for i in li])
    cnt = 0
    for i in li:
        if li.count(i) == 2:
            li.remove(i)
            cnt += 1
    return cnt == 2


def is_pair(li):  # 8
    li = sorted([int(i[1:]) for i in li])
    cnt = 0
    for i in li:
        if li.count(i) == 2:
            li.remove(i)
            cnt += 1
    return cnt == 1



def __game(pl_bet, bot0_bet, bot1_bet):
    bet = 0
    player, bot0, bot1 = [[], pl_bet], [[], bot0_bet], [[], bot1_bet] #['♦6', '♠11', '♦12', '♠13', '♦14']

    for i in range(5):
        player[0].append(deck.pop(0))

    for i in range(5):
        bot0[0].append(deck.pop(0))

    for i in range(5):
        bot1[0].append(deck.pop(0))

    player[0] = sorted(player[0], key=lambda x: int(x[1:]))
    sleep(0.5)
    print("Here are your cards:")
    sleep(0.5)
    _card_print(player[0])
    sleep(0.5)
    print(*_your_hand(player[0]), sep=' - ')
    sleep(0.5)
    print("Place a bet")

    quick_bet = int(input())
    while player[1] - quick_bet < -1 or quick_bet < 10:
        print(f"The bet must be more than 10 and not exceed your balance({player[1]} points on your balance).")
        quick_bet = int(input())
    player[1] = player[1] - quick_bet
    bet += quick_bet

    quick_bet = _dummy0(bot0[0])
    while bot0[1] - quick_bet < 0:
        quick_bet = _dummy0(bot0[0])
    print(f"the bot0 made a bet of {quick_bet} points")
    bet += quick_bet

    quick_bet = _dummy0(bot1[0])
    while bot1[1] - quick_bet < 0:
        quick_bet = _dummy0(bot1[0])
    print(f"the bot1 made a bet of {quick_bet} points")
    bet += quick_bet

    sleep(0.5)
    print("Total bet:", bet)
    sleep(1)
    print("Select the cards you want to discard (the ID is displayed above them). If you don't want to discard the cards, just press Enter")
    sleep(0.5)
    print(" 1  2  3  4  5")
    _card_print(player[0])

    quick_bet = [input(), True]
    while quick_bet[1]:
        try:
            for i in [player[0][int(i) - 1] for i in quick_bet[0].split()]:
                del player[0][player[0].index(i)]
            quick_bet[1] = False
        except:
            print('Incorrect input. Please enter numbers from 1 to 5 separated by spaces.')
            quick_bet = [input(), True]

    for i in range(5 - len(player[0])):
        player[0].append(deck.pop(0))

    print("Your hand:")
    _card_print(player[0])
    print(*_your_hand(player[0]), sep=' - ')
    sleep(0.5)

    print('Do you want to give up?(y/n)')
    if 'y' in input().lower():
        return player[1], bot0[1], bot1[1]
    sleep(0.5)

    print("Place a bet")
    quick_bet = int(input())
    while player[1] - quick_bet < -1 or quick_bet < 1:
        print(f"The rate must be positive and not exceed your balance({player[1]} points on your balance).")
        quick_bet = int(input())
    player[1] = player[1] - quick_bet
    bet += quick_bet

    quick_bet = bot0[1]
    bot0 = _dummy1(id=0, *bot0)
    bet += quick_bet - bot0[1]

    quick_bet = bot1[1]
    bot1 = _dummy1(id=1, *bot1)
    bet += quick_bet - bot1[1]

    print("Total bet:", bet)
    sleep(0.5)
    print()
    for i in range(10):
        print('\033[95m-\033[0m', end='')
        sleep(0.1)
    print()
    sleep(0.5)

    print('Your cards:')
    sleep(0.25)
    _card_print(player[0])
    sleep(0.25)
    print(*_your_hand(player[0]), sep=' - ')

    sleep(0.5)
    for i in range(10):
        print('\033[93m-\033[0m', end='')
        sleep(0.1)
    print()
    sleep(0.5)

    print("Bot0 cards:")
    sleep(0.25)
    _card_print(bot0[0])
    sleep(0.25)
    print(*_your_hand(bot0[0]), sep=' - ')

    sleep(0.5)
    for i in range(10):
        print('\033[93m-\033[0m', end='')
        sleep(0.1)
    print()
    sleep(0.5)

    print("Bot1 cards:")
    sleep(0.25)
    _card_print(bot1[0])
    sleep(0.25)
    print(*_your_hand(bot1[0]), sep=' - ')

    if _your_hand(player[0])[0] > _your_hand(bot0[0])[0] and _your_hand(player[0])[0] > _your_hand(bot1[0])[0]:
        print('You win!')
        player[1] += bet
    elif _your_hand(player[0])[0] < _your_hand(bot0[0])[0] and _your_hand(bot1[0])[0] < _your_hand(bot0[0])[0]:
        print('You lose!(bot0 win)')
        bot0[1] += bet
    elif _your_hand(player[0])[0] < _your_hand(bot1[0])[0] and _your_hand(bot1[0])[0] > _your_hand(bot0[0])[0]:
        print('You lose!(bot1 win)')
        bot1[1] += bet
    else: #Недостаёт еще одного усл.(в элс)
        if _your_hand(player[0]) == _your_hand(bot0[0]):
            if _winner_is(player[0], bot0[0]) == 0:
                print('You win!')
                player[1] += bet
            elif _winner_is(player[0], bot0[0]) == 1:
                print('You lose!(bot0 win)')
                bot0[1] += bet
            else:
                print('Draw(player and bot0 split the bet)')
                player[1] += bet // 2
                bot0[1] += bet // 2

        elif _your_hand(player[0]) == _your_hand(bot1[0]):
            print(_winner_is(player[0], bot1[0]))
            if _winner_is(player[0], bot1[0]) == 0:
                print('You win!')
                player[1] += bet
            elif _winner_is(player[0], bot1[0]) == 1:
                print('You lose!(bot1 win)')
                bot1[1] += bet
            else:
                print('Draw(player and bot1 split the bet)')
                player[1] += bet // 2
                bot1[1] += bet // 2

        elif _your_hand(bot0[0]) == _your_hand(bot1[0]):
            if _winner_is(bot0[0], bot1[0]) == 0:
                print('You lose!(bot0 win)')
                bot0[1] += bet
            elif _winner_is(bot0[0], bot1[0]) == 1:
                print('You lose!(bot1 win)')
                bot1[1] += bet
            else:
                print('Draw(bot0 and bot1 split the bet)')
                bot0[1] += bet // 2
                bot1[1] += bet // 2


    return player[1], bot0[1], bot1[1]


try:
    print("\033[3mHello player! Welcome to the game \033[93mPoker\033[0m\033[3m! In this game you will play \033[95mclassic poker (Draw Poker)\033[0m\033[3m with a bot.")
    sleep(0.5)
    print("You will be in the game until you lose everything or until you want to stop.")
    sleep(0.5)
    flag = True

    _player_bet, _bot0_bet, _bot1_bet = 100, 99999, 99999
    while flag and _player_bet:
        deck = ['♥' + str(i) for i in range(2, 15)] + ['♦' + str(i) for i in range(2, 15)] + ['♣' + str(i) for i in range(2, 15)] + ['♠' + str(i) for i in range(2, 15)]
        shuffle(deck)
        if _bot0_bet < 1 or _bot1_bet < 1:
            print('Bro... You destroyed our casino. We have no more money.\033[91m GET OUT!!\033[0m')
            break

        _player_bet, _bot0_bet, _bot1_bet = __game(_player_bet, _bot0_bet, _bot1_bet)

        if _player_bet > 0:
            print(f"On your account {_player_bet} points. Again? (y/n)")
            flag = True if 'y' in input().lower() else False
    else:
        if _player_bet:
            print(f"You have {_player_bet} points left. Thanks for playing, come again.")
        else:
            print("Adyos,\033[91m loser♥\033[0m")
except:
    raise Exception("\033[1mWow, you broke everything.")
