const normalizeData_2 = (data) => {
  const content = {
    id: data.id,
    in_game_players: data.in_game_players,
    home_team: {},
    away_team: {},
    slug: data.slug,
    statistician: data.statistician
  }

  normalizePlayers(content.home_team, data.home_team)
  normalizePlayers(content.away_team, data.away_team)
  return content  
}

const normalizePlayers = (teamContent, teamData) => {
  for (let key in teamData) {
    if (key != 'players') {
      teamContent[key] = teamData[key]
    } else {
      teamContent['players'] = {}
    }
  }
  for (let index in teamData.players) {
    teamContent['players'][teamData.players[index].number] = 
      teamData.players[index]
  }
}

export default normalizeData_2;