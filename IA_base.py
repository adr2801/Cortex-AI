import numpy as np

class PrioriseurIA :
    def __init__(self):
        self.w1 = np.random.randn(5, 16)*0.09 # Poids de la première couche
        self.w2 = np.random.randn(16, 1)*0.09 # Poids de la deuxième couche
        self.b1 = np.zeros((1, 16)) # Biais de la première couche
        self.b2 = np.zeros((1, 1))
        
    def sigmoid(self, x):
        x = np.clip(x, -500, 500)
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def forward(self, X):
        self.z1 = np.dot(X, self.w1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.w2) + self.b2
        self.output = self.sigmoid(self.z2)
        return self.output
    
    def train(self, X, y, epochs=100000, lr=0.1):
        intervalle = 1000
        for epoch in range(epochs):
            #if epoch > 10000:
                #lr = 0.1 * (1 - epoch/epochs) # Diminution du taux d'apprentissage au fil des époques
            #Forward pass
            output = self.forward(X)
            
            # Calcule de l'erreur
            n = len(X)
            error = (1/n) * np.sum(np.square(output- y))
            
            # Backpropagation
            d_output = (output - y) * self.sigmoid_derivative(output)
            error_hidden = np.dot(d_output, self.w2.T)
            d_hidden = error_hidden * self.sigmoid_derivative(self.a1)
            if epoch % intervalle == 0:
                print(f"Epoch {epoch} Error: {error}")
            
            # mise a jour des poids et biais
            # Un facteur de "pression" pour garder les poids petits
            decay = 0.0022

            # Mise à jour des poids avec freinage intégré
            self.w2 -= self.a1.T.dot(d_output) * lr
            self.b2 -= np.sum(d_output, axis=0, keepdims=True) * lr
            self.w1 -= X.T.dot(d_hidden) * lr
            self.b1 -= np.sum(d_hidden, axis=0, keepdims=True) * lr

            #bloque l'explosion des poids
            self.w1 = np.clip(self.w1, -4, 4)
            self.w2 = np.clip(self.w2, -4, 4)
            if epoch % intervalle == 0:
                print(f"Epoch {epoch} Weights1: {self.w1[0]} Weights2: {self.w2[0]} lr = {lr}")
                print(f"Somme des poids W1 : {np.sum(np.abs(self.w1))}")
            # Sauvegarde des poids
        np.save('weights1.npy', self.w1)
        np.save('weights2.npy', self.w2)

        # Sauvegarde des biais
        np.save('bias1.npy', self.b1)
        np.save('bias2.npy', self.b2)

        print("Cerveau sauvegardé avec succès ! 🧠💾")
    def reset_weights(self):
        # On relance l'initialisation aléatoire (Xavier/Glorot)
        self.w1 = np.random.randn(5, 8) * np.sqrt(1. / 5)
        self.b1 = np.zeros((1, 8))
        
        self.w2 = np.random.randn(8, 1) * np.sqrt(1. / 8)
        self.b2 = np.zeros((1, 1))
        print("Cerveau réinitialisé ! Retour à zéro.")

