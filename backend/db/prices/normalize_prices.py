from motor.motor_asyncio import AsyncIOMotorClient
import pandas as pd
import asyncio
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.tokenize import word_tokenize
from gensim.models.phrases import Phraser
from gensim.models import Phrases
import re
from sklearn.metrics.pairwise import cosine_similarity

PHASER_THRESHOLD = 1
SAMPLE_SIZE = 300000
MAX_DF = 0.02

actual_prices = {
    "spagetti": 1.5,
    "meat balls": 6,
    "tomato sause": 1.6,
    "vodka": 17.84,
    "milk": 0.73,
    "bread": 0.70,
    "ham": 13.3,
    "porage": 0.9,
    "pizza": 3.5,
    "fryes": 1.35,
    "crisps": 5.70,
    "sossages": 6.64,
    "fish": 9.97,
    "bananas": 0.16,
    "plain flour": 0.47,
    "demorara sugar": 2.18,
    "doughnuts": 0.24,
    "cheddar cheese": 9.69,
    "soy sauce": 3.7,
    "honey": 7,
    "shreddies": 1.5,
    "dried mango": 15,
    "double decker chocolate": 1.2,
    "coca cola zero": 3.8,
    "pink lady apples": 0.44,
    "limes": 0.24,
    "blueberries": 7.93,
    "deglet nour dates": 5.98,
    "maris piper potatoes": 0.9,
    "3 red onions": 0.32,
    "brocoli": 3.97,
    "cavolo nero kale": 4.45,
    "red peppers": 0.67,
    "british wonky mushrooms": 2.6,
    "ginger": 7.92,
    "teriyaki stir fry sauce": 4.6,
    "salted butter": 7.96,
    "salted penuts": 3.73,
    "CAbinet Sauvinout wine": 49.9,
    "olive oil": 6.2,
    "vegetable stock cube": 10.30
}

async def getRandom1000():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["shoppingdb"]
    price_collection = db["prices"]

    command = [
        {"$sample": {"size": SAMPLE_SIZE}} #Finds 1000 random items
    ]

    #docs = await price_collection.aggregate(pipeline=command).to_list(None) #runs the command on the mongoDB
    docs = await price_collection.find({}).to_list(None)


    return docs

def cleanWords(word):
    return re.sub(r'[^A-Za-z ]', '', word.lower())

async def testDf(actual_prices):
    __data = pd.DataFrame(await getRandom1000()) #converts the list to a pandas dataframe
    
    mask = __data["unit"] == "g" #converts g to kg
    __data.loc[mask, "unit"] = "kg"
    __data.loc[mask, "price"] = (__data.loc[mask, "price"] * 10).round(2)

    mask = __data["unit"] == "ml"
    __data.loc[mask, "unit"] = "l"
    __data.loc[mask, "price"] = (__data.loc[mask, "price"] * 10).round(2)

    mask = __data["unit"] == "cl"
    __data.loc[mask, "unit"] = "l"
    __data.loc[mask, "price"] = ((__data.loc[mask, "price"] / 75 ) * 100).round(2)

    __data["tokens"] = [ word_tokenize(cleanWords(x)) for x in __data.name] #split up each name into tokens

    phraser = Phraser(Phrases(__data.tokens, min_count=1, threshold=PHASER_THRESHOLD)) #groups together tokens into logical phrases
    __data["phrases"] = [phraser[x] for x in __data.tokens]

    __data["normalized_name"] = __data.phrases.apply(lambda x: ' '.join(x)) #convert the tokens back into strings but similar words are joined

    dfs = [0.01, 0.02, 0.03, 0.025, 0.015]
    scores = [10000000000, 10000000000, 10000000000, 10000000000, 10000000000]
    best_df = 0
    best_score = 1000000000000000000
    for df in dfs:
        print(f"Testing df of {df}")
        vectorizer = TfidfVectorizer(
        max_df=df
        )
        X = vectorizer.fit_transform(__data.normalized_name)
        print(df, len(vectorizer.vocabulary_))
        total_score = 0
        for name, price in actual_prices.items():
            user_input = name
            user_tokens = word_tokenize(cleanWords(user_input))
            user_phrases = phraser[user_tokens]
            user_normalized = ' '.join(user_phrases)
            query = vectorizer.transform([user_normalized]) #runs same processing that was ran on the database

            __data['similarity'] = cosine_similarity(query, X).flatten()
            predicted_item = __data.sort_values('similarity', ascending=False).iloc[0]
            predicted_price = predicted_item.price
            accuracy = (price - predicted_price) ** 2 #we square the difference to punish outcomes that are further away from the expected value
            total_score += accuracy
            print(f"df: {df} item: {name}, prediction price: {predicted_price} predicted item: {predicted_item['name']}, actual:{price}, accuracy: {accuracy}")

        scores[dfs.index(df)] = total_score
        if total_score < best_score:
            best_df = df
            best_score = total_score
            print(f"New Best! new best df: {best_df} score: {best_score}")

    print("===================")
    print(f"Finished testing! Best df is {best_df} with a score of {best_score}")
    print("======================")
    for i in range(len(dfs)):
        print(f"df: {dfs[i]} score: {scores[i]}")

