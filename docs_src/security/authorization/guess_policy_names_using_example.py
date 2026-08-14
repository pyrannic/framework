from pyrannic import ServiceProvider
from pyrannic.contracts import GateInterface
from pyrannic.ioc import Resolves
from pyrannic.support import string


class AppServiceProvider(ServiceProvider):
    def boot(self, gate: Resolves[GateInterface]) -> None:
        gate.guess_policy_names_using(self.guess_policy_name)

    def guess_policy_name(self, model_name: str) -> str | list[str]:
        """Return the full module path and class name of the policy for the given model."""

        if model_name == "User":
            return "app.my_awesome_policies.user.UserPolicy"
        elif model_name == "Post":
            return [
                "app.my_awesome_policies.post.PostPolicy",
                "app.my_awesome_policies.blog_post.BlogPostPolicy",
            ]
        else:
            return f"app.my_awesome_policies.{string.to_snake_case(model_name)}.{model_name}Policy"
