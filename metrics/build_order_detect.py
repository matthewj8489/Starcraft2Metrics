import math
from metrics.bod import BuildOrderDeviation
from metrics.neural_network import NeuralNetwork
import metrics.unit_constants as uc

class BuildOrderDetect(object):

    def detect_build_order(bo, compare_bo, depth=-1):
        """Determines how closely two build orders match each other.

        Args:
            bo (BuildOrderElement[]): A build order to compare against.

            compare_bo (BuildOrderElement[]): A build order that will be compared to bo.
                
            (depth) (int): Optional. The depth with which to traverse the build order. If
                not defined (-1), the entire build order will be used.

        Returns:
            int: The confidence (0.0 - 1.0) that the compare_bo build order is a derivative
                of the bo build order.

            BuildOrderDeviation: The BOD object used to determine the confidence.
                
        """
        bod = BuildOrderDeviation(bo)
        bod.calculate_deviations(compare_bo, depth)
        #order_dev = bod.get_scaled_order_dev()
        ## there could be more accuracy if the discrepencies were split into 4 categories:
        ## worker, army, building, upgrade and a NN trained on those inputs instead.
        #discrepencies = bod.get_scaled_discrepency()

        #confidence = BuildOrderDetect._nn3_feed_forward(order_dev, discrepencies)
        #nn = BuildOrderDetect._get_nn()
        #confidence = nn.feed_forward([order_dev, discrepencies])[0]

        confidence = BuildOrderDetect._get_confidence(bod)

        return confidence, bod

    def _get_confidence(bod):
        return BuildOrderDetect._get_11_in_confidence(bod)

    def _get_11_in_confidence(bod):
        nn = BuildOrderDetect._get_11_in_4_hidden_nn2()
        return nn.feed_forward([bod.get_scaled_order_dev(),
                                bod.get_scaled_tag_order_dev(uc.WORKER_TAG),
                                bod.get_scaled_tag_order_dev(uc.ARMY_TAG),
                                bod.get_scaled_tag_order_dev(uc.BUILDING_TAG),
                                bod.get_scaled_tag_order_dev(uc.UPGRADE_TAG),
                                bod.get_scaled_tag_order_dev(uc.BASE_TAG),
                                bod.get_scaled_tag_order_dev(uc.SUPPLY_TAG),
                                bod.get_scaled_tag_order_dev(uc.PRODUCTION_TAG),
                                bod.get_scaled_tag_order_dev(uc.TECH_TAG),
                                bod.get_scaled_tag_order_dev(uc.STAT_TAG),
                                bod.get_scaled_discrepency()])[0]

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

# error:  1.1429904571108542
# ------
# * Inputs: 11
# ------
# Hidden Layer
# Neurons: 4
#  Neuron 0
#   Weight: 1.3424953169896272
#   Weight: -0.78795003383842
#   Weight: 0.6858100797810829
#   Weight: 1.565989441772572
#   Weight: 1.772776172725554
#   Weight: 0.1040434713955894
#   Weight: -0.4038231268624331
#   Weight: 2.273535925445667
#   Weight: 1.1965322943452563
#   Weight: 0.23546043643790626
#   Weight: 0.577843129095928
#   Bias: 0.5073119112112034
#  Neuron 1
#   Weight: 1.4537194324420568
#   Weight: -1.1505121910005616
#   Weight: 1.168194045744283
#   Weight: 0.69931006236948
#   Weight: 1.3540174152790672
#   Weight: 0.8862108383249583
#   Weight: -0.47751226377026834
#   Weight: 2.809561695019671
#   Weight: 1.8388481222975248
#   Weight: 0.4541530057677762
#   Weight: 0.5301504097180963
#   Bias: 0.5073119112112034
#  Neuron 2
#   Weight: 1.3996831702684862
#   Weight: 0.18172169577654296
#   Weight: 0.6152008413407345
#   Weight: 0.768879045972945
#   Weight: 0.5108218676327336
#   Weight: 0.6365350838735276
#   Weight: -0.05418273312952676
#   Weight: 1.6023575630601723
#   Weight: 0.6666880817685606
#   Weight: 0.42369065793603533
#   Weight: 0.7145718710398888
#   Bias: 0.5073119112112034
#  Neuron 3
#   Weight: -4.914719737462895
#   Weight: 7.93776438411558
#   Weight: -1.8603166007285221
#   Weight: -2.486331973070748
#   Weight: -6.357063769302771
#   Weight: 0.7923950855295077
#   Weight: 4.873586795506894
#   Weight: -10.80830931894128
#   Weight: -6.782512419223006
#   Weight: 0.09213037641564148
#   Weight: -0.03239491768802935
#   Bias: 0.5073119112112034
# ------
# * Output Layer
# Neurons: 1
#  Neuron 0
#   Weight: -4.716993852540922
#   Weight: -5.387323540178562
#   Weight: -2.8946503690397662
#   Weight: 26.77988076064274
#   Bias: 0.9558905275220134
# ------
    def _get_11_in_4_hidden_nn():
        h0_w = [1.3424953169896272, -0.78795003383842, 0.6858100797810829, 1.565989441772572,
                1.772776172725554, 0.1040434713955894, -0.4038231268624331, 2.273535925445667,
                1.1965322943452563, 0.23546043643790626, 0.577843129095928]
        h1_w = [1.4537194324420568, -1.1505121910005616, 1.168194045744283, 0.69931006236948,
                1.3540174152790672, 0.8862108383249583, -0.47751226377026834, 2.809561695019671,
                1.8388481222975248, 0.4541530057677762, 0.5301504097180963]
        h2_w = [1.3996831702684862, 0.18172169577654296, 0.6152008413407345, 0.768879045972945,
                0.5108218676327336, 0.6365350838735276, -0.05418273312952676, 1.6023575630601723,
                0.6666880817685606, 0.42369065793603533, 0.7145718710398888]
        h3_w = [-4.914719737462895, 7.93776438411558, -1.8603166007285221, -2.486331973070748,
                -6.357063769302771, 0.7923950855295077, 4.873586795506894, -10.80830931894128,
                -6.782512419223006, 0.09213037641564148, -0.03239491768802935]
        h_b = 0.5073119112112034
        o_w = [-4.716993852540922, -5.387323540178562, -2.8946503690397662, 26.77988076064274]
        o_b = 0.9558905275220134

        return NeuralNetwork(11, 4, 1, h0_w + h1_w + h2_w + h3_w, h_b, o_w, o_b)


