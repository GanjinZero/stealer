from hand import pfIndexToPocket, pfPocketToIndex, ranks
import json


def change_hand_order(hand):
    """
    Clean the hand in right order.
    9Ts -> T9s
    """
    if len(hand) == 2:
        return hand
    if ranks[hand[0]] < ranks[hand[1]]:
        return (hand[1] + hand[0] + hand[2])
    return hand

def is_pair(hand):
    if len(hand) == 2:
        return True
    return False

def is_suited(hand):
    if len(hand) == 3:
        if hand[-1] == 's':
            return True
    return False

def is_offsuited(hand):
    if is_pair(hand) or is_suited(hand):
        return False
    if len(hand) == 3:
        return True
    return False # For empty hand

def hand_vs_hand(hand1, hand2):
    hand1_use = change_hand_order(hand1)
    hand2_use = change_hand_order(hand2)
    file = open("..\\hands\\" + hand1_use + ".json", 'r', encoding='utf-8')
    hand_eval_dict = json.load(file)
    use_str = hand1_use + "-" + hand2_use
    return hand_eval_dict[use_str]

def combinator_count(hand="", hand_list=[]):
    count = []
    for hand_v in hand_list:
        if hand == "":
            if is_pair(hand_v):
                count += [6]
            if is_suited(hand_v):
                count += [4]
            if is_offsuited(hand_v):
                count += [12]
        if is_pair(hand):
            blocker = hand[0]
            if is_pair(hand_v):
                if hand_v[0] == blocker:
                    count += [1]
                else:
                    count += [6]
            if is_suited(hand_v):
                if hand_v[0] == blocker or hand_v[1] == blocker:
                    count += [2]
                else:
                    count += [4]
            if is_offsuited(hand_v):
                if hand_v[0] == blocker or hand_v[1] == blocker:
                    count += [6]
                else:
                    count += [12]
        if is_suited(hand):
            blocker_0 = hand[0]
            blocker_1 = hand[1]
            if is_pair(hand_v):
                if hand_v[0] == blocker_0 or hand_v[0] == blocker_1:
                    count += [3]
                else:
                    count += [6]
            if is_suited(hand_v):
                repeat_count = 4 - len(set([blocker_0, blocker_1, hand_v[0], hand_v[1]]))
                if repeat_count == 0: # A3s vs 45s
                    count += [4]
                else:
                    count += [3]
            if is_offsuited(hand_v):
                repeat_count = 4 - len(set([blocker_0, blocker_1, hand_v[0], hand_v[1]]))
                if repeat_count == 2: # A3s vs A3o
                    count += [6]
                if repeat_count == 1: # A3s vs 34o
                    count += [9]
                if repeat_count == 0:
                    count += [12]
        if is_offsuited(hand):
            blocker_0 = hand[0]
            blocker_1 = hand[1]
            if is_pair(hand_v):
                if hand_v[0] == blocker_0 or hand_v[0] == blocker_1:
                    count += [3]
                else:
                    count += [6]
            if is_suited(hand_v):
                repeat_count = 4 - len(set([blocker_0, blocker_1, hand_v[0], hand_v[1]]))
                if repeat_count == 0: # A3o vs 45s
                    count += [4]
                if repeat_count == 1: # A3o vs 34s
                    count += [3]
                if repeat_count == 2: # A3o vs A3s
                    count += [2]
            if is_offsuited(hand_v):
                repeat_count = 4 - len(set([blocker_0, blocker_1, hand_v[0], hand_v[1]]))
                if repeat_count == 2: # A3o vs A3o
                    count += [7]
                if repeat_count == 1: # A3o vs 34o
                    count += [9]
                if repeat_count == 0:
                    count += [12]
    return count

def hand_vs_comb(hand, hand_list):
    count = combinator_count(hand, hand_list)
    percent = 0
    for i in range(len(hand_list)):
        hand_v = hand_list[i]
        percent += count[i] * hand_vs_hand(hand, hand_v)
    return percent / sum(count)

if __name__ == "__main__":
    hand_vs_hand("AA", "AKo")
    hand_vs_comb("QQ", ["AA", "AKs", "KK", "QQ"])