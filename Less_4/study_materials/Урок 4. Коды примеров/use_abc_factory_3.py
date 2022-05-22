from abc_factory_3 import AbstractFactory

factory_type = input()
factory = AbstractFactory.create_factory(factory_type)

parser = factory.create_parser()
analizer = factory.create_analizer()
sender = factory.create_sender()

parser.parse()
