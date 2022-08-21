#!/usr/bin/python
import sys
import logging

#create logger
# logging.basicConfig(filename='tinyhelper.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger('simple_log')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
ch.setFormatter(formatter)

logger.addHandler(ch)

class colors: # You may need to change color settings
    RED = '\033[31m'
    ENDC = '\033[m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[38;5;27m'
    ORANGE = '\033[38;5;202m'
    PURPLE = '\033[38;5;129m'

def print_floor(floor):
    logger.debug('printing the floor formatted')
    # logger.debug(list(floor))
    types = {
        'Creative': colors.ORANGE,
        'Recreation': colors.YELLOW,
        'Service': colors.BLUE,
        'Retail': colors.PURPLE,
        'Food': colors.GREEN,
        'Residential': colors.ENDC
    }
    keys = {
        'Floor Name': 18,
        'Type': 12,
        'Rank': 4,
        'Floor Number': 4
    }
    # logger.debug(floor.items())
    # logger.debug(floor.keys())
    
    # v1
    # print(types.get(floor['Type'], colors.ENDC) + f'{floor["Floor Name"]: <{17}}' + " " + f'{floor["Type"]: <{10}}' + " " + f'{floor["Rank"]: >{3}}' + colors.ENDC)

    # v2
    # print_string = types.get(floor['Type'], colors.ENDC)
    # for key in floor.keys(): 
    #     logger.debug(floor[key])
    #     print_string = print_string + f'{floor[key]:<{keys[key]}}'
    # print_string = print_string + colors.ENDC
    # print(print_string)

    # v3
    # print(types.get(floor['Type'], colors.ENDC) + ''.join([f'{floor[key]:<{keys[key]}}' for key in floor.keys() if key!='Floor Number']) + colors.ENDC)

    # v4
    if floor.get('Floor Number'):
        print(types.get(floor['Type'], colors.ENDC) + f'{floor["Floor Number"]:<{keys["Floor Number"]}}' + ''.join([f'{floor[key]:<{keys[key]}}' for key in floor.keys() if key!='Floor Number']) + colors.ENDC)
    else:
       print(types.get(floor['Type'], colors.ENDC) + ''.join([f'{floor[key]:<{keys[key]}}' for key in floor.keys()]) + colors.ENDC)
    


def main(argv):
    import argparse
    import csv

    parser = argparse.ArgumentParser(description='Tells you what floor to build next in Tiny Tower')
    parser.add_argument("-l","--full-list", required=False, action='store_true', help="Print out the full list of floors in descending order. Superscedes all other commands.")
    parser.add_argument("-gt","--gold-tickets", required=False, nargs = "?", default = 0, type = int, help="Number of Gold Tickets on the tower. Used to calculate how many residential floors are needed.")
    parser.add_argument("-sl","--shared-living", required=False, action='store_true', default=False, help="Flag if the player has unlocked the shared living tech upgrade. Sets the maximum occupancy for a residential floor to 6 bitizens instead of 5.")
    parser.add_argument("-r","--reuse_bits", required=False, action='store_true', default=False, help="Flag if the player will reuse bits for floors 3 up to the number of gold tickets. Allows the player to build less residential floors and more stores.")
    parser.add_argument("-t","--target_floor", required=False, nargs = "?", default = 50, type = int, help = "What floor the player is building towards next. Defaults to 50 to show first 50 floors of the tower.")
    parser.add_argument("-d","--debug", required=False, action='store_true', default=False, help="Add flag to run with debug statements on.")
    args = parser.parse_args()

    if not(args.debug):
        ch.setLevel(logging.INFO)
    logger.debug(args)

    logger.debug("reading in floors.csv")
    floors_list = "floors.csv"
    floors = []
    with open('floors.csv', newline='') as floors_list:
        reader = csv.DictReader(floors_list)
        for row in reader:
            row.update({"Rank":int(row["Rank"])})
            floors.append(row)
        
    logger.debug("successfully read in floors.csv")
    
    if args.full_list:
        [print_floor(x) for x in sorted(floors, key=lambda d: d['Rank'], reverse=True)]
        logger.debug("finished running with -l argument")
        exit()
    
    if args.gold_tickets is None:
        args.gold_tickets = 0
    logger.debug('gold tickets: %s', args.gold_tickets)

    if args.shared_living:
        max_occupancy = 6
    else:
        max_occupancy= 5
    logger.debug('max occupancy: %s', max_occupancy)

    if args.target_floor is None:
        args.target_floor = 50
    logger.debug('target floor: %s', args.target_floor)

    residential_floor = {
        "Floor Name": "Residential", 
        "Type": "Residential"
    }

    current_vacancy = 0
    current_tower = []
    next_store = floors.pop(0)
    for current_floor_num in range(2,args.target_floor+1):
        logger.debug('next store: %s', next_store)
        logger.debug('current floor number: %s', current_floor_num)
        logger.debug('current vacancy: %s', current_vacancy)

        if current_floor_num == 2 or current_vacancy < 3:
            current_floor = residential_floor.copy()
            current_floor.update({"Floor Number": current_floor_num})
            logger.debug("adding floor: %s" ,current_floor)
            current_tower.append(current_floor)
            current_vacancy += max_occupancy
            
        elif args.reuse_bits and next_store["Rank"]>3 and next_store["Rank"]<args.gold_tickets:
            # if reuse_bits is on, then don't decrease vacancy for floors ranked 4 up to the number of gold tickets
            current_floor = next_store.copy()
            current_floor.update({"Floor Number": current_floor_num})
            logger.debug("adding floor: %s" ,current_floor)
            current_tower.append(current_floor)
            next_store = floors.pop(0)

        else:
            current_floor = next_store.copy()
            current_floor.update({"Floor Number": current_floor_num})
            logger.debug("adding floor: %s" ,current_floor)
            current_tower.append(current_floor)
            current_vacancy -= 3
            next_store = floors.pop(0)

    # [print_floor(x) for x in sorted(current_tower, key=lambda d: d['Floor Number'], reverse=True)]
    [print_floor(x) for x in current_tower]




if __name__ == "__main__":
   main(sys.argv[1:])