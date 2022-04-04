import numpy as np
import torch
#import rvo2
from crowd_sim.envs.policy.policy import Policy
from crowd_sim.envs.utils.action import ActionXY

from crowd_sim.envs.policy.socialforce import Simulator, PedPedPotential
from crowd_sim.envs.policy.socialforce.fieldofview import FieldOfView
# should be covered
# from ../../../../socialforce.potentials import PedPedPotential
# from ../../../../socialforce.fieldofview import FieldOfView


class SF(Policy):
    def __init__(self):
        """
        timeStep        The time step of the simulation.
                        Must be positive.
        neighborDist    The default maximum distance (center point
                        to center point) to other agents a new agent
                        takes into account in the navigation. The
                        larger this number, the longer the running
                        time of the simulation. If the number is too
                        low, the simulation will not be safe. Must be
                        non-negative.
        maxNeighbors    The default maximum number of other agents a
                        new agent takes into account in the
                        navigation. The larger this number, the
                        longer the running time of the simulation.
                        If the number is too low, the simulation
                        will not be safe.
        timeHorizon     The default minimal amount of time for which
                        a new agent's velocities that are computed
                        by the simulation are safe with respect to
                        other agents. The larger this number, the
                        sooner an agent will respond to the presence
                        of other agents, but the less freedom the
                        agent has in choosing its velocities.
                        Must be positive.
        timeHorizonObst The default minimal amount of time for which
                        a new agent's velocities that are computed
                        by the simulation are safe with respect to
                        obstacles. The larger this number, the
                        sooner an agent will respond to the presence
                        of obstacles, but the less freedom the agent
                        has in choosing its velocities.
                        Must be positive.
        radius          The default radius of a new agent.
                        Must be non-negative.
        maxSpeed        The default maximum speed of a new agent.
                        Must be non-negative.
        velocity        The default initial two-dimensional linear
                        velocity of a new agent (optional).

        ORCA first uses neighborDist and maxNeighbors to find neighbors that need to be taken into account.
        Here set them to be large enough so that all agents will be considered as neighbors.
        Time_horizon should be set that at least it's safe for one time step

        In this work, obstacles are not considered. So the value of time_horizon_obst doesn't matter.

        """
        super().__init__()
        self.name = 'sf'
        self.trainable = False
        self.multiagent_training = None
        self.kinematics = 'holonomic'
        self.safety_space = 0
        self.neighbor_dist = 10
        self.max_neighbors = 10
        self.time_horizon = 5
        self.time_horizon_obst = 5
        self.radius = 0.3
        self.max_speed = 1
        self.sim = None

    # Taken from https://github.com/vita-epfl/trajnetplusplusdataset/blob/6364550049d12336ef077dc12c1b9721f2182af5/trajnetdataset/controlled_data.py#L18
    # No equivalent in ORCA
    # TODO: should this be its own utils file? should this be called get_circle_crossing
    # probably shouldn't use; this creates a circle crossing from nothing, and this class is to be used in an extant env
    def generate_circle_crossing(self, num_ped, sim=None, radius=4, mode=None):
        positions = []
        goals = []
        speed = []
        agent_list = []
        if mode == 'trajnet':
            radius = 10 ## 10 (TrajNet++)
        for _ in range(num_ped):
            while True:
                angle = random.uniform(0, 1) * np.pi * 2
                # add some noise to simulate all the possible cases robot could meet with human
                px_noise = (random.uniform(0, 1) - 0.5)  ## human.v_pref
                py_noise = (random.uniform(0, 1) - 0.5)  ## human.v_pref
                px = radius * np.cos(angle) + px_noise
                py = radius * np.sin(angle) + py_noise
                collide = False
                for agent in agent_list:
                    min_dist = 0.8
                    if mode == 'trajnet':
                        min_dist = 2    ## min_dist ~ 2*human.radius + discomfort_dist ## 2 (TrajNet++)
                    if norm((px - agent[0], py - agent[1])) < min_dist or \
                            norm((px - agent[2], py - agent[3])) < min_dist:
                        collide = True
                        break
                if not collide:
                    break

            positions.append((px, py))
            goals.append((-px, -py))
            if sim is not None:
                sim.addAgent((px, py))
            velocity = np.array([-2 * px, -2 * py])
            magnitude = np.linalg.norm(velocity)
            init_vel = 1 * velocity / magnitude if magnitude > 1 else velocity
            speed.append([init_vel[0], init_vel[1]])
            agent_list.append([px, py, -px, -py])
        trajectories = [[positions[i]] for i in range(num_ped)]
        return trajectories, positions, goals, speed

    def configure(self, config):
        # self.time_step = config.getfloat('orca', 'time_step')
        # self.neighbor_dist = config.getfloat('orca', 'neighbor_dist')
        # self.max_neighbors = config.getint('orca', 'max_neighbors')
        # self.time_horizon = config.getfloat('orca', 'time_horizon')
        # self.time_horizon_obst = config.getfloat('orca', 'time_horizon_obst')
        # self.radius = config.getfloat('orca', 'radius')
        # self.max_speed = config.getfloat('orca', 'max_speed')
        return

    def set_phase(self, phase):
        return

    # TODO: incorporate sf_params into state
    #                                  [tau, v0,  sigma]
    def predict(self, state):#, sf_params=[0.5, 2.1, 0.3], end_range=0.2):
        """
        Create a socialforce simulation at each time step and run one step


        ========================================================================
        == ORCA Description ====================================================
        Create a rvo2 simulation at each time step and run one step
        Python-RVO2 API: https://github.com/sybrenstuvel/Python-RVO2/blob/master/src/rvo2.pyx
        How simulation is done in RVO2: https://github.com/sybrenstuvel/Python-RVO2/blob/master/src/Agent.cpp

        Agent doesn't stop moving after it reaches the goal, because once it stops moving, the reciprocal rule is broken
        ========================================================================

        :param state:
        state = JointState()
        - state.human_states: [ObservableState, ...]: TODO: is it a list? tuple? tensor?
        - state.self_state: FullState

        # TODO: socialforce wants state as a numpy array or tensor! Will not like the state object used here!

        crowd_sim/envs/utils/state.py
        - FullState: [px, py, vx, vy, r, goalx, goaly, v_pref, theta]
        - ObservableState: [px, py, vx, vy, r]

        :return:
        action
        """
        #self_state = state.self_state
        params = self.neighbor_dist, self.max_neighbors, self.time_horizon, self.time_horizon_obst
        v0_init = np.random.normal(1.34, 0.26, size=(2))
        ped_ped = PedPedPotential(1./fps, v0=sf_params[1], sigma=sf_params[2])
        field_of_view = FieldOfView()

        # delete old one, TODO: make it so it isn't deleted if there are the correct number of agents, as is done for orca
        if self.sim is not None: #and self.sim.getNumAgents() != len(state.human_states) + 1:
            del self.sim
            self.sim = None
        # build new sim
        if self.sim is None:
            # intialize sim object
            #socialforce.Simulator(initial_state, ped_ped=ped_ped, field_of_view=field_of_view,
            #                  delta_t=1./fps, tau=sf_params[0])
            #                                       TODO: THIS WON'T WORK BECAUSE THESE ARE STATE OBJECTS AND NOT JUST LISTS.
            #                                             WILL NEED TO TURN THIS INTO A WORKABLE FORM. But how can they pass
            #                                             their state object into rvo2??
            self.sim = socialforce.Simulator(torch.tensor([state.self_state] + state.human_states), ped_ped=ped_ped, field_of_view=field_of_view,
                              delta_t=self.time_step, tau=sf_params[0])
            #self.sim = rvo2.PyRVOSimulator(self.time_step, *params, self.radius, self.max_speed)
            # add robot
            self.sim.addAgent(self_state.position, *params, self_state.radius + 0.01 + self.safety_space,
                              self_state.v_pref, self_state.velocity)
            # add all humans
            for human_state in state.human_states:
                self.sim.addAgent(human_state.position, *params, human_state.radius + 0.01 + self.safety_space,
                                  self.max_speed, human_state.velocity)

        # TODO: I could just make it create a new simulator at every timestep for now.
        #       This if-else tree is to save computation
        # XXX: IN THE END I DON'T THINK THE Simulator CLASS KEEPS TRACK OF NUM_HUMANS DIRECTLY
        #      Actually, it might indirectly, with one of the dimensions of **self.V = ped_ped**
        # # if there exists self.sim but it has the wrong number of agents
        # if self.sim is not None and self.sim.getNumAgents() != len(state.human_states) + 1:
        #     del self.sim
        #     self.sim = None
        # build new sim
        # if self.sim is None:
        #     # intialize sim object
        #     self.sim = rvo2.PyRVOSimulator(self.time_step, *params, self.radius, self.max_speed)
        #     # add robot
        #     self.sim.addAgent(self_state.position, *params, self_state.radius + 0.01 + self.safety_space,
        #                       self_state.v_pref, self_state.velocity)
        #     # add all humans
        #     for human_state in state.human_states:
        #         self.sim.addAgent(human_state.position, *params, human_state.radius + 0.01 + self.safety_space,
        #                           self.max_speed, human_state.velocity)
        # # sim exists and is the right size
        # else:
        #     # set robot at current pos and velocity
        #     self.sim.setAgentPosition(0, self_state.position)
        #     self.sim.setAgentVelocity(0, self_state.velocity)
        #     # set humans at current pos and velocity
        #     for i, human_state in enumerate(state.human_states):
        #         self.sim.setAgentPosition(i + 1, human_state.position)
        #         self.sim.setAgentVelocity(i + 1, human_state.velocity)

        # Set the preferred velocity to be a vector of unit magnitude (speed) in the direction of the goal.
        velocity = np.array((self_state.gx - self_state.px, self_state.gy - self_state.py))
        speed = np.linalg.norm(velocity)
        pref_vel = velocity / speed if speed > 1 else velocity

        # XXX: maybe will need for sf?
        # Perturb a little to avoid deadlocks due to perfect symmetry.
        # perturb_angle = np.random.random() * 2 * np.pi
        # perturb_dist = np.random.random() * 0.01
        # perturb_vel = np.array((np.cos(perturb_angle), np.sin(perturb_angle))) * perturb_dist
        # pref_vel += perturb_vel

        self.sim.setAgentPrefVelocity(0, tuple(pref_vel))


        for i, human_state in enumerate(state.human_states):
            # unknown goal position of other humans
            self.sim.setAgentPrefVelocity(i + 1, (0, 0))

        # carry out step in simulator
        self.sim.doStep()
        # action is defined in problem as instantaneous velocity (x,y)
        action = ActionXY(*self.sim.getAgentVelocity(0))
        self.last_state = state

        return action
