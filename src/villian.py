from hand_eval import combinator_count
from sklansky import rank


def hand_cmp(hand1, hand2):
    x = rank.index(hand1)
    y = rank.index(hand2)
    if x < y:
        return 1
    if x > y:
        return -1
    return 0

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def freq_to_list(method="up", now_list=[], freq=1):
    return_list = []
    if now_list == []:
        use_list = rank
    else:
        use_list = sorted(now_list, key=cmp_to_key(hand_cmp), reverse=True)
        
    if method == "down":
        use_list = sorted(use_list, key=cmp_to_key(hand_cmp), reverse=False)

    count = combinator_count("", use_list)
    use_count = round(sum(count) * freq)
    now_count = 0

    for i in range(len(use_list)):
        return_list += [use_list[i]]
        now_count += count[i]
        if now_count >= use_count:
            return return_list
        
    return return_list

class Villian:
    def __init__(self, rfi, f3b, r4b, open_size=3):
        """
        rfi: Raise first in
        f3b: Fold to 3-bet
        r4b: Raise to 4-bet
        f3c: Flat call 3-bet
        """
        self.rfi = rfi
        self.rfi_list = freq_to_list("up", now_list=[], freq=self.rfi)
        self.f3b = f3b
        self.f3b_list = freq_to_list("down", now_list=self.rfi_list, freq=self.f3b)
        self.r4b = r4b
        self.r4b_list = freq_to_list("up", now_list=self.rfi_list, freq=self.r4b)
        self.f3c_list = list(set(self.rfi_list).difference(set(self.f3b_list)).difference(set(self.r4b_list)))
        self.open_size = open_size
    
    def change_list(self, rfi_list, f3b_list, r4b_list):
        """
        Need to write this very powerful
        like 99+ refers 99, TT, JJ, QQ, KK, AA
        Alse deal with bluffing like A5s
        """
        return 0

if __name__ == "__main__":
    villian_btn = Villian(0.42, 0.65, 0.08, 3)
    print(villian_btn.rfi_list)
    print(villian_btn.f3b_list)
    print(villian_btn.r4b_list)
    print(villian_btn.f3c_list)