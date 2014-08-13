import json
import sys

if __name__ == "__main__":
    output = sys.stdin.read()
    output_dict = json.loads(output)
    winner = output_dict['winner']
    players = output_dict['players']
    all_players = output_dict['all_players']
         
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

    for player in all_players.values():
        print 'Player {} killed: '.format(player['name']),
        for killed_player, num_times in player['has_killed'].items():
            print '{} x {}, '.format(killed_player, num_times),
        print
    for player in all_players.values():
        print 'Player {} was killed by: '.format(player['name']),
        for killed_player, num_times in player['was_killed_by'].items():
            print '{} x {}, '.format(killed_player, num_times),
        print