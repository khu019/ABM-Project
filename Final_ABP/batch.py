
from model import *
from agents import *
import  pickle

import  matplotlib.pyplot as plt
from mesa.batchrunner import  BatchRunner


iterations = 10
max_steps = 200

fixed_params = {

'grass': True
}

variable_params = {'initial_hunter': range(5,30,5),
                   'hunting_season_end':range(1, 11, 1)
                   }

batchrun = BatchRunner(
    model_cls= HuntersModel,
    fixed_parameters= fixed_params,
    variable_parameters= variable_params,
    iterations = iterations,
    max_steps= max_steps,
    model_reporters={
        'average_welfare': lambda m: m.average_welfare(),
    },
    agent_reporters= None,
    display_progress= True
)
batchrun.run_all()

#batchdata = batchrun.get_model_vars_dataframe()
data2 = batchrun.get_model_vars_dataframe()

#print(batchdata.head())
#batchdata.head()

plt.scatter(data2.hunting_season_end, data2.average_welfare)
plt.xlabel('hunting_season_end')
plt.ylabel('average_welfare')

def savefile(obj,file):
    with open(file,'wb') as f:
        pickle.dump(obj,f,pickle.HIGHEST_PROTOCOL)

def loadfile(obj,file):
    with open(file,'rb') as f:
        obj = pickle.load(f)

savefile(obj=data2,file='data2.pkl')

with open('data2.pkl','rb') as f:
    result = pickle.load(f)

print(result)











