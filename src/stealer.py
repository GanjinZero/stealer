from game_parameter import small_blind
from hand_eval import hand_vs_comb, combinator_count
from villian import Villian


def hero_3b_fold_4b_ev(hand, three_bet_size, villian):
    villian_fold_count = sum(combinator_count(hand, villian.f3b_list))
    villian_call_count = sum(combinator_count(hand, villian.f3c_list))
    villian_4b_count = sum(combinator_count(hand, villian.r4b_list))
    count = villian_fold_count + villian_call_count + villian_4b_count
    pot = 1 + small_blind + villian.open_size
    new_pot = 1 + small_blind + three_bet_size * villian.open_size * 2
    ev_fold = pot
    ev_4b = - three_bet_size * villian.open_size
    ev_call = - three_bet_size * villian.open_size + new_pot * hand_vs_comb(hand, villian.f3c_list)
    ev = (ev_fold * villian_fold_count + ev_call * villian_call_count + ev_4b * villian_4b_count) / count
    return str(round(ev, 2)) + " BB"

if __name__ == "__main__":
    villian_btn = Villian(0.42, 0.6, 0.15, 3)
    print(hero_3b_fold_4b_ev("KQo", three_bet_size=3, villian=villian_btn))
    print(hero_3b_fold_4b_ev("KQo", three_bet_size=3.5, villian=villian_btn))
    print(hero_3b_fold_4b_ev("KQo", three_bet_size=4, villian=villian_btn))
    villian_btn = Villian(0.42, 0.6, 0.15, 2.4)
    print(hero_3b_fold_4b_ev("KQo", three_bet_size=3, villian=villian_btn))
    print(hero_3b_fold_4b_ev("KQo", three_bet_size=3.5, villian=villian_btn))
    print(hero_3b_fold_4b_ev("KQo", three_bet_size=4, villian=villian_btn))