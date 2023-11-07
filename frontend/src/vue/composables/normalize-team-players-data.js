const normalizeData = (data) => {
  let content = {}  
  let players = data.home_team.players

  for (let i = 0; i < players.length; ++i ) {
    content[players[i].info.player_number] = players[i]
  }

  data.home_team.players = content

  content = {}
  players = data.away_team.players

  for (let i = 0; i < players.length; ++i ) {
    content[players[i].info.player_number] = players[i]
  }

  data.away_team.players = content

  return data
}

const normalize = (players) => {
  

  players = content
}

export default normalizeData