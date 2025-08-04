import os
import opik
from loguru import logger
from opik.configurator.configure import OpikConfigurator
from config import settings

def configure() -> None:
    """
    Configure Opik/Comet integration if OPIK_API_KEY and OPIK_PROJECT are set in the environment.
    """
    api_key = settings.OPIK_API_KEY
    project = settings.OPIK_PROJECT

    if api_key and project:
        try:
            client = OpikConfigurator(api_key=api_key)
            default_workspace = client._get_default_workspace()
        except Exception as e:
            logger.warning(f"Default workspace not found: {e}. Setting workspace to None and enabling interactive mode.")
            default_workspace = None

        os.environ["OPIK_PROJECT_NAME"] = project

        try:
            opik.configure(
                api_key=api_key,
                workspace=default_workspace,
                use_local=False,
                force=True,
            )
            logger.info(f"Opik configured successfully using workspace '{default_workspace}'")
        except Exception as e:
            logger.error(f"Opik configuration failed: {e}")
            logger.warning(
                "Couldn't configure Opik. There may be a problem with the OPIK_API_KEY, OPIK_PROJECT, or the Opik server."
            )
    else:
        logger.warning(
            "OPIK_API_KEY and OPIK_PROJECT are not set. Set them to enable prompt monitoring with Opik (powered by Comet ML)."
        )