import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Cargar el CSV
df = pd.read_csv("./datos/datos_balance.csv")

# Eliminar columna 'empresa' si no es numérica
df = df.drop(columns=["empresa"], errors='ignore')

# Variable objetivo: Rentabilidad2
y = df["Rentabilidad"]

# Variables de entrada: columnas de los años 2020, 2021, 2022
X = df.loc[:, df.columns.str.contains("2020|2021|2022")]

# Escalado
scaler_X = StandardScaler()
X_scaled = scaler_X.fit_transform(X)

# No escalamos y si es una variable de clasificación binaria (por ejemplo: sube o baja)
# Si es regresión (valor continuo), podrías escalar y también revertir luego
# Aquí asumimos regresión, así que escalamos:
scaler_y = StandardScaler()
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))

# Separar datos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Crear el modelo
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))  # Solo una salida: Rentabilidad2

model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=100, batch_size=16, validation_split=0.2)

# Evaluar
loss = model.evaluate(X_test, y_test)
print(f"Pérdida (MSE) en test: {loss:.4f}")

# Predecir
y_pred_scaled = model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred_scaled)
