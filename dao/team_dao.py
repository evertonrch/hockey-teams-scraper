import logging
from config.db_config import get_connection
from model.team import Team

log = logging.getLogger(__name__)

def save(team: Team) -> None:
    conn = get_connection()
    cursor = conn.cursor()

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
        log.error("erro ao inserir no banco: ", str(ex))
    
    cursor.close()
    conn.close()

    