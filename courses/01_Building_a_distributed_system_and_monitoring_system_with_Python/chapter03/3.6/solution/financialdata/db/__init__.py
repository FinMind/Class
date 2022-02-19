from financialdata.db.router import (
    Router,
)
from financialdata.db.db import *

router = Router()


def get_db_router():
    return router
