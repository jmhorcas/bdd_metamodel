from typing import Optional, cast

from flamapy.core.models import VariabilityModel
from flamapy.metamodels.configuration_metamodel.models.configuration import Configuration
from flamapy.core.operations import ConfigurationsNumber
from flamapy.metamodels.bdd_metamodel.models.bdd_model import BDDModel


class BDDConfigurationsNumber(ConfigurationsNumber):
    """It computes the number of solutions of the BDD model.

    It also supports counting the solutions from a given partial configuration.
    """

    def __init__(self, partial_configuration: Optional[Configuration] = None) -> None:
        self.result = 0
        self.partial_configuration = partial_configuration

    def execute(self, model: VariabilityModel) -> 'BDDConfigurationsNumber':
        bdd_model = cast(BDDModel, model)
        self.result = configurations_number(bdd_model, self.partial_configuration)
        return self

    def get_result(self) -> int:
        return self.result

    def get_configurations_number(self) -> int:
        return self.get_result()


def configurations_number(bdd_model: BDDModel,
                          partial_configuration: Optional[Configuration] = None) -> int:
    if partial_configuration is None:
        u_func = bdd_model.root
        n_vars = len(bdd_model.variables)
    else:
        values = dict(partial_configuration.elements.items())
        u_func = bdd_model.bdd.let(values, bdd_model.root)
        n_vars = len(bdd_model.variables) - len(values)

    return bdd_model.bdd.count(u_func, nvars=n_vars)