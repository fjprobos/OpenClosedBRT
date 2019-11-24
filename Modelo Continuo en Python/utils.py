# Script to add some auxiliar functions

def geometry_sensitivity_parameters(lambdap, lambdac, lambdaCBD, R, R1, beta, alpha, alpha1, alpha2,
                                    beta1, beta2, delta, multiplier):
    """

    :param lambdap:
    :param lambdac:
    :param lambdaCBD:
    :param R:
    :param R1:
    :param beta:
    :param alpha:
    :param alpha1:
    :param alpha2:
    :param beta1:
    :param beta2:
    :param delta:
    :param multiplier:
    :return:
    """

    corridor_demand = (beta - R1)*R*lambdac
    beta_new = beta*multiplier
    lambdac_new = corridor_demand/((beta_new - R1)*R)
    cbd_demand = R1*R*lambdaCBD
    lambdaCBD_new = cbd_demand/(R1*R)
    alpha1_new = alpha1*multiplier
    alpha2_new = alpha2*multiplier
    periphery_demand = (alpha1+alpha2)*lambdap
    lambdap_new = periphery_demand/(alpha1_new+alpha2_new)
    alpha_new = alpha*multiplier
    beta1_new = beta1*multiplier
    beta2_new = beta2*multiplier

    corridor_demand_new = (beta_new - R1)*R*lambdac_new
    periphery_demand_new = (alpha1_new+alpha2_new)*lambdap_new

    # Each of the later elements have to maintain their demand when increasing their areas, so new
    # areas have to be computed with new demand density as well.

    return lambdap_new, lambdac_new, lambdaCBD_new, R, R1, beta_new, alpha_new, alpha1_new, alpha2_new, beta1_new,\
        beta2_new, delta
