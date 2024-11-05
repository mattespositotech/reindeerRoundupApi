from enums.roundup_enums import RoundupStatus
from enums.user_enums import UserStatus
import uuid


def prep_roundup_for_mongo(roundup):
    roundup['status'] = RoundupStatus.InProgress.value

    for participant in roundup['participants']:
        # change to prep method
        participant['status'] = UserStatus.Pending.value
        participant['uuid'] = str(uuid.uuid4())

    roundup['blacklists'] = remove_duplicates(roundup['blacklists'])

    return roundup

def prep_participant(participant):
    participant['status'] = UserStatus.Pending.value
    participant['uuid'] = str(uuid.uuid4())

def remove_duplicates(blacklist):
    seen = set()
    unique_blacklist = []

    for lst in blacklist:
        tpl = tuple(lst)
        if tpl not in seen:
            seen.add(tpl)
            unique_blacklist.append(lst)
    
    return unique_blacklist