import math
from bod import BuildOrderDeviation
from neural_network import NeuralNetwork

class BuildOrderDetect(object):

    def detect_build_order(bo, compare_bo, depth=-1):
        """Determines how likely a build order is modeled after the benchmark build.

        Determines the confidence that the given build order is modeled after the
        benchmark build order contained here.

        Args:
            compare_bo (BuildOrderElement[]): An array of BuildOrderElements to
                determine if it closely matches the benchmark build order.
                
            (depth) (int): Optional. The depth with which to traverse the build order. If
                not defined (-1), the entire build order will be used.

        Returns:
            int: The confidence (0.0 - 1.0) that the given build order is a derivative
                of the benchmark build order.

            BuildOrderDeviation: The BOD object used to determine the confidence.
                
        """
        bod = BuildOrderDeviation(bo)
        bod.calculate_deviations(compare_bo, depth)
        order_dev = bod.get_scaled_order_dev()
        ## there could be more accuracy if the discrepencies were split into 4 categories:
        ## worker, army, building, upgrade and a NN trained on those inputs instead.
        discrepencies = bod.get_scaled_discrepency()

        #confidence = BuildOrderDetect._nn3_feed_forward(order_dev, discrepencies)
        nn = BuildOrderDetect._get_nn()
        confidence = nn.feed_forward([order_dev, discrepencies])[0]

        return confidence, bod


    def _get_nn():
        return BuildOrderDetect._get_nn3()

    def _get_nn1():
        return None

    def _get_nn2():
        return None

##------
##* Inputs: 2
##------
##Hidden Layer
##Neurons: 3
## Neuron 0
##  Weight: 1.438617802013817
##  Weight: 1.210894486550306
##  Bias: 0.9830518282072616
## Neuron 1
##  Weight: -6.123341253463274
##  Weight: -2.4295370408770265
##  Bias: 0.9830518282072616
## Neuron 2
##  Weight: 2.255625136086102
##  Weight: 1.2090876656522709
##  Bias: 0.9830518282072616
##------
##* Output Layer
##Neurons: 1
## Neuron 0
##  Weight: -2.9882917693755138
##  Weight: 25.94240655627592
##  Weight: -4.283797205140412
##  Bias: 0.3817826993754133
##------
    def _get_nn3():
        h0_w = [1.438617802013817, 1.210894486550306]
        h1_w = [-6.123341253463274, -2.4295370408770265]
        h2_w = [2.255625136086102, 1.2090876656522709]
        h_b = 0.9830518282072616
        o_w = [-2.9882917693755138, 25.94240655627592, -4.283797205140412]
        o_b = 0.3817826993754133

        return NeuralNetwork(2, 3, 1, h0_w + h1_w + h2_w, h_b, o_w, o_b)
        

    def _nn_feed_forward(order, disc):
        NN_WI1 = -0.8326388182288694
        NN_WI2 = -7.0693717100666690
        NN_BI = 0.8541325726369238
        NN_WH = 19.123065721771997
        NN_BH = 0.20449835272881134

        h = 1 / (1 + math.exp(-(order * NN_WI1 + disc * NN_WI2 + NN_BI)))
        out = 1 / (1 + math.exp(-(h * NN_WH + NN_BH)))

        return out

##------
##* Inputs: 2
##------
##Hidden Layer
##Neurons: 2
## Neuron 0
##  Weight: 8.338633843804
##  Weight: -1.5270798061037594
##  Bias: 0.9785443288439529
## Neuron 1
##  Weight: -13.711848744765582
##  Weight: 1.835616004688895
##  Bias: 0.9785443288439529
##------
##* Output Layer
##Neurons: 1
## Neuron 0
##  Weight: -8.431803459641838
##  Weight: 20.56901232827286
##  Bias: 0.8140641980822715
##------
    def _nn2_feed_forward(order, disc):
        NN_WOH1 = 8.338633843804
        NN_WDH1 = -1.5270798061037594
        NN_BH1 = 0.9785443288439529
        NN_WOH2 = -13.711848744765582
        NN_WDH2 = 1.835616004688895
        NN_BH2 = 0.9785443288439529
        NN_WO1 = -8.431803459641838
        NN_WO2 = 20.56901232827286
        NN_BO = 0.8140641980822715

        h1 = 1 / (1 + math.exp(-(order * NN_WOH1 + disc * NN_WDH1 + NN_BH1)))
        h2 = 1 / (1 + math.exp(-(order * NN_WOH2 + disc * NN_WDH2 + NN_BH2)))

        out = 1 / (1 + math.exp(-(h1 * NN_WO1 + h2 * NN_WO2 + NN_BO)))

        return out

##------
##* Inputs: 2
##------
##Hidden Layer
##Neurons: 2
## Neuron 0
##  Weight: -7.605137795850566
##  Weight: -2.0031154649023453
##  Bias: 0.7924616674420797
## Neuron 1
##  Weight: 5.556900142766295
##  Weight: 0.427239990025159
##  Bias: 0.7924616674420797
##------
##* Output Layer
##Neurons: 1
## Neuron 0
##  Weight: 22.604220170902686
##  Weight: -6.1049626514600215
##  Bias: 0.8554616195309589
##------
    def _nn3_feed_forward(order, disc):
        NN_WOH1 = -7.605137795850566
        NN_WDH1 = -2.0031154649023453
        NN_BH1 = 0.7924616674420797
        NN_WOH2 = 5.556900142766295
        NN_WDH2 = 0.427239990025159
        NN_BH2 = 0.7924616674420797
        NN_WO1 = 22.604220170902686
        NN_WO2 = -6.1049626514600215
        NN_BO = 0.8554616195309589

        h1 = 1 / (1 + math.exp(-(order * NN_WOH1 + disc * NN_WDH1 + NN_BH1)))
        h2 = 1 / (1 + math.exp(-(order * NN_WOH2 + disc * NN_WDH2 + NN_BH2)))

        out = 1 / (1 + math.exp(-(h1 * NN_WO1 + h2 * NN_WO2 + NN_BO)))

        return out
