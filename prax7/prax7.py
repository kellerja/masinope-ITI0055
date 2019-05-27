def fc_entails_setup(kb):
    count = []
    inferred = {}
    agenda = []
    kb_by_symbol = {}
    for i, rule in enumerate(kb[1:]):
        count.append(len(rule[0]))
        inferred[rule[1]] = False
        if not kb_by_symbol.get(rule[1], False):
            kb_by_symbol[rule[1]] = []
        for s in rule[0]:
            temp = kb_by_symbol.get(s, [])
            temp.append((i, rule))
            kb_by_symbol[s] = temp
    for fact in kb[0]:
        agenda.append(fact)
        inferred[fact] = False
    return count, inferred, agenda, kb_by_symbol

def fc_entails(kb, q):
    # kb - teadmusbaas mingil kujul
    # q - loogikamuutuja e. sümbol, mille kohta tahame teada, kas see järeldub kb-st
    if q in kb[0]: return True
    count, inferred, agenda, kb_by_symbol = fc_entails_setup(kb)
    while len(agenda) != 0:
        current_symbol = agenda.pop()
        if not inferred[current_symbol]:
            inferred[current_symbol] = True
            for i, rule in kb_by_symbol[current_symbol]:
                count[i] -= 1
                if count[i] == 0:
                    if rule[1] == q: return True
                    agenda.append(rule[1])
    return False

def generate_rules(moves):
    rules = [[]]
    for i in range(len(moves)):
        for j in range(len(moves)):
            prev = i % len(moves)
            prev_prev = j % len(moves)
            if i == j:
                rules.append((['PP_' + moves[prev_prev],'P_' + moves[prev]], moves[prev]))
            else:
                for z in range(len(moves)):
                    if (z != i and z != j):
                        rules.append((['PP_' + moves[prev_prev], 'P_' + moves[prev]], moves[z]))
                        break
    return rules

def kkp(moves, possible_moves):
    if len(moves) < 2: return "Need list with at least 2 moves"
    prev_prev = moves[-2]
    prev = moves[-1]
    kb = generate_rules(possible_moves)
    kb[0] = ['PP_' + prev_prev, 'P_' + prev]
    for move in possible_moves:
        if (fc_entails(kb, move)):
            return "Roboti käik: " + move
    return "Invalid inputs"

moves = ['Kivi', 'Paber', 'Käärid']
print(kkp([moves[0], moves[1]], moves))
print(kkp([moves[0], moves[0]], moves))
print(kkp([moves[2], moves[1]], moves))
print(kkp([moves[2], moves[2]], moves))
