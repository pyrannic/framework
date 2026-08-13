from pyrannic import ServiceProvider
from pyrannic.contracts import GateInterface
from pyrannic.ioc import Resolves


class AppServiceProvider(ServiceProvider):
    def boot(self, gate: Resolves[GateInterface]) -> None:
        gate.define_ability("update-post", lambda user, post: user.id == post.user_id)
