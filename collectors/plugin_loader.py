import importlib.util
import inspect
from collectors.collector import Collector


class CollectorLoader:
    def __init__(self, module_path: str):
        self.module_path = f'collectors/{module_path}.py'
        self.module = None

    def load_module(self):
        spec = importlib.util.spec_from_file_location("dynamic_module", self.module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.module = module
        return module

    def create_instance(self, class_name: str, url: str):
        if self.module is None:
            self.load_module()

        cls = getattr(self.module, class_name, None)
        if cls is None:
            raise ImportError(f"The class '{class_name}' not found in the module '{self.module_path}'")


        if not inspect.isclass(cls) or not issubclass(cls, Collector):
            raise TypeError(f"The class '{class_name}' is not an inheritor of 'Collector'")

        return cls(url)
