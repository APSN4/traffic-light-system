Road_len = 100
N = 3
cars = []
Dev_mode = False # Режим разработчика [Откладка]

class TRoad:
    def __init__(self, length0, width0):
        if length0 > 0:
            self.length = length0
        else:
            self.length = 0
        if width0 > 0:
            self.width = width0
        else:
            self.width = 0
        # модель светофора
        self.tr_light_condition = 0 # состояние [0:зеленый, 1:желтый, 2:красный]
        self.pos_tr_light = Road_len//3 # координата светофора
        self.switcher = 0 # switcher варьируется [0-5] секунд
        self.sequence_up = False  # порядок сигналов светофора [...зеленый-желтый-красный-желтый-зеленый...]

    def tr_light_switcher(self):
        road.switcher += 1
        if road.tr_light_condition == 0 and road.switcher == 5: # Зеленый сигнал
            road.tr_light_condition = 1
            road.switcher = 0
            if Dev_mode == True:
                print("[Светофор] Зеленый")
        elif road.tr_light_condition == 1 and road.switcher == 1: # Желтый сигнал
            if road.sequence_up == False:
                road.tr_light_condition = 2
            else:
                road.tr_light_condition = 0
                road.sequence_up = False
            road.switcher = 0
            if Dev_mode == True:
                print("[Светофор] Желтый")
        elif road.tr_light_condition == 2 and road.switcher == 5: # Красный сигнал
            road.tr_light_condition = 1
            road.sequence_up = True
            road.switcher = 0
            if Dev_mode == True:
                print("[Светофор] Красный")

road = TRoad(60, 3)

class TCar:
    def __init__ ( self, road0, p0, v0 ):
        self.road = road0
        self.P = p0 # номер полосы
        self.V = v0 # скорость
        self.X = 0 # координата
        self.pass_tr_light = False # Если [self.X + self.V > road.pos_tr_light] выполнено уже 1 раз, то мы проехали светофор
        self.is_stopped = False
    def move(self):
        if self.is_stopped == False:
            self.X += self.V
        if self.X > self.road.length:
            self.X = 0
            self.pass_tr_light = False
            print("--------")
            print("Машина начала движение с [X = 0]")
    def tr_light_checker(self):
        if self.X == road.pos_tr_light or self.X + self.V > road.pos_tr_light and self.pass_tr_light == False:
            if road.tr_light_condition == 0:
                self.is_stopped = False
                print("Машина проехала на зеленый")
                self.pass_tr_light = True
            elif road.tr_light_condition == 1:
                print("Водитель видит желтый")
                self.pass_tr_light = True
            elif road.tr_light_condition == 2:
                self.is_stopped = True
                print("Машина остановилась на красный")
    def post_to_tr_light(self):
        road.tr_light_switcher()

# Основной блок кода

for i in range(N):
    cars.append(TCar(road, i+1, 2*(i+1))) # 2*(i+1) [скорость из задачки]

for k in range(Road_len):
    for i in range(N): #было (N):
        cars[i].post_to_tr_light()
        cars[i].tr_light_checker()
        cars[i].move()

        print("Машина: " + str(i + 1) + " | координата: " + str(cars[i].X) + " | " + str(road.switcher))
print("После 100 шагов (Предположим шаг = 1 секунде)")
for i in range(N):
    print("Машина: " + str(i+1) + " | координата: " + str(cars[i].X))