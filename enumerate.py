import us

abbreviations = []
for state in us.states.STATES:
    if state:
        print(state.abbr.upper())
