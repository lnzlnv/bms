const normalizeData = (data) => {
  const content = {
    count: data.count,
    next: data.next,
    previous: data.previous,
    results: {}
  }

  for(let i = 0; i < data.results.length; ++i) {
    content['results'][data.results[i].id] = data.results[i];
  }

  return content
}

export default normalizeData;