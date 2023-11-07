const normalizeData = (data) => {
  const content = {}

  for(let i = 0; i < data.length; ++i) {
    content[data[i].player_number] = data[i];
  }

  return content
}

export default normalizeData