X_train = np.array([[0.0, 0.0, 1.0, 0.4, 1.0], [0.5, 0.5, 0.5, 0.5, 0.5], # Tes ancres
    [1.0, 1.0, 0.1, 1.0, 1.0], [0.9, 0.8, 0.2, 0.7, 0.9], # Très haute priorité
    [0.1, 0.1, 0.8, 0.2, 0.3], [0.2, 0.1, 0.9, 0.1, 0.4], # Très basse priorité
    [0.8, 0.2, 0.1, 0.9, 0.8], [0.2, 0.8, 0.5, 0.4, 0.6], # Priorités moyennes
    [0.7, 0.7, 0.3, 0.8, 0.7], [0.1, 0.9, 0.8, 0.5, 0.4],
    [0.9, 0.1, 0.2, 0.6, 0.5], [0.4, 0.4, 0.4, 0.4, 0.4],
    [0.6, 0.6, 0.6, 0.6, 0.6], [1.0, 0.5, 0.1, 0.3, 0.9],
    [0.2, 0.2, 0.2, 0.2, 0.2], [0.8, 0.8, 0.8, 0.8, 0.8],
    [0.3, 0.7, 0.2, 0.9, 0.5], [0.7, 0.3, 0.1, 0.5, 1.0],
    [0.0, 1.0, 0.5, 0.2, 0.4], [1.0, 0.0, 0.1, 0.8, 0.6],
    [0.5, 0.9, 0.2, 0.7, 0.8], [0.9, 0.5, 0.4, 0.2, 0.3],
    [0.1, 0.3, 0.5, 0.7, 0.9], [0.3, 0.1, 0.9, 0.4, 0.2],
    [0.6, 0.2, 0.3, 0.8, 0.5], [0.2, 0.6, 0.7, 0.1, 0.4],
    [0.8, 0.9, 0.1, 0.1, 1.0], [0.4, 0.8, 0.3, 0.6, 0.5],
    [0.7, 0.4, 0.2, 0.9, 0.7], [0.5, 0.1, 0.8, 0.3, 0.2],
    [0.9, 0.9, 0.5, 0.5, 0.5], [0.1, 0.1, 0.1, 0.1, 0.1],
    [0.2, 0.3, 0.4, 0.5, 0.6], [0.6, 0.5, 0.4, 0.3, 0.2],
    [0.7, 0.8, 0.9, 1.0, 1.0], [0.3, 0.2, 0.1, 0.0, 0.0],
    [0.5, 0.7, 0.3, 0.4, 0.9], [0.8, 0.5, 0.2, 0.1, 0.6],
    [0.4, 0.2, 0.7, 0.8, 0.3], [0.9, 0.3, 0.1, 0.5, 0.8],
    [0.1, 0.8, 0.4, 0.2, 0.5], [0.6, 0.9, 0.2, 0.7, 0.4],
    [1.0, 1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0, 0.0],
    [0.5, 0.2, 0.9, 0.1, 0.3], [0.3, 0.8, 0.4, 0.6, 0.7],
    [0.7, 0.1, 0.2, 0.5, 0.9], [0.2, 0.9, 0.5, 0.8, 0.1],
    [0.9, 0.4, 0.3, 0.2, 1.0], [0.4, 0.6, 0.8, 0.9, 0.2],
    [0, 0, 1, 0.4, 1],[0, 0, 1, 0.4, 1],[0, 0, 1, 0.4, 1],[0, 0, 1, 0.4, 1]]) # Entrées d'entraînement
y_train = np.array([[0.02], [0.50], [0.98], [0.85], [0.05], [0.08], [0.45], [0.55], # 8 premiers
    [0.75], [0.40], [0.42], [0.40], [0.60], [0.65], [0.20], [0.80], # 16
    [0.62], [0.52], [0.48], [0.45], [0.78], [0.55], [0.35], [0.15], # 24
    [0.43], [0.32], [0.88], [0.65], [0.68], [0.18], [0.92], [0.10], # 32
    [0.38], [0.45], [0.82], [0.12], [0.62], [0.58], [0.35], [0.65], # 40
    [0.42], [0.72], [0.99], [0.01], [0.22], [0.68], [0.38], [0.65], # 48
    [0.60], [0.48],[0.02],[0.02],[0.02],[0.02]]) # Sorties d'entraînement



ia = PrioriseurIA()
#ia.reset_weights()
try:
    ia.w1 = np.load('weights1.npy')
    ia.w2 = np.load('weights2.npy')
    ia.b1 = np.load('bias1.npy')
    ia.b2 = np.load('bias2.npy')
    print("Reprise de l'entraînement à partir des poids sauvegardés...")
except FileNotFoundError:
    print("Aucune sauvegarde trouvée, démarrage de zéro.")
#ia.train(X_train, y_train)

# Test : Urgence Moyenne(0.5), Importante(0.8), Courte(0.2), Envie(0.9), Énergie(0.7)
#test_input = np.array([[0.5, 0.8, 0.2, 0.9, 0.7]]) 
#prediction = ia.forward(test_input)
#print(ia.w1[0][0])
#print(ia.b2[0][0])
#print(f"Pour cette nouvelle tâche, l'IA prédit un score de : {prediction[0][0]:.4f}")