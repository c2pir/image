import numpy as np

DEFAULT_INPUTS_SHIFTS = np.array([[0, 0], [0, 1], [0, -1], [1, 0], [-1, 0]])
DEFAULT_OUTPUTS_SHIFTS = np.array([[-1, 2], [0, 2], [1, 2],
                                   [-1, -2], [0, -2], [1, -2],
                                   [2, -1], [2, 0], [2, 1],
                                   [-1, -1], [-1, 1], [1, -1], [1, 1]])

def create_nodes_equalizer_from(context, behaviour,
                                globals_inputs = [],
                                inputs_shifts = DEFAULT_INPUTS_SHIFTS,
                                outputs_shifts = DEFAULT_OUTPUTS_SHIFTS):
    """ """
    all_nodes = []
    for i in range(len(context)):
        for j in range(len(context[0])):
            ne = NodeEqualizer([i, j], behaviour)
            ne.globals_inputs = globals_inputs
            ne.outputs_shifts = outputs_shifts
            ne.inputs_shifts = inputs_shifts
            all_nodes.append(ne)
    return all_nodes

def setInBound(position,context):
    h,w = context.shape
    position[0] = position[0] % h
    position[1] = position[1] % w
    # negative index managment
    if position[0]<0:
        position[0] += h
    if position[1]<0:
        position[1] += w
    return position

class NodeEqualizer(object):
    """ TODO """
    def __init__(self, position, behaviour):
        self.position = np.array(position)
        self.behaviour = behaviour
        self.globals_inputs = []
        self.inputs_shifts = []
        self.outputs_shifts = []

    def iteration(self, context, editable_mask, dt = 0.1):
        """ TODO """
        new_context = context.copy()
        x = self.construct_x(context)

        if self.behaviour is not None:
            outs = self.behaviour(x)
            var = 0
            for i in range(len(outs)):
                p = self.position + self.outputs_shifts[i]
                p = setInBound(p, context)

                # vérifier que la position est éditable
                if editable_mask[p[0], p[1]]:
                    var = outs[i]-context[p[0], p[1]]
                    new_context[p[0], p[1]] += dt*var

        return new_context

    def construct_x(self,context):
        """ TODO """
        x = []
        for shift in self.inputs_shifts:
            p = self.position + shift
            p = setInBound(p, context)
            x.append(context[p[0], p[1]])
        return x+self.globals_inputs

if __name__=="__main__":
    from skimage import io
    import matplotlib.pyplot as plt

    context = io.imread("../icons/cut.png",as_gray=True)

    def behaviour(x):
        return np.random.random((13,))

    all_nodes = create_nodes_equalizer_from(context,behaviour)

    ones = np.ones_like(context)
    result = context.copy()
    for node in all_nodes:
        result = node.iteration(result,ones,dt = 0.05)

    plt.imshow(result)