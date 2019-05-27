from hmmlearn import hmm
import numpy as np

state_map = ['S', 'M', 'L']
hidden_state_map = ['H', 'C']

states = np.array([state_map.index(x) for x in 'S M S S L L M M L M S M M S S L S L L L L L L L L L L S L S'.split()]).reshape(-1, 1)

# [(H)ot_weather, (C)old_weather]
initial = np.array([0.6, 0.4])                 # initial state probability
# [
# [H, C],
# [H, C]
# ]
transition = np.array([[0.7, 0.3],[0.3, 0.7]])  # state transition
# [
# H: [(S)mall, (M)edium, (L)arge],
# C: [S, M, L]
# ]
sensor = np.array([[0.1, 0.4, 0.5], [0.7, 0.2, 0.1]])    # observation, given state

# katse 1
hm1 = hmm.MultinomialHMM(n_components=2)
hm1.startprob_ = initial
hm1.transmat_ = transition
hm1.emissionprob_ = sensor

h_states = hm1.predict(states)
print("Most likely hidden states (known model)", ' '.join([hidden_state_map[x] for x in h_states]))

# katse 2
hm2 = hmm.MultinomialHMM(n_components=2, params="st", init_params="st")
hm2.emissionprob_ = sensor

hm2.fit(states)
h_states = hm2.predict(states)
print("Most likely hidden states (partially known)", ' '.join([hidden_state_map[x] for x in h_states]))
print("Learned transition probabilities")
print(hm2.transmat_)

# katse 3
hm3 = hmm.MultinomialHMM(n_components=2, params="est", init_params="est")

hm3.fit(states)
h_states = hm3.predict(states)
print("Most likely hidden states (unknown)", ' '.join([hidden_state_map[x] for x in h_states]))
print("Learned emission probabilities")
print(hm3.emissionprob_)
print("Learned transition probabilities")
print(hm3.transmat_)
print('Learned initial probabilities')
print(hm3.startprob_)
