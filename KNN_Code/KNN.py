# qSort programm 28.10.2020  -  Jeremias Boucsein (nach Vorlage aus Buch)
#
# Multi layered Perceptron using a sigmoid activation function and packpropagation
#
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils.validation import check_random_state


class MLP:
    def __init__(self, eta=0.03, random_state=4, iterations=100, n_input_neurons=4,
                 n_hidden_neurons=3, n_output_neurons=1):

        self.errors = []
        self.random_state = random_state
        random_state = check_random_state(self.random_state)

        self.n_input_neurons = n_input_neurons
        self.n_hidden_neurons = n_hidden_neurons
        self.n_output_neurons = n_output_neurons

        self.iterations = iterations
        self.eta = eta

        self.w_ih = []
        self.w_ho = []

        self.network = []  # Hier werden alle Werte des Netzes gespeichert

        """ --------------------------------------------------------------- """

        # Input Layer mit Nullen initialisieren
        self.inputLayer = np.zeros((self.n_input_neurons+1, 5))      # +1 für Bias
        self.inputLayer[0] = 1  # Bias

        # Hidden Layer mit Nullen initialisieren
        self.hiddenLayer = np.zeros((self.n_hidden_neurons+1, 5))    # +1 für Bias
        self.hiddenLayer[0] = 1  # Bias

        # Output Layer mit Nullen initialisieren
        self.outputLayer = np.zeros((self.n_output_neurons+1, 5))    # Bias hier nur für die Einheitlichkeit
        # ohne könnte man nicht die Matrizen rechenoperationen nutzen wenn n_output_neurons = 1 ist

        # Gewichte w_ij mit Zufallszahlen zwischen -1, 1 initialisieren
        self.w_ih = 2 * random_state.random_sample((self.n_hidden_neurons+1, self.n_input_neurons+1)) - 1
        self.w_ih[0] = 0  # Die oberste Zeile der Gewichte wird hier wieder
        # aus Gründen der Einheitlichkeit initialisiert und nicht genutzt

        # Gewichte w_ho mit Zufallszahlen zwischen -1, 1 initialisieren
        self.w_ho = 2 * random_state.random_sample((self.n_output_neurons+1, self.n_hidden_neurons+1)) - 1
        self.w_ho[0] = 0  # siehe erklärung Zeile 46/47

        self.network.append(self.inputLayer)
        self.network.append(self.w_ih)
        self.network.append(self.hiddenLayer)
        self.network.append(self.w_ho)
        self.network.append(self.outputLayer)

    def __str__(self):
        for i in self.network:
            print(i)
            print("-------------------")
        return ""

    # Sigmoid Funktion als Aktivierungsfunktion
    @staticmethod
    def func_act(x):
        return 1.0 / (1.0 + np.exp(-x))

    # Diese Funktion hat keien wirklichen Nutzen, allerdings will ich die Möglichkeit offen halten
    # eine andere Outputfunktion im Nachhinein zu implementieren.
    # Diese würde dann hier stehen
    @staticmethod
    def func_out(x):
        return x

    def predict(self, X):

        self.network[0][:, 2] = X   # Speichern des Inputs an der richtigen Stelle der Input-Layer

        """------------------------- Hidden-Layer -------------------------"""
        # Berechnen der gewichteten Summe für den Input der Hidden-Layer
        # Aus den Gewichten w_ih und dem Input
        self.network[2][1:, 0] = np.dot(self.network[1][1:, :], self.network[0][:, 2])
        # anwenden der Aktivierungsfunktion auf die Inputwerte der Hidden-Layer
        self.network[2][1:, 1] = MLP.func_act(self.network[2][1:, 0])
        # anwenden der Outputfunktion auf die Ergebnisse der Aktivierungsfunktion. Das sind die Outputs!
        self.network[2][1:, 2] = MLP.func_out(self.network[2][1:, 1])
        # berechnen der Steigung (durch die Ableitung der Aktivierungsfunktion, hier der Signoiden)
        # für die Backpropagation
        self.network[2][1:, 3] = self.network[2][1:, 2] * (1.0 - self.network[2][1:, 2])

        """------------------------- Output-Layer -------------------------"""
        # Erklärung siehe Dokumentierung Hidden-Layer
        self.network[4][1:, 0] = np.dot(self.network[3][1:, :], self.network[2][:, 2])
        self.network[4][1:, 1] = MLP.func_act(self.network[4][1:, 0])
        self.network[4][1:, 2] = MLP.func_out(self.network[4][1:, 1])
        self.network[4][1:, 3] = self.network[4][1:, 2] * (1.0 - self.network[4][1:, 2])

        return self.network[4][1:, 2]

    def fit(self, training_data):
        # für den Plot

        for iteration in range(self.iterations):

            error = 0.0

            for i in range(len(training_data)):
                x = training_data[i][0]
                y = training_data[i][1]

                # Errechnen des Outputs des Netzes
                y_hat = self.predict(x)

                # Differenz zum Sollwert
                diff = y - y_hat

                # Quadratische Fehler für den Plot
                # sum wird benutzt um sicher zu gehen, dass ein Wert raus kommt.
                # Da diff eine Matrix ist, wenn es mehr als nur ein Output Neuron gibt
                error += 0.5 * np.sum(diff * diff)

                # Berechnen von delta_w der Output-Layer Neuronen
                # Nach der Formel: delta_wo = out * (1 - out) * (y - y_hat)
                self.network[4][1:, 4] = self.network[4][1:, 3] * diff

                # Berechnen von delta_w der Hiddden-Layer Neuronen
                # nach der Formel: delta_wh = out * (1 - out) * Skalarprodukt(w_ho, delta_wo)
                self.network[2][:, 4] = self.network[2][:, 3] * np.dot(self.network[3][:].T, self.network[4][:, 4])

                # Berechnen von Delta_w der Gewichte von der Hidden- zur Output-Layer
                delta_w_ho = self.eta * np.outer(self.network[4][:, 4], self.network[2][:, 2].T)

                # Berechnen von Delta_w der Gewichte von der Input- zur Hidden-Layer
                delta_w_ih = self.eta * np.outer(self.network[2][:, 4], self.network[0][:, 2].T)

                # Anpassen der Gewichte
                self.network[3][:] += delta_w_ho
                self.network[1][:] += delta_w_ih

            self.errors.append(error)

    def plot(self):
        fignr = 1
        plt.figure(fignr, figsize=(5, 5))

        plt.plot(self.errors)

        plt.style.use("seaborn-whitegrid")
        plt.xlabel("iterations")
        plt.ylabel("Fehler")
        plt.savefig('Plot_MLP.pdf')

        
if __name__ == '__main__':
    data_in = [
        (np.array([1, 0, 0, 0, 0]), 0),
        (np.array([1, 0, 1, 0, 1]), 0),
        (np.array([1, 1, 0, 1, 0]), 1),
        (np.array([1, 0, 1, 0, 1]), 0),
        (np.array([1, 1, 0, 1, 0]), 1),
        (np.array([1, 0, 1, 0, 1]), 1),
        (np.array([1, 1, 0, 1, 1]), 1),
        (np.array([1, 0, 1, 1, 1]), 1)
    ]

    knn = MLP(eta=0.03, iterations=30000)

    knn.fit(data_in)

    knn.plot()

    kepp = True
    while kepp:
        s = None
        while True:
            s = input("Input(erster Wert muss 1 sein)(für Stop (S)): ")
            if s == "S" or s == "s":
                kepp = False
            s = list(s)
            try:
                for i in range(len(s)):
                    s[i] = int(s[i])
                break
            except ValueError:
                if kepp:
                    print("nochmal")
                else:
                    break

        if s[0] != "S" and s[0] != "s":
            t = np.array(s)
            erg = knn.predict(t)
            print("Ergebnis:", erg)
        
