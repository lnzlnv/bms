export default (data) => {
  const content = data
  content.unshift(data[data.length-1])
  content.push(data[0])

  return data
}