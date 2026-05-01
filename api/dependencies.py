from logging import Logger

from fastapi import Request, Depends

from api.config import Config


def get_config(request: Request) -> Config:
    return request.app.state.cfg


def get_logger(request: Request) -> Logger:
    return request.app.state.logger



class CommonDependencies:
    def __init__(
        self,
        config: Config = Depends(get_config),
        logger: Logger = Depends(get_logger),
    ):
        self.cfg: Config = config
        self.logger: Logger = logger