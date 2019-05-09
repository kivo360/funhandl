import time
import uuid
from loguru import logger
from funhandler import Handler

from crayons import cyan

handle = Handler()
set_id = handle.generate_stochastic_episodes(
    episode_number=30,
    sessions_per_episode=1,
    steps_per_session=1000
)
# set_id = "027da34a-4289-4dd2-aa19-01a6a05cda03"
# set_id = "869b57bf-00bf-4281-9531-a2cea01a3c35"
# set_id = "726241df-f49f-42c8-b6e4-3fcff08d5744"
print(set_id)
time.sleep(5)
limit=250
episodes = handle.get_episodes(set_id)
for eps in episodes:
    eid = uuid.uuid4().hex
    sessions = handle.get_sessions(eps)
    while handle.is_sessions(eps):
        session_id = handle.pop_session(eps)
        print(f"Trying session: {session_id}")
        handle.load_session(session_id)
        while handle.is_session(session_id):
            result = handle.pop_data(session_id, limit=limit)
            if handle.is_limit(result, limit):
                logger.info(cyan(f"{result}"), enqueue=True)
                # print(result)
