from game_parameter import small_blind
from hand_eval import hand_vs_comb, combinator_count
from villian import Villian
from sklansky import rank
from math import pow


def hero_3b_fold_4b_ev(hand, three_bet_size, villian, position):
    villian_fold_count = sum(combinator_count(hand, villian.f3b_list))
    villian_call_count = sum(combinator_count(hand, villian.f3c_list))
    villian_4b_count = sum(combinator_count(hand, villian.r4b_list))
    count = villian_fold_count + villian_call_count + villian_4b_count
    pot = 1 + small_blind + villian.open_size
    new_pot = 1 + small_blind + three_bet_size * villian.open_size * 2
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

    ev_4b = - three_bet_size * villian.open_size
    ev_call = - three_bet_size * villian.open_size + new_pot * hand_vs_comb(hand, villian.f3c_list)
    ev_no_cold_4b = (ev_fold * villian_fold_count + ev_call * villian_call_count + ev_4b * villian_4b_count) / count

    ev = ev_4b * cold_4b_total_prob + ev_no_cold_4b * (1 - cold_4b_total_prob)
    
    if position == "BB":
        ev -= 1
    if position == "SB":
        ev -= small_blind
    return str(round(ev, 2)) + " BB"

if __name__ == "__main__":
    villian_btn = Villian(0.42, 0.6, 0.15, 2.4)
    print(hero_3b_fold_4b_ev("KTo", three_bet_size=3, villian=villian_btn, position="SB"))
    print(hero_3b_fold_4b_ev("KTo", three_bet_size=3.5, villian=villian_btn, position="SB"))
    print(hero_3b_fold_4b_ev("KTo", three_bet_size=4, villian=villian_btn, position="SB"))
    villian_utg = Villian(0.15, 0.5, 0.2, 2.4)
    print(hero_3b_fold_4b_ev("KQo", three_bet_size=3, villian=villian_utg, position="MP"))
    print(hero_3b_fold_4b_ev("KQo", three_bet_size=3.5, villian=villian_utg, position="SB"))
    print(hero_3b_fold_4b_ev("KQo", three_bet_size=3, villian=villian_utg, position="BB"))