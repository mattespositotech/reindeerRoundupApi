import random
from services.roundup import get_roundup_by_id
from utils.exceptions import NoValidCombinationError
from utils.constants import MATCH_MAX_ATTEMPTS

def launch_secret_santa(roundup_id):
    roundup = get_roundup_by_id(roundup_id)
    
    matches = get_matches(roundup)

    return matches

def get_matches(roundup):
    participants = roundup['participants']
    blacklists = roundup['blacklist']

    participants_ids = get_list_of_ids_that_accepted(participants)
    sanitized_blacklists = sanitize_blacklists_by_accepted(participants_ids, blacklists)

    return attempt_match(participants_ids, sanitized_blacklists)

def get_list_of_ids(participants):
    return [par['id'] for par in participants]

def get_list_of_ids_that_accepted(participants):
    return [par['id'] for par in participants if par['status'] == 1]

def sanitize_blacklists_by_accepted(accepted_ids, blacklists):
    sanitized_blacklists = [[id for id in blacklist if id in accepted_ids] for blacklist in blacklists]
    return [blacklist for blacklist in sanitized_blacklists if blacklist]

# change prints to logs
def attempt_match(id_list, blacklists):
    for attempt in range(MATCH_MAX_ATTEMPTS):
        try:
            return match_participants(id_list, blacklists)
        except NoValidCombinationError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == MATCH_MAX_ATTEMPTS - 1:
                print("Max attempts reached. Unable to find a valid assignment.")

def match_participants(id_list, blacklists):
    matches = {id: None for id in id_list}
    used_values = set()

    blacklist_lookup = {}
    for blacklist in blacklists:
        for blk_id in blacklist:
            blacklist_lookup[blk_id] = set(blacklist)
    
    for id in id_list:
        valid_choices = set(id_list) - {id} - used_values
        if id in blacklist_lookup:
            valid_choices -= blacklist_lookup[id]
        
        if not valid_choices:
            raise NoValidCombinationError
        
        chosen_value = random.choice(list(valid_choices))
        matches[id] = chosen_value
        used_values.add(chosen_value)

    return matches