from app.models.post import Post
from app.policies.post import PostPolicy

from pyrannic import ServiceProvider
from pyrannic.contracts import GateInterface
from pyrannic.ioc import Resolves


class AppServiceProvider(ServiceProvider):
    def boot(self, gate: Resolves[GateInterface]) -> None:
        gate.define_policy(Post, PostPolicy)
