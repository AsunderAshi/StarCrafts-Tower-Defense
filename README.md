#Игра «Tower Defense»:
Версия 1.2
Автор: Шишкин Антон (shishkinanton14@gmail.com)

#Описание:
Данное приложение является реализацией игры «Tower Defense»

#Требования:
1. Python версии не ниже 3.4
2. Библиотека json
3. PyQt версии 5

#Состав:
1. Графическая версия – Gameboard.py
2. Описание башен – Towers.py
3. Описание врагов – enemy.py
4. Глобальные переменные – globals.py
5. Текстуры – Textures/
6. Описание волн – Waves.json

#Графическая версия:
Запуск – “Gameboard.py”

#Подробности реализации:
Игра состоит из одной карты и двух волн монстров.
Целью игры является – не дать более чем пяти монстрам завершить свой путь.
Чтобы помешать им сделать это, необходимо строить башни, атакующие их. Размещение баше возможно в ячейках, не занятых другой башней и не лежащих на пути врага.
Доступные башни:
1. Marine:
	Урон – 50
	Дальность выстрела – 100
	Цена – 100
	Цена продажи – 75
2. Marauder:
	Урон – 75
 	Дальность выстрела – 100
	Цена – 200
	Цена продажи – 150
3. Siege Tank:
	Урон – 300
	Дальность выстрела – 200
	Цена – 500
	Цена продажи – 250
4. Ghost:
	Урон – 100
	Дальность выстрела – 100
	Цена – 150
	Цена продажи - 110
