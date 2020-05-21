from datetime import datetime
import re
import os
import sqlite3


DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flights_db.sqlite")
connection = sqlite3.connect(DATABASE_PATH)

flights_regex = {
    "from cairo to hurghada": re.compile(r"from cairo to hurghada|\bto hurghada|from CA to HG\b"),
    "from hurghada to cairo": re.compile(r"from hurghada to cairo|from HG to CA\b"),
    "from cairo to aswan": re.compile(r"from cairo to aswan|\bto aswan|from CA to AS\b"),
    "from aswan to cairo": re.compile(r"from aswan to cairo|from AS to CA\b"),
    "from cairo to sharm el shiekh": re.compile(r"from cairo to sharm el shiekh|\bto sharm el shiekh|from CA to SA\b|from cairo to sharm al shiekh|from cairo to sharm al shaiekh|from cairo to sharm el-shaiekh|from cairo to sharm al-shaiekh|from cairo to sharm el-shiekh"),
    "from from sharm el shiekh to cairo": re.compile(r"from sharm el shiekh to cairo|from SA to CA\b|from sharm al shiekh to cairo|from sharm al shaiekh to cairo|from sharm el-shaiekh to cairo|from sharm al-shaiekh to cairo|from sharm el-shiekh to cairo"),
}

# build a bank request to make things fun
response_bank = {
    "greetings": ["hello there!, how can i help?", "hello!, I am yasmen, i can  help you to book a flight and ask for any flight informations?", "Hello friend! how can i help you?"],
    "thanks": ["Feel free to contact us anytime", "I am happy to help", "More than happy to help"],
    "availability_enq": ["we have a flight {flight} on {date} for only {price}$ !!", "the nearest flight {flight} is on {date}, with the price of {price}$."],
    "cost_enq": ["the nearest flight {flight} will cost only {price}$"],
    "date_enq": ["we have a flight {flight} on {date} for only {price}$ !!", "the nearest flight {flight} is on {date}, with the price of {price}$."],
    "reserve_enq": ["Sure, you would like to confirm your booking a flight {flight} , on {date} ", "Would you please confirm your flight reservation {flight}  on {date}?"],
    "unknown": ["i didn't get that sorry", "kindly would you try again, i didn't get this one", "sorry could you try this again"],
    "registered": ["you have registered to a flight {flight}!, see you on {date} !!"]
}

examples = [
    # greetings
    "hello there",
    "good morning",
    "welcome",
    "hi!, how are you",
    "Hi there !!",

    # thanks
    "thanks",
    "that's it",
    "goodbye",
    "bye",
    "okay",

    # cost examples
    "How much for the flight from cairo to hurghada?",
    "what is the cost for the flight from hurghada to aswan",
    "what is the price for the flight from aswan to cairo?",
    "what is the price of the flight from hurghada to aswan",
    "can you tell me the price of a flight from cairo to sharm el sheikh",
    "what do i pay for the flight from sharm el sheikh to cairo?",
    "how much will i pay for this flight?",

    # availability examples
    "do you have a flight from hurghada to aswan",
    "i want to know if you have a flight from hurghada to cairo",
    "do you have information about a flight to cairo ?",
    "i want to know information about a flight from sharm el sheikh to cairo",
    "do you have summer flights ?",
    "i want to travel from cairo to aswan",

    # date examples
    "when will the flight be ?",
    "when can i travel ?",
    "can you tell me the flight date?",
    "what is the date for the upcoming flight?",
    "when is the soonest flight",
    "when is the nearest flight",

    # reservation
    "i want to reserve the flight from cairo to aswan",
    "i want to sign up in the the flight from hurghada to aswan",
    "let me reserve this fight",
    "register me in the flight to aswan",
    "can i reserve this flight",
    "can i book this flight",
    "let me book this fight",
    "i want to book the flight from cairo to aswan",
    "sign me up in the flight from sharm el sheikh to el hurghada",
    "great would you book this flight to me",
]

labels = [
    # greetings
    "greetings",
    "greetings",
    "greetings",
    "greetings",
    "greetings",

    # thanks
    "thanks",
    "thanks",
    "thanks",
    "thanks",
    "thanks",

    # cost labels
    "cost_enq",
    "cost_enq",
    "cost_enq",
    "cost_enq",
    "cost_enq",
    "cost_enq",
    "cost_enq",

    # availability labels
    "availability_enq",
    "availability_enq",
    "availability_enq",
    "availability_enq",
    "availability_enq",
    "availability_enq",

    # date
    "date_enq",
    "date_enq",
    "date_enq",
    "date_enq",
    "date_enq",
    "date_enq",

    # reservation labels
    "reserve_enq",
    "reserve_enq",
    "reserve_enq",
    "reserve_enq",
    "reserve_enq",
    "reserve_enq",
    "reserve_enq",
    "reserve_enq",
    "reserve_enq",
    "reserve_enq",
]

#knowldge back ~ our database
KB = {
    "from cairo to hurghada":
    {
        "price": 100,
        "date": datetime(2020, 5, 5),
        "registered": 0
    },
    "from hurghada to cairo":
    {
        "price": 200,
        "date": datetime(2020, 5, 10),
        "registered": 0
    },
    "from cairo to sharm el sheikh":
    {
        "price": 150,
        "date": datetime(2020, 5, 3),
        "registered": 0
    },
    "from sharm el sheikh to cairo":
    {
        "price": 200,
        "date": datetime(2020, 5, 17),
        "registered": 0
    },
    "from cairo to aswan":
    {
        "price": 250,
        "date": datetime(2020, 6, 20),
        "registered": 0
    },
    "from aswan to cairo":
    {
        "price": 200,
        "date": datetime(2020, 7, 11),
        "registered": 0
    }
}


def load_data_to_db():
    connection.execute("delete from flights")
    for flight in KB.keys():
        price = KB[flight]['price']
        date = KB[flight]['date'].strftime("%d-%m-%Y")
        register = KB[flight]['registered']
        connection.execute(f"insert into flights (name, price, duration, start_date, registered)\
            values ('{flight}', '{price}', '{date}', '{register}')")
    connection.commit()
    print("all done !")

def get_flight_data(flight):
    res = connection.execute(f"select * from flights where name = '{flight}'").fetchall()[0]
    course_info = {
        "name": res[0],
        "price": res[2],
        "date": res[3],
        "registered": res[4]
    }
    return course_info

def register_user(flight):
    connection.execute(f"update flights set registered=registered+1 where name = '{flight}'")
    connection.commit()

    


if __name__ == "__main__":
    load_data_to_db()