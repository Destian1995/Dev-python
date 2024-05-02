#Список статистики игроков (Kills/Death/Assistance)
kda = [2.44,2.1,1.22,1.33,1.45,1.51,0.76,0.98,2.12,1.34,1.14,1.41, 2.32, 3.01, 2.29, 1.86]
kda_avg = sum(kda)/len(kda)

#Добавление бота если игроков нечетное количество
if len(kda)%2 != 0:
     kda.append(round(kda_avg))

#Отсечение смурфов
kda = sorted(kda)
rang_low = kda[:int(len(kda)/2)]
rang_high = kda[int(len(kda)/2):]

#Балансировка low команд
rang_low_team1 = rang_low[:int(len(rang_low)/2)]  
rang_low_team2 = rang_low[int(len(rang_low)/2):]
for i in range(len(rang_low_team1)):
    temp = rang_low_team1[i]
    rang_low_team1[i] = rang_low_team2[i]
    rang_low_team2[i] = temp
    result1 = sum(rang_low_team1)/len(rang_low_team1)
    result2 = sum(rang_low_team2)/len(rang_low_team2)
    if (result1*100)/result2 >= 90:
          break
#Балансировка high команд
rang_high_team1 = rang_high[:int(len(rang_high)/2)]  
rang_high_team2 = rang_high[int(len(rang_high)/2):]
for i in range(len(rang_high_team1)):
    temp = rang_high_team1[i]
    rang_high_team1[i] = rang_high_team2[i]
    rang_high_team2[i] = temp
    result1 = sum(rang_high_team1)/len(rang_high_team1)
    result2 = sum(rang_high_team2)/len(rang_high_team2)
    if (result1*100)/result2 >= 90:
          break
#Итог балансировки команд:
print("low команды:\n","Команда 1: \n",rang_low_team1,"\n Команда 2: \n", rang_low_team2)
print("high команды:\n","Команда 1: \n",rang_high_team1,"\n Команда 2: \n", rang_high_team2)
