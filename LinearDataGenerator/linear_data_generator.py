import os.path
import pickle
import ktrain
import deepl
import pandas as pd
import translators as ts
from pathlib import Path

def main():
    models_path = '..\\models'
    data_path = '..\\data'

    deepl_translator = deepl.Translator("09f9226e-2b26-7cd1-6606-9dd8b8cccf2f:fx")

    # Try loading the Sequential model located in the {models_path}
    try:
        sequential_model = ktrain.load_predictor(f'{os.getcwd()}\\{models_path}\\spam_model_sequential')
    except ImportError:
        print("Sequential model could not be imported correctly.")
    except IOError as error:
        print(f"Sequential model could not be found. {error}")

    # Try loading the Bayes model located in the {models_path} and its vectorizer located in the same folder
    try:
        bayes_model, vectorizer = pickle.load(open(f'{os.getcwd()}\\{models_path}\\spam_model_bayes.pickle', 'rb'))
    except ImportError:
        print("Bayes model could not be imported correctly.")
    except IOError:
        print("Bayes model could not be found.")

    # Load the spam dataset
    df1 = pd.read_csv(f'{os.getcwd()}\\{data_path}\\spam_1.csv', quotechar='"')
    df2 = pd.read_csv(f'{os.getcwd()}\\{data_path}\\spam_2.csv', quotechar='"')

    df = df1.append(df2[['Category','Message']], ignore_index=True)

    with open(Path(f"{os.getcwd()}\\{data_path}\\spam_results_linear.csv"), "a", encoding="utf-8") as writer:
        writer.write("Category,NNPrediction,BPrediction\n")
        for index, row in df.iterrows():
            text = row['Message']
            category = row['Category']

            # Tries to translate text to English-GB using DeepL/Bing/Yandex
            # This is done because the model has a bias for Bulgarian and considers every Bulgarian word as a spam word
            try:
                text = (deepl_translator.translate_text(text, target_lang="EN-GB")).text
            except:
                try:
                    text = ts.translate_text(text, translator='yandex')
                except:
                    try:
                        text = ts.translate_text(text)
                    except:
                        print(f"Couldn't load any translating model. Continuing without translation...")
                        pass

            # Sequential Prediction

            # Predict the class label for the text
            sequential_prediction = (sequential_model.predict_proba([text])).item(1)

            # Bayes Prediction

            # Vectorize the text
            text_vectorized = vectorizer.transform([text])

            # Predict the class label for the text
            bayes_prediction = ((bayes_model.predict_proba(text_vectorized))[:, 1]).item(0)
            
            print(f"Processing index {index}...")
            writer.write(f"{category},{sequential_prediction:.2f},{bayes_prediction:.2f}\n")

if __name__ == '__main__':
    main()