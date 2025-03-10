from dataclasses import dataclass, field


@dataclass
class Module:
    name: str
    credits: int = None
    score: float = None


@dataclass
class User:
    name: str
    modules: list[Module] = field(default_factory=list)

    def get_module_names(self) -> list[str]:
        return [module.name for module in self.modules]

    def get_modules(self) -> list[Module]:
        return self.modules

    def get_module_by_name(self, module_name: str) -> Module:
        return next(
            (
                (i, module)
                for i, module in enumerate(self.modules)
                if module.name == module_name
            ),
            None,
        )

    def add_module(self, module: str) -> None:
        self.modules.append(Module(module))

    def update_module_name(self, old_module: str, new_module: str) -> None:
        i, update_module = self.get_module_by_name(old_module)
        update_module.name = new_module
        self.modules[i] = update_module

    def update_module(self, old_module: str, module: Module) -> None:
        i, _update_module = self.get_module_by_name(old_module)
        self.modules[i] = module

    @property
    def total_credits(self) -> int:
        return sum(module.credits for module in self.modules if module.credits)

    @property
    def credits_so_far(self) -> int:
        return sum(
            module.credits * module.score / 100
            for module in self.modules
            if module.score is not None
        )

    @property
    def total_credits_so_far(self) -> int:
        return sum(
            module.credits for module in self.modules if module.score is not None
        )

    @property
    def score_so_far(self) -> float:
        return (
            100 * self.credits_so_far / self.total_credits_so_far
            if self.total_credits_so_far
            else 0
        )

    def score_needed(self, target_score) -> float:
        return (
            100
            * (self.total_credits * target_score - self.credits_so_far)
            / (self.total_credits - self.total_credits_so_far)
        )
