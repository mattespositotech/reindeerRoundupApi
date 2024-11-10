from enums.roundup_enums import RoundupStatus
from enums.user_enums import UserStatus
import uuid


def prep_roundup_for_mongo(roundup):
    roundup['status'] = RoundupStatus.InProgress.value

    for participant in roundup['participants']:
        prep_participant(participant)

    roundup['blacklists'] = remove_duplicate_blacklists(roundup['blacklists'])

    return roundup

def prep_participant(participant):
    participant['status'] = UserStatus.Pending.value
    participant['uuid'] = str(uuid.uuid4())

def remove_duplicate_blacklists(blacklists):
    seen = set()
    unique_blacklist = []

    for lst in blacklists:
        tpl = tuple(lst)
        if tpl not in seen:
            seen.add(tpl)
            unique_blacklist.append(create_blacklist_object(lst))
    
    return unique_blacklist

def create_blacklist_object(blacklist):
    return {'uuid': str(uuid.uuid4()), 'blacklist': blacklist}