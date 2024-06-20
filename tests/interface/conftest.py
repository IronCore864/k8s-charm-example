import pytest
from charm import MyFancyDatabaseCharm
from interface_tester import InterfaceTester
from scenario.state import State


@pytest.fixture
def interface_tester(interface_tester: InterfaceTester):
    interface_tester.configure(
        charm_type=MyFancyDatabaseCharm,
        state_template=State(
            leader=True,  # we need leadership
        ),
    )
    # this fixture needs to yield (NOT RETURN!) interface_tester again
    yield interface_tester
