```python
from funhandler import Handler

handle = Handler()


""" This should generate 10 episodes with 8000 steps of indiviual coins. It's double when considering jump diffusion"""
handle.generate_stochastic_episodes(
    episode_number=10, 
    types_per_episode=['gbm', 'jump_diffusion'], 
    number_per_episode=8000) # Generates a hierarchy of stochastic sessions



# Example Stochastic Episodes
""" Returns a list of episodes """
episodes = handle.get_episodes() # ['1a9f9a17-2e6a-4c8f-8793-c50b508c8ba4', 'a57fb01e-5457-429a-a405-8152401e2715',...]
env = PortfolioEnv()

for eps in episodes:
    eid = client.start_episode() # assuming we're using the ray library to learn what's going on
    
    while handle.is_sessions(eps):
        env.reset()
        session_id = handle.pop_session(episode_id=eps) # '112c5d5e-170d-47b7-a05c-a03b693980b2'
        while handle.is_session(session_id=session_id):
            data = handle.pop_data(session_id=session_id)
            preprocessed = strategy.step(data)
            # reshape preprocessed data here
            # Have a (4 rows, n columns) in numpy array
            action = client.get_action(preprocessed)
            reward = env.step(action)
            if reward != 0:
                client.log_returns(eid, reward)
    client.end_episode(eid, obs)
```