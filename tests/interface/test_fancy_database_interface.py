from interface_tester import InterfaceTester


def test_fancy_database_interface(interface_tester: InterfaceTester):
    interface_tester.configure(
        interface_name="my-fancy-database",
        interface_version=0,
    )
    interface_tester.run()
