import us

abbreviations = []
for state in us.states.STATES:
    # abbreviations.append(state.abbr.upper())
    if state:
        print(state.abbr.upper())
# print(" ".join(abbreviations))
