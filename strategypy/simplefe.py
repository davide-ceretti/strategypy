import json
import sys

if __name__ == "__main__":
    output = sys.stdin.read()
    output_dict = json.loads(output)
    winner = output_dict['winner']
    players = output_dict['players']
    turns = output_dict['turns']
    initial_frame = output_dict['frames'][0]
    last_frame = output_dict['frames'][-1]
    initial_count = sum((len(x) for x in initial_frame.itervalues()))
    final_count = sum((len(x) for x in last_frame.itervalues()))

    winner = None if winner is None else players[str(winner)]
    if winner is None:
        print 'No player won and the game ended in {} turns'.format(turns)
    else:
        print 'Player {} won in {} turns'.format(winner, turns)
    print 'Initial unit count: {}'.format(initial_count)
    print 'Final unit count: {}'.format(final_count)
