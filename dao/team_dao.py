import logging
from pathlib import Path
from config.db_config import get_connection
from model.team import Team

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
ddl_file = ROOT / "ddl.sql"

def create_table():
    with open(ddl_file, "r") as file:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(file.read())

def save(team: Team) -> None:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            create_table()
            
            sql = """
                INSERT INTO tb_hockei_team(
                    name, year, wins, losses, ot_losses, win_percent, goals_for, goals_against, diff
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s 
                )
            """.strip()

            try:
                log.info(f"inserindo dados do time: {team.name} no banco...")
                cursor.execute(sql, tuple(team.__dict__.values()))
                conn.commit()
            except Exception as ex:
                log.error("erro ao inserir no banco: %s", ex)