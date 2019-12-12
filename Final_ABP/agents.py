from mesa import Agent
from random_walk import RandomWalker

class Hunter(RandomWalker):
    def __init__(self,unique_id,pos,model,moore,energy = 5,welfare = 0 ):
        super().__init__(unique_id,pos,model,moore=moore)

        self.energy = energy
        self.welfare = welfare


    def step(self):
        self.random_move()


        # always kill bear first if available, then rabbit.
        if self.model.hunting_season_start-1 <= self.model.schedule.time % 10 <= self.model.hunting_season_end-1:
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            rabbit = [obj for obj in this_cell if isinstance(obj, Rabbit)]
            bear = [obj for obj in this_cell if isinstance(obj, Bear)]
            if len(bear) > 0:
                bear_to_kill = self.random.choice(bear)
                self.welfare += self.model.hunter_gain_from_bear
                self.model.grid._remove_agent(self.pos, bear_to_kill)
                self.model.schedule.remove(bear_to_kill)
               # print('welfare of hunter', self.unique_id, '=',self.welfare)
                self.model.hunter_welfare_list[self.unique_id-1] = self.welfare


            elif len(rabbit) > 0:
                rabbit_to_kill = self.random.choice(rabbit)
                self.welfare += self.model.hunter_gain_from_rabbit
                self.model.grid._remove_agent(self.pos, rabbit_to_kill)
                self.model.schedule.remove(rabbit_to_kill)
                #print('welfare of hunter', self.unique_id, '=', self.welfare)

                self.model.hunter_welfare_list[self.unique_id - 1] = self.welfare



        # leaving:
        else:
            #IMHULKprint('welfare of hunter', self.unique_id, '=', self.welfare)
            self.model.hunter_welfare_list[self.unique_id - 1] = self.welfare











class Rabbit(RandomWalker):
    '''
    A rabbit that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    '''

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        '''
        A model step. Move, then eat grass and reproduce.
        '''
        self.random_move()
        living = True

        if self.model.grass:
            # Reduce energy
            self.energy -= 1

            # If there is grass available, eat it
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [obj for obj in this_cell
                           if isinstance(obj, GrassPatch)][0]
            if grass_patch.fully_grown:
                self.energy += self.model.rabbit_gain_from_food
                grass_patch.fully_grown = False
             # Death
            if self.energy <= 0:
                    self.model.grid._remove_agent(self.pos, self)
                    self.model.schedule.remove(self)
                    living = False
                    #print('rabbit', self.unique_id, 'died')


        if living and self.random.random() < self.model.rabbit_reproduce:
            # Create a new rabbit:
            if self.model.grass:
                self.energy /= 2
            lamb = Rabbit(self.model.next_id(), self.pos, self.model,
                         self.moore, self.energy)
            self.model.grid.place_agent(lamb, self.pos)
            self.model.schedule.add(lamb)




class Bear(RandomWalker):
    '''
    A bear that walks around, reproduces (asexually) and eats rabbit.
    '''

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1

        # If there are rabbits present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        rabbit = [obj for obj in this_cell if isinstance(obj, Rabbit)]
        if len(rabbit) > 0:
            rabbit_to_eat = self.random.choice(rabbit)
            self.energy += self.model.bear_gain_from_food

            # Kill the rabbit
            self.model.grid._remove_agent(self.pos, rabbit_to_eat)
            self.model.schedule.remove(rabbit_to_eat)

        # Death or reproduction
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.bear_reproduce:
                # Create a new bear cub
                self.energy /= 2
                cub = Bear(self.model.next_id(), self.pos, self.model,
                           self.moore, self.energy)
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)


class GrassPatch(Agent):
    '''
    A patch of grass that grows at a fixed rate and it is eaten by rabbit
    '''

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        '''
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        '''
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1

