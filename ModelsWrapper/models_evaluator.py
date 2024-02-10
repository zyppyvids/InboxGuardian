import deepl
import numpy as np
import translators as ts
from models_connector import Connector

class Evaluator():
    def __init__(self):
        self.connector = Connector(models_path = 'models')
        self.deepl_translator = deepl.Translator("09f9226e-2b26-7cd1-6606-9dd8b8cccf2f:fx")

    def evaluate(self, text):
        try:
            (sequential_model, (bayes_model, vectorizer), model_combiner) = self.connector.get_models()
            if text:
                # Tries to translate text to English-GB using DeepL/Bing/Yandex
                # This is done because the model has a bias for Bulgarian and considers every Bulgarian word as a spam word
                try:
                    text = (self.deepl_translator.translate_text(text, target_lang="EN-GB")).text
                except:
                    try:
                        text = ts.translate_text(text, translator='yandex')
                    except:
                        try:
                            text = ts.translate_text(text)
                        except:
                            pass

                # Sequential Prediction

                # Predict the class label for the text
                sequential_prediction = (sequential_model.predict_proba([text])).item(1)

                # Bayes Prediction

                # Vectorize the text
                text_vectorized = vectorizer.transform([text])

                # Predict the class label for the text
                bayes_prediction = ((bayes_model.predict_proba(text_vectorized))[:, 1]).item(0)
                
                # Pass it through a LogisticRegression to evaluate whether it's spam or not based on the two models' predictions
                logistic_prediction = (model_combiner.predict([[(round(sequential_prediction, 2) * 100), (round(bayes_prediction, 2) * 100)]])).item(0)
                
                if logistic_prediction == 1:
                    return True
                
                return False

            else:
                print("Cannot evaluate empty text.")
        except ConnectionError:
            print("Cannot evaluate because Connector does not work.")
