from ANNarchy import *
from ANNarchy.extensions.bold import *
from extras import startMonitors, getMonitors
from model_neuronmodels import newBoldNeuron
import pylab as plt

## PARAMS
simParams={}
simParams['sim_dur1'] = 5000
simParams['sim_dur2'] = 20000
simParams['sim_dur3'] = 20000
simParams['dt'] = 0.1
setup(dt=simParams['dt'])


### ONE SPIKING NEURON WHERE TWO VARIABLES CAN BE SET
## NEURON MODEL
aux_neuron = Neuron(
    parameters="""
    """,
    equations = """
        v=0
        da/dt=0
        db/dt=0
    """,
    spike = """
        v>10
        """,
    reset = """
        v=0
    """
)
## POPULATION
pop = Population(1, neuron=aux_neuron, name='aux_pop')


### BOLD MONITORS
monB = {}
monB['1'] = BoldMonitor(populations=pop,
                  input_variables="a",
                  recorded_variables=["BOLD", "I_CBF", "s_CBF", "f_in", "E", "q", "v", "f_out"])
monB['2'] = BoldMonitor(populations=pop,
                  input_variables=["a", "b"],
                  output_variables=["I_f","I_r"],
                  bold_model=newBoldNeuron,
                  recorded_variables=["I_CBF","I_CMRO2","s_CBF","s_CMRO2","f_in","r","v","q","f_out","BOLD"])
                  
### GENERATE monDict for BOLDMonitors, to easier start and get the monitors
monDictB={'BOLD;1': ["BOLD", "I_CBF", "s_CBF", "f_in", "E", "q", "v", "f_out"],
          'BOLD;2': ["I_CBF","I_CMRO2","s_CBF","s_CMRO2","f_in","r","v","q","f_out","BOLD"]}


### COMPILE            
compile('annarchy_fig_Balloon_model')



### SIMULATE
## START BOLD MONITORS
startMonitors(monDictB,monB)

## ACTUAL SIMULATION
simulate(simParams['sim_dur1'])
pop.a=0.2
pop.b=0.05
simulate(simParams['sim_dur2'])
pop.a=0
pop.b=0
simulate(simParams['sim_dur3'])


### GET MONITORS
recordingsB={}
recordingsB=getMonitors(monDictB,monB,recordingsB)


### SAVE DATA
np.save('../dataRaw/Fig_Balloon_model_data_recordingsB.npy',recordingsB)
np.save('../dataRaw/Fig_Balloon_model_data_simParams.npy',simParams)
