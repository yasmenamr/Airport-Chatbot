# Yasmen Amr chat-bot

```raw
bot : hello!, I am yasmen, i can  help you to book a flight and ask for any flight informations?
user: which flights do you have ?
bot : we are a domestic airport ,our flights are between cairo and some governments ,where would you travel?
user:i want to travel from cairo to aswan.
bot : the nearest flight from cairo to aswan is on 20-06-2020, with the price of 250$.
user: great would you book this flight to me ?
```

the bot helps users to know about the flights that are available in our Airport, and tell them information about them

## Usage and installation

to use the model with your own system, you can create an object of the Bot class and choose if you want it to retrain, it as follows

```python
from cyborg import Bot

# if you want it to retrain, set retrain=True
# you can choose which approach deep_learning or machine learning
bot = Bot(retrain=False, deep_learning=True)
# run the bot loop
bot.run_blocking()
```

Don't forget to create a virtual environment to run the code

```bash
$python -m venv venv
$source venv/bin/activate
$pip install -r requirements.txt
```
