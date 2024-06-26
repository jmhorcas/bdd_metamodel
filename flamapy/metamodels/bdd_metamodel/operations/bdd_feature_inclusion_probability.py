from typing import Any, Optional, cast

from flamapy.core.models import VariabilityModel
from flamapy.metamodels.configuration_metamodel.models.configuration import Configuration
from flamapy.metamodels.bdd_metamodel.models import BDDModel
from flamapy.metamodels.bdd_metamodel.operations.interfaces import FeatureInclusionProbability
from flamapy.metamodels.bdd_metamodel.operations import BDDProducts


class BDDFeatureInclusionProbability(FeatureInclusionProbability):
    """The Feature Inclusion Probability (FIP) operation determines the probability
    for a variable to be included in a valid solution.

    This is a brute-force implementation that enumerates all solutions
    for calculating the probabilities.

    Ref.: [Heradio et al. 2019. Supporting the Statistical Analysis of Variability Models. SPLC.
    (https://doi.org/10.1109/ICSE.2019.00091)]
    """

    def __init__(self, partial_configuration: Optional[Configuration] = None) -> None:
        self.result: dict[Any, float] = {}
        self.partial_configuration = partial_configuration

    def execute(self, model: VariabilityModel) -> 'BDDFeatureInclusionProbability':
        bdd_model = cast(BDDModel, model)
        self.result = feature_inclusion_probability(bdd_model, self.partial_configuration)
        return self

    def get_result(self) -> dict[Any, float]:
        return self.result

    def feature_inclusion_probability(self) -> dict[Any, float]:
        return self.get_result()


def feature_inclusion_probability(bdd_model: BDDModel,
                                  config: Optional[Configuration] = None) -> dict[Any, float]:
    products = BDDProducts(config).execute(bdd_model).get_result()
    n_products = len(products)
    if n_products == 0:
        return {feature: 0.0 for feature in bdd_model.variables}

    prob = {}
    for feature in bdd_model.variables:
        prob[feature] = sum(feature in p.elements for p in products) / n_products
    return prob
