import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Загрузка данных из файла
data = pd.read_csv(r'C:\Users\User\Desktop\test\data.csv', delimiter=';', header=None)
new_data = input("Сколько данных нужно будет обработать?: ")
# Разделение данных на входные и выходные
X = data.iloc[:, 0]  # Входные данные (первый столбец)
y_hours_minutes = data.iloc[:, 1]  # Выходные данные (второй столбец)

# Преобразование времени из часов и минут в десятичную дробь
def convert_time(time_str):
    hours, minutes = map(float, time_str.split('.'))
    return hours + minutes / 60

y = y_hours_minutes.apply(lambda x: convert_time(str(x)))

# Масштабирование входных данных
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X.values.reshape(-1, 1))

# Разделение данных на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Создание модели нейронной сети
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(1,)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Обучение модели
model.fit(X_train, y_train, epochs=10000, batch_size=32, verbose=2)

# Оценка производительности модели
mse = model.evaluate(X_test, y_test)
print(f'Производительность модели: {mse}')

# Прогнозирование выходных значений
new_data_scaled = scaler.transform(np.array([new_data]).reshape(-1, 1))
prediction = model.predict(new_data_scaled)
hours = int(prediction[0][0])
minutes = int((prediction[0][0] - hours) * 60)
print(f'Прогноз времени обработки данных: {hours} часов {minutes} минут')
