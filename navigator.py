from random import randint

class Navigator:
       def __init__(self,robot=None,logger=None):
          self.robot=robot
          self.logger=logger
       
       def generate_random_route(self,points=None,dist=100,height=5):
          rez={}
          for i in range(points):
                rez[f"Точка {i}"]={
                
                "lat": randint(-dist,dist), 
                "lon": randint(-dist,dist),
                "alt": height
                
                }
          if self.logger:
             self.logger<<f"Сгенерирован случайный маршрут{rez}"
          return rez
