import os.path
import pickle
import ktrain

class Connector:
    def __init__(self, models_path):
        self.models_path = models_path
        print("Connector initializing...")
        self.__load_models() 

    def __load_models(self):
        # Try loading the Sequential model located in the {models_path}
        try:
            self.sequential_model = ktrain.load_predictor(os.path.join(os.getcwd(), self.models_path, 'spam_model_sequential'))
        except ImportError:
            print("Sequential model could not be imported correctly.")
        except IOError as error:
            print(f"Sequential model could not be found. {error}")

        # Try loading the Bayes model located in the {models_path} and its vectorizer located in the same folder
        try:
            self.bayes_model, self.vectorizer = pickle.load(open(os.path.join(os.getcwd(), self.models_path, 'spam_model_bayes.pickle'), 'rb'))
        except ImportError:
            print("Bayes model could not be imported correctly.")
        except IOError:
            print("Bayes model could not be found.")
       

        try:
            self.model_combiner = pickle.load(open(os.path.join(os.getcwd(), self.models_path, 'spam_model_combiner.pickle'), 'rb'))
        except ImportError:
            print("Combiner model could not be imported correctly.")
        except IOError:
            print("Combiner model could not be found.")
            
        if self.bayes_model and self.sequential_model and self.model_combiner:
            print("+ Loaded models...")

    def get_models(self):
        # Return tuple of tuples containing models and their needed objects
        if self.sequential_model and self.bayes_model and self.model_combiner:
            return (self.sequential_model, (self.bayes_model, self.vectorizer), self.model_combiner)
        else:
            raise ConnectionError()