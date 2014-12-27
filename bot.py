#-----------------------------------------------------------#
# Heads Up Omaha Challange - Starter Bot                    #
#===========================================================#
#                                                           #
# Last update: 22 May, 2014                                 #
#                                                           #
# @author Jackie <jackie@starapple.nl>                      #
# @version 1.0                                              #
# @license MIT License (http://opensource.org/licenses/MIT) #
#-----------------------------------------------------------#
from sys import stderr, stdin, stdout
import itertools
from poker import Card, Hand, Pocket, Table
from poker import Ranker

class Bot(object):
    '''
    Main bot class
    '''
    def __init__(self):
        '''
        Bot constructor

        Add data that needs to be persisted between rounds here.
        '''
        self.settings = {}
        self.match_settings = {}
        self.game_state = {}
        self.pocket = None
        self.bots = {
            'me': {},
            'opponent': {}
        }

        # Need to initialize to 0.
        self.match_settings['round'] = 0
        self.match_settings['table'] = []

    def run(self):
        '''
        Main loop

        Keeps running while begin fed data from stdin.
        Writes output to stdout, remember to flush.
        '''
        while not stdin.closed:
            try:
                rawline = stdin.readline()

                # End of file check
                if len(rawline) == 0:
                    break

                line = rawline.strip()

                # Empty lines can be ignored
                if len(line) == 0:
                    continue

                parts = line.split()
                command = parts[0].lower()

                if command == 'settings':
                    self.update_settings(parts[1:])
                    pass
                elif command == 'match':
                    self.update_match_info(parts[1:])
                    pass
                elif command.startswith('player'):
                    self.update_game_state(parts[0], parts[1], parts[2])
                    pass
                elif command == 'action':
                    stdout.write(self.make_move(parts[2]) + '\n')
                    stdout.flush()
                    pass
                else:
                    stderr.write('Unknown command: %s\n' % (command))
                    stderr.flush()
            except EOFError:
                return

    def update_settings(self, options):
        '''
        Updates game settings
        '''
        key, value = options
        self.settings[key] = value

    def update_match_info(self, options):
        '''
        Updates match information
        '''
        key, value = options
        if key == 'round' and int(value) == int(self.match_settings['round']) + 1:
            self.match_settings['table'] = []
        self.match_settings[key] = value


    def update_game_state(self, player, info_type, info_value):
        '''
        Updates game state
        '''
        # Checks if info pertains self
        if player == self.settings['yourBot']:
            
            # Update bot stack
            if info_type == 'stack':
                self.bots['me']['stack'] = int(info_value)

            # Remove blind from stack
            elif info_type == 'post':
                self.bots['me']['stack'] -= int(info_value)

            # Update bot cards
            elif info_type == 'hand':
                self.bots['me']['pocket'] = Pocket(self.parse_cards(info_value))

            # Round winnings, currently unused
            elif info_type == 'wins':
                pass

            else:
                stderr.write('Unknown info_type: %s\n' % (info_type))

        else:

            # Update opponent stack
            if info_type == 'stack':
                self.bots['opponent']['stack'] = int(info_value)

            # Remove blind from opponent stack
            elif info_type == 'post':
                self.bots['opponent']['stack'] -= int(info_value)

            # Opponent hand on showdown, currently unused
            elif info_type == 'hand':
                pass

            # Opponent round winnings, currently unused
            elif info_type == 'wins':
                pass

    def make_move(self, timeout):
        '''
        Checks cards and makes a move
        '''
        
        # Get average card value

        """
        My Stuff
        Will need to decide how strong hands actually are in omaha later on.
        """
        #if not self.match_settings.has_key('table'):
        #    return 'call ' + self.match_settings['amountToCall']

        command = ''

        ## Evaluate hand, before the flop
        #if not self.match_settings.has_key('table') or len(self.match_settings['table']) == 0:
        if len(self.match_settings['table']) == 0:
            hand_strength = Ranker.rank_single_hand(self.bots['me']['pocket'])
            stderr.write('four card hand strength: ' + str(hand_strength) + '\n')
            if hand_strength >= 60:
                command = 'raise ' + str(2 * int(self.match_settings['maxWinPot']))
            elif hand_strength >= 40:
                command = 'raise ' + str(int(self.match_settings['maxWinPot']))
            elif hand_strength >= 22:
                command = 'raise' + str(2/3 * int(self.match_settings['maxWinPot']))
            elif hand_strength >= 16:
                command = 'call ' + self.match_settings['amountToCall']
            else:
                command = 'call ' + self.match_settings['amountToCall']
        else:
            hand_strength = self.find_all_hands()[0]
            if hand_strength >= 14:
                command = 'raise ' + str(min([int(self.bots['me']['stack']), int(self.bots['opponent']['stack'])]))
            elif hand_strength >= 11:
                command = 'raise ' + str(1/2 * int(self.match_settings['maxWinPot']))
            elif hand_strength >= 8:
                command = 'raise ' + str(int(self.match_settings['bigBlind']))
            elif int(self.match_settings['amountToCall']) >= 2 * int(self.match_settings['bigBlind']):
                command = 'fold 0'
            elif hand_strength >= 6:
                command = 'call ' + self.match_settings['amountToCall']
            else:
                command = 'fold 0'
        return command

        """
        End my stuff
        """
        '''
        OLD STUFF
        average_card_value = 0
        for card in self.bots['me']['pocket']:
            average_card_value += card.number
        average_card_value /= 4

        # Check if we have something good
        if average_card_value > 8:
            return 'raise ' + str(2 * int(self.match_settings['bigBlind']))
        elif average_card_value > 4:
            return 'call ' + self.match_settings['amountToCall']

        return 'check 0'
        '''
    def parse_cards(self, cards_string):
        '''
        Parses string of cards and returns a list of Card objects
        '''
        return [Card(card[1], card[0]) for card in cards_string[1:-1].split(',')]

    def find_all_hands(self):
        ## Make sure the table is dealt or errors will show up.
        #try:
        #    self.match_settings['table']
        #except:
        #    return [7, self.bots['me']['pocket']]

        hands = []

        ## Stderr full self variables
        stderr.write('full self: ' + str(vars(self)) + '\n')

        #hand = self.parse_cards(self.bots['me']['hand'])
        hand = self.bots['me']['pocket']
        #table = self.match_settings['table']
        table = Table(self.parse_cards(self.match_settings['table']))

        #stderr.write('hand: ' + str(hand) + '\n')
        #stderr.write('hand2:' + str())
        #stderr.write('table: ' + str(table) + '\n')

        for h in itertools.combinations(hand, 2):
            for t in itertools.combinations(table, 3):
                hands += [h + t]
        ranked_hands = [Ranker.rank_five_cards(hand) for hand in hands]
        #stderr.write(str(max(ranked_hands)) + '\n')
        return max(ranked_hands)
        #for hand in hands:
        #    stderr.write('Ranker working: ' + str(Ranker.rank_five_cards(hand)) + '\n')

if __name__ == '__main__':
    '''
    Not used as module, so run
    '''
    Bot().run()