from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from agents import Bear, Rabbit, GrassPatch, Hunter
from model import HuntersModel


def hunters_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Rabbit:
        portrayal["Shape"] = "resources/rabbit.png"

        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Bear:
        portrayal["Shape"] = "resources/bear.png"

        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is Hunter:
        portrayal['Shape'] = "resources/hunter.png"
        portrayal['scale'] = 0.9
        portrayal['Layer'] = 1.5
        portrayal['text_color'] = 'Red'

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(hunters_portrayal, 25, 25, 500, 500)
chart_element = ChartModule([{"Label": "bears", "Color": "#AA0000"},
                             {"Label": "rabbit", "Color": "#666666"},
                             {"Label": "total_welfare","Color": 'green'},
                             {"Label": "average_welfare", "Color": 'blue'}])

model_params = {"grass": UserSettableParameter('checkbox', 'Grass Enabled', True),
                "grass_regrowth_time": UserSettableParameter('slider', 'Grass Regrowth Time', 15, 1, 50),
                "initial_rabbit": UserSettableParameter('slider', 'Initial rabbit Population', 100, 10, 300),
                "rabbit_reproduce": UserSettableParameter('slider', 'rabbit Reproduction Rate', 0.2, 0.01, 1.0,
                                                         0.01),
                "hunting_season_start": UserSettableParameter('slider', 'hunting_season_start', 1, 1, 10),
                "hunting_season_end": UserSettableParameter('slider', "hunting_season_end", 5, 1,10),
                "initial_bears": UserSettableParameter('slider', 'Initial bear Population', 50, 10, 300),
                'initial_hunter':UserSettableParameter('slider', 'Initial hunter num', 10, 0, 100, 5),
                "bear_reproduce": UserSettableParameter('slider', 'bear Reproduction Rate', 0.1, 0.01, 1.0,
                                                        0.01,
                                                        description="The rate at which bear agents reproduce."),
                "bear_gain_from_food": UserSettableParameter('slider', 'bear Gain From Food Rate', 20, 1, 50),
                "rabbit_gain_from_food": UserSettableParameter('slider', 'rabbit Gain From Food', 5, 1, 10)}

server = ModularServer(HuntersModel, [canvas_element, chart_element], "Hunters", model_params)
server.port = 8522