async def testThreshold(actual_prices):
    __data = pd.DataFrame(await getRandom1000()) #converts the list to a pandas dataframe
    
    mask = __data["unit"] == "g" #converts g to kg
    __data.loc[mask, "unit"] = "kg"
    __data.loc[mask, "price"] = (__data.loc[mask, "price"] * 10).round(2)

    mask = __data["unit"] == "ml"
    __data.loc[mask, "unit"] = "l"
    __data.loc[mask, "price"] = (__data.loc[mask, "price"] * 10).round(2)

    mask = __data["unit"] == "cl"
    __data.loc[mask, "unit"] = "l"
    __data.loc[mask, "price"] = ((__data.loc[mask, "price"] / 75 ) * 100).round(2)

    __data["tokens"] = [ word_tokenize(cleanWords(x)) for x in __data.name] #split up each name into tokens

    thresholds = [2, 4, 3, 1, 10]
    scores = [10000000000, 10000000000, 10000000000, 10000000000, 10000000000]
    best_threshold = 0
    best_score = 1000000000000000000
    for threshold in thresholds:
        print(f"Testing threshold of {threshold}")
        phraser = Phraser(Phrases(__data.tokens, min_count=1, threshold=threshold)) #groups together tokens into logical phrases
        __data["phrases"] = [phraser[x] for x in __data.tokens]
        __data["normalized_name"] = __data.phrases.apply(lambda x: ' '.join(x)) #convert the tokens back into strings but similar words are joined

        vectorizer = TfidfVectorizer(
        max_df=0.02
        )
        X = vectorizer.fit_transform(__data.normalized_name)
        total_score = 0
        for name, price in actual_prices.items():
            user_input = name
            user_tokens = word_tokenize(cleanWords(user_input))
            user_phrases = phraser[user_tokens]
            user_normalized = ' '.join(user_phrases)
            query = vectorizer.transform([user_normalized]) #runs same processing that was ran on the database

            __data['similarity'] = cosine_similarity(query, X).flatten()
            predicted_item = __data.sort_values('similarity', ascending=False).iloc[0]
            predicted_price = predicted_item.price
            accuracy = (price - predicted_price) ** 2 #we square the difference to punish outcomes that are further away from the expected value
            total_score += accuracy
            print(f"threshold: {threshold} item: {name}, prediction price: {predicted_price} predicted item: {predicted_item['name']}, actual:{price}, accuracy: {accuracy}")

        scores[thresholds.index(threshold)] = total_score
        if total_score < best_score:
            best_threshold = threshold
            best_score = total_score
            print(f"New Best! new best threshold: {best_threshold} score: {best_score}")

    print("===================")
    print(f"Finished testing! Best threshold is {best_threshold} with a score of {best_score}")
    print("======================")
    for i in range(len(thresholds)):
        print(f"threshold: {thresholds[i]} score: {scores[i]}")

async def main():
    __data = pd.DataFrame(await getRandom1000()) #converts the list to a pandas dataframe
    
    #print(__data.head())
    mask = __data["unit"] == "g" #converts g to kg
    __data.loc[mask, "unit"] = "kg"
    __data.loc[mask, "price"] = (__data.loc[mask, "price"] * 10).round(2)

    mask = __data["unit"] == "ml"
    __data.loc[mask, "unit"] = "l"
    __data.loc[mask, "price"] = (__data.loc[mask, "price"] * 10).round(2)

    mask = __data["unit"] == "cl"
    __data.loc[mask, "unit"] = "l"
    __data.loc[mask, "price"] = ((__data.loc[mask, "price"] / 75 ) * 100).round(2)

    #print(__data.head())

    __data["tokens"] = [ word_tokenize(cleanWords(x)) for x in __data.name] #split up each name into tokens
    #print(__data.tokens.head())

    
    phraser = Phraser(Phrases(__data.tokens, min_count=1, threshold=PHASER_THRESHOLD)) #groups together tokens into logical phrases
    __data["phrases"] = [phraser[x] for x in __data.tokens]


    
    #mask = __data.phrases != __data.tokens
    #print(pd.DataFrame({"s1": __data.phrases[mask], "s2": __data.tokens[mask]})) #This can be used for debugging to see what the phraser has changed
    
    __data["normalized_name"] = __data.phrases.apply(lambda x: ' '.join(x)) #convert the tokens back into strings but similar words are joined
    
    vectorizer = TfidfVectorizer(
        max_df=MAX_DF
    )
    X = vectorizer.fit_transform(__data.normalized_name) #generates a matrix of tokens representing where words are present

    user_input = "penne pasta"
    user_tokens = word_tokenize(cleanWords(user_input))
    user_phrases = phraser[user_tokens]
    user_normalized = ' '.join(user_phrases)
    query = vectorizer.transform([user_normalized]) #runs same processing that was ran on the database

    __data['similarity'] = cosine_similarity(query, X).flatten()
    top_match = __data.sort_values('similarity', ascending=False).iloc[0]
    print(top_match)
    

asyncio.run(main())
#asyncio.run(testThreshold(actual_prices))