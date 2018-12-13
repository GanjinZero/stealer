from stealer import hero_3b_fold_4b_ev
from game_parameter import small_blind
from hand_eval import hand_vs_comb, combinator_count
from villian import Villian
from sklansky import rank

# May need to rewrite stealer ev with bb and sb

def ev_call(hand, villian):
    ev = -(villian.open_size - 1) + hand_vs_comb(hand, villian.rfi_list) * (small_blind + villian.open_size * 2)
    return round(ev, 2)

def bb_vs_open_dict(villian):
    three_bet_size = 3.5
    for hand in rank:
        ev_3b_f4b = hero_3b_fold_4b_ev(hand, three_bet_size, villian, "BB")
        ev_c = ev_call(hand, villian)
        print(hand, ev_c, ev_3b_f4b)

if __name__ == "__main__":
    villian_btn = Villian(0.5, 0.6, 0.15, 2.4)
    bb_vs_open_dict(villian_btn)