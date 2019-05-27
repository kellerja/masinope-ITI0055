# actions = ['NoOp', 'Left', 'Right', 'Suck']

def performance(state, actions, performance_const=0):
    cleanliness = 0
    for room in state['rooms']:
        if room['isDirty']:
            cleanliness -= 100 # non clean rooms are really bad
        else:
            cleanliness += 1
    energy = 0
    for actions in actions:
        if actions == 'Left':
            energy += 1
        elif actions == 'Right':
            energy += 1
        elif actions == 'Suck':
            energy += 1
    return performance_const + cleanliness - energy

def vacworld_sim(state, steps=10):
    history = []
    prev_actions = []
    agent_state = None
    score = None
    for step in range(steps):
        for i, room in enumerate(state['rooms']):
            if not room['agent']: continue
            percepts = {'isDirty': room['isDirty'], 'room': room['name']}
            action, agent_state = room['agent'](percepts, agent_state)
            prev_actions.append(action)
            score = performance(state, prev_actions)
            history.append('agent in room ' + room['name'] + ' with isDirty ' + str(room['isDirty']).upper() + ' did ' + action.upper() + ' on step ' + str(step) + " with score " + str(score))
            if (action == 'Suck'):
                state['rooms'][i]['isDirty'] = False
            elif (action == 'Left'):
                state['rooms'][(i + 1) % len(state['rooms'])]['agent'] = room['agent']
                room['agent'] = None
            elif (action == 'Right'):
                state['rooms'][(i - 1) % len(state['rooms'])]['agent'] = room['agent']
                room['agent'] = None
            break
    return history, score

def reflex_agent(percepts, state=None):
    action = 'NoOp'
    if percepts['isDirty']:
        action = 'Suck'
    elif percepts['room'] == 'A':
        action = 'Right'
    else:
        action = 'Left'
    return action, state

def state_reflex_agent(percepts, state):
    if state is None:
        state = [] # list of clean rooms
    action = "NoOp"
    if percepts['isDirty']:
        action = 'Suck'
        state.append(percepts['room'])
    elif percepts['room'] == 'A' and 'B' not in state:
        action = 'Right'
        if not percepts['isDirty']:
            state.append(percepts['room'])
    elif percepts['room'] == 'B' and 'A' not in state:
        action = 'Left'
        if not percepts['isDirty']:
            state.append(percepts['room'])
    return action, state

def new_state(agent, room_A_dirty=True, room_B_dirty=True):
    a = {
        "name": "A",
        "isDirty": room_A_dirty,
        "agent": agent
    }
    b = {
        "name": "B",
        "isDirty": room_B_dirty,
        "agent": None
    }
    state = {
        "rooms": [a, b],
    }
    return state

if __name__=='__main__':
    moves, score = vacworld_sim(new_state(reflex_agent))
    print('Agent reflex_agent finished with score ' + str(score))
    moves, score = vacworld_sim(new_state(state_reflex_agent))
    print('Agent state_reflex_agent finished with score ' + str(score))
