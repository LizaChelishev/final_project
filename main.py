from db_config import create_all_entities
from db_repo import DbRepo

local_session = create_all_entities()
db_repo = DbRepo(local_session)