# error:  0.7989472036499342
# ------
# * Inputs: 11
# ------
# Hidden Layer
# Neurons: 4
#  Neuron 0
#   Weight: -7.970815600531029
#   Weight: 10.542279921514856
#   Weight: -3.6187680730386025
#   Weight: -0.8334123316107944
#   Weight: -11.446509428051742
#   Weight: -2.9410427994449324
#   Weight: 6.950148799151987
#   Weight: -23.235113478622825
#   Weight: -11.531035813317295
#   Weight: 6.715622760849261
#   Weight: 1.0033074016597492
#   Bias: 0.38169903502202085
#  Neuron 1
#   Weight: 1.9346887387205673
#   Weight: -2.317210779451903
#   Weight: 1.6553996089866703
#   Weight: 1.6865985167588242
#   Weight: 2.6607532207809634
#   Weight: 1.0123101156225829
#   Weight: -0.4371368893194504
#   Weight: 5.037322630766162
#   Weight: 2.493956271363889
#   Weight: -0.46569355943939933
#   Weight: 0.23611939474208044
#   Bias: 0.38169903502202085
#  Neuron 2
#   Weight: 1.0166519015462108
#   Weight: -0.6243755727582182
#   Weight: 1.439588096136361
#   Weight: 1.4927671322677272
#   Weight: 0.9396990924921599
#   Weight: 0.4471278679620689
#   Weight: 0.6454797079737866
#   Weight: 3.088870218367033
#   Weight: 1.3294631651155733
#   Weight: -0.334291191988051
#   Weight: 0.4361978751225785
#   Bias: 0.38169903502202085
#  Neuron 3
#   Weight: 1.6671982122844833
#   Weight: -1.8608472688584787
#   Weight: 1.621878276046722
#   Weight: 1.296840280736802
#   Weight: 1.463163025275035
#   Weight: 0.6798635054297681
#   Weight: 0.04428297796056346
#   Weight: 3.3082927132431963
#   Weight: 2.20753252543875
#   Weight: -0.37094441779997567
#   Weight: 0.3670225242384293
#   Bias: 0.38169903502202085
# ------
# * Output Layer
# Neurons: 1
#  Neuron 0
#   Weight: 42.47676782652039
#   Weight: -7.051942893210369
#   Weight: -3.5845153026074
#   Weight: -5.156678187797401
#   Bias: 0.6278831031881964
# ------
    def _get_11_in_4_hidden_nn2():
        h0_w = [-7.970815600531029, 10.542279921514856, -3.6187680730386025, -0.8334123316107944,
                -11.446509428051742, -2.9410427994449324, 6.950148799151987, -23.235113478622825,
                -11.531035813317295, 6.715622760849261, 1.0033074016597492]
        h1_w = [1.9346887387205673, -2.317210779451903, 1.6553996089866703, 1.6865985167588242,
                2.6607532207809634, 1.0123101156225829, -0.4371368893194504, 5.037322630766162,
                2.493956271363889, -0.46569355943939933, 0.23611939474208044]
        h2_w = [1.0166519015462108, -0.6243755727582182, 1.439588096136361, 1.4927671322677272,
                0.9396990924921599, 0.4471278679620689, 0.6454797079737866, 3.088870218367033,
                1.3294631651155733, -0.334291191988051, 0.4361978751225785]
        h3_w = [1.6671982122844833, -1.8608472688584787, 1.621878276046722, 1.296840280736802,
                1.463163025275035, 0.6798635054297681, 0.04428297796056346, 3.3082927132431963,
                2.20753252543875, -0.37094441779997567, 0.3670225242384293]
        h_b = 0.38169903502202085
        o_w = [42.47676782652039, -7.051942893210369, -3.5845153026074, -5.156678187797401]
        o_b = 0.6278831031881964

        return NeuralNetwork(11, 4, 1, h0_w + h1_w + h2_w + h3_w, h_b, o_w, o_b)