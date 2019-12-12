'''
bear-rabbit Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo bear rabbit Predation model.
    http://ccl.northwestern.edu/netlogo/models/bearrabbitPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
'''

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agents import Rabbit, Bear, GrassPatch, Hunter
from schedule import RandomActivationByBreed


class HuntersModel(Model):



    description = 'A model for simulating bear and rabbit (predator-prey) ecosystem modelling.'

    def __init__(self, height=25, width=25,
                 initial_rabbit=100, initial_bears=50,
                 rabbit_reproduce=0.2, bear_reproduce=0.1,
                 bear_gain_from_food=10, verbose=False,
                 grass=False, grass_regrowth_time=15, rabbit_gain_from_food=5,
                 initial_hunter = 10, hunter_gain_from_rabbit = 5,hunter_welafre_list = [],
                 hunter_gain_form_bear = 10,extinction_punishment = -1000,
                 hunting_season_start = 1, hunting_season_end = 5):
        # Note:  always 1 =< hunting_season_start =< hunting_season_end <= 10
        '''
        Create a new bear-rabbit model with the given parameters.

        Args:
            initial_rabbit: Number of rabbit to start with
            initial_bears: Number of bears to start with
            rabbit_reproduce: Probability of each rabbit reproducing each step
            bear_reproduce: Probability of each bear reproducing each step
            bear_gain_from_food: Energy a bear gains from eating a rabbit
            grass: Whether to have the rabbit eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            rabbit_gain_from_food: Energy rabbit gain from grass, if enabled.
        '''
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_rabbit = initial_rabbit
        self.initial_bears = initial_bears
        self.rabbit_reproduce = rabbit_reproduce
        self.bear_reproduce = bear_reproduce
        self.bear_gain_from_food = bear_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.rabbit_gain_from_food = rabbit_gain_from_food
        self.hunter_gain_from_rabbit = hunter_gain_from_rabbit
        self.hunter_gain_from_bear = hunter_gain_form_bear
        self.initial_hunter = initial_hunter
        self.hunter_welfare_list = hunter_welafre_list
        self.extinction_punishment = extinction_punishment
        self.hunting_season_start = hunting_season_start
        self.hunting_season_end = hunting_season_end
        self.verbose = verbose

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {"bears": lambda m: m.schedule.get_breed_count(Bear),
             "rabbit": lambda m: m.schedule.get_breed_count(Rabbit),
             "total_welfare" : lambda m: m.sum_welfare(),
             "average_welfare": lambda m: m.average_welfare()
             })





        # Create hunter:
        self.hunter_welfare_list = []
        for i in range(self.initial_hunter):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = 5
            hunter = Hunter(self.next_id(), (x, y), self, True, energy, welfare=0)
            self.hunter_welfare_list.append(hunter.welfare)
            self.grid.place_agent(hunter, (x, y))
            self.schedule.add(hunter)



        # Create rabbit:
        for i in range(self.initial_rabbit):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.rabbit_gain_from_food)
            rabbit = Rabbit(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(rabbit, (x, y))
            self.schedule.add(rabbit)

        # Create bears
        for i in range(self.initial_bears):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.bear_gain_from_food)
            bear = Bear(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(bear, (x, y))
            self.schedule.add(bear)

        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = self.random.randrange(self.grass_regrowth_time)

                patch = GrassPatch(self.next_id(), (x, y), self,
                                   fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def sum_welfare(self):
        if self.schedule.get_breed_count(Bear) > 0 and self.schedule.get_breed_count(Rabbit) > 0:
            return sum(self.hunter_welfare_list)
        else:
            return  sum(self.hunter_welfare_list)+ self.extinction_punishment * self.initial_hunter


    def average_welfare(self):
       if self.schedule.get_breed_count(Bear) > 0 and self.schedule.get_breed_count(Rabbit) > 0:

           return self.sum_welfare()/self.initial_hunter
       else:
           return self.sum_welfare()/self.initial_hunter



    def step(self):

        self.schedule.step()
        #print(self.hunter_welfare_list)
        #print('total welfare is ', self.sum_welfare())
       # print(self.schedule.time)

        #print('average welfare is', self.average_welfare())
        # collect data
        self.datacollector.collect(self)

        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(Bear),
                   self.schedule.get_breed_count(Rabbit)])

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number bears: ',
                  self.schedule.get_breed_count(Bear))
            print('Initial number rabbit: ',
                  self.schedule.get_breed_count(Rabbit))

        for i in range(step_count):
            self.step()


        if self.verbose:
            print('')
            print('Final number bears: ',
                  self.schedule.get_breed_count(Bear))
            print('Final number rabbit: ',
                  self.schedule.get_breed_count(Rabbit))
