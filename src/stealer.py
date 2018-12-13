from game_parameter import small_blind
from hand_eval import hand_vs_comb, combinator_count
from villian import Villian
from sklansky import rank
from math import pow


def hero_3b_fold_4b_ev(hand, three_bet_size, villian, position):
    adjust = 0
    if position == "BB":
        adjust = 1
    if position == "SB":
        adjust = small_blind

    villian_fold_count = sum(combinator_count(hand, villian.f3b_list))
    villian_call_count = sum(combinator_count(hand, villian.f3c_list))
    villian_4b_count = sum(combinator_count(hand, villian.r4b_list))
    count = villian_fold_count + villian_call_count + villian_4b_count
    pot = 1 + small_blind + villian.open_size
    new_pot = 1 + small_blind + three_bet_size * villian.open_size * 2 - adjust
    ev_fold = pot

    if position == "BB":
        people_unaction_count = 0
    if position == "SB":
        people_unaction_count = 1
    if position == "BTN":
        people_unaction_count = 2
    if position == "CO":
        people_unaction_count = 3
    if position == "MP":
        people_unaction_count = 4
    default_cold_4b_range = ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AKo", "AQs"]
    cold_4b_prob = sum(combinator_count(hand, default_cold_4b_range)) / sum(combinator_count(hand, rank))
    cold_4b_total_prob = 1 - pow((1 - cold_4b_prob), people_unaction_count)

    ev_4b = - three_bet_size * villian.open_size + adjust
    ev_call = - three_bet_size * villian.open_size + adjust + new_pot * hand_vs_comb(hand, villian.f3c_list)
    ev_no_cold_4b = (ev_fold * villian_fold_count + ev_call * villian_call_count + ev_4b * villian_4b_count) / count

    ev = ev_4b * cold_4b_total_prob + ev_no_cold_4b * (1 - cold_4b_total_prob)
    

    return round(ev, 2)
    # return str(round(ev, 2)) + " BB"

def threeb_steal_range(villian, position):
    ev_plus_list = []
    ev_minus_list = []
    ev_breakeven_list = []

    three_bet_size = 3
    if position == "SB":
        three_bet_size = 3.5
    if position == "BB":
        three_bet_size = 3.5

    for hand in rank:
        ev = hero_3b_fold_4b_ev(hand, three_bet_size, villian, position)
        print(hand, ev)
        if ev > 0.1:
            ev_plus_list.append(hand)
        if ev < -0.1:
            ev_minus_list.append(hand)
        if -0.1 <= ev <= 0.1:
            ev_breakeven_list.append(hand)
    return ev_plus_list, ev_breakeven_list, ev_minus_list

if __name__ == "__main__":
    """
    villian_btn = Villian(0.42, 0.6, 0.15, 2.4)
    print(hero_3b_fold_4b_ev("KTo", three_bet_size=3, villian=villian_btn, position="SB"))
    print(hero_3b_fold_4b_ev("KTo", three_bet_size=3.5, villian=villian_btn, position="SB"))
    print(hero_3b_fold_4b_ev("KTo", three_bet_size=4, villian=villian_btn, position="SB"))
    villian_utg = Villian(0.15, 0.5, 0.2, 2.4)
    print(hero_3b_fold_4b_ev("KQo", three_bet_size=3, villian=villian_utg, position="MP"))
    print(hero_3b_fold_4b_ev("KQo", three_bet_size=3.5, villian=villian_utg, position="SB"))
    print(hero_3b_fold_4b_ev("KQo", three_bet_size=3, villian=villian_utg, position="BB"))
    """

    villian_btn = Villian(0.5, 0.6, 0.15, 2.4)
    list_1, list_2, list_3 = threeb_steal_range(villian_btn, "BB")
    print(list_1)
    print(list_2)
    print(list_3)