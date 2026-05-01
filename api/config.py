import os
from typing import List


class Config:
    # API Config
    title: str
    description: str
    environment: str
    version: str
    root_path: str

    # CORS Config
    cors_origins: List[str]

    # Mail Config
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str

    def __init__(self):
        config = os.environ
        # General Config
        self.title = config.get("API_TITLE", default="Niyya Women Verification")
        self.description = config.get("API_DESCRIPTION", default="Verification with Niyya constraints")
        self.environment = config.get("ENVIRONMENT", default="dev")
        self.version = config.get("API_VERSION", default="0.1.0")
        self.root_path = config.get("API_ROOT", default="/api/v1")
        # CORS Config
        self.cors_origins = str(config.get("CORS_ORIGINS", default=[]) or "").split(",")
        # Mail Config
        self.mail_username = config.get("MAIL_USERNAME")
        self.mail_password = config.get("MAIL_PASSWORD")
        self.mail_from = config.get("MAIL_FROM")
        self.mail_port = config.get("MAIL_PORT", default=587)
        self.mail_server = config.get("MAIL_SERVER", default="smtp.gmail.com")
        self.mail_from_name = config.get("MAIL_FROM_NAME", default="Portfolio Contact")
