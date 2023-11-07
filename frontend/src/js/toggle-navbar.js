const layers = [
  document.querySelector('.js-layer-1'),
  document.querySelector('.js-layer-2'),
  document.querySelector('.js-layer-3')
]

const links = document.querySelector('.js-links')

document.querySelector('.js-btn-burger').addEventListener('click', () => {
  links.classList.toggle('custom-h-1')

  layers[0].classList.toggle('layer-1')
  layers[1].classList.toggle('layer-2')
  layers[2].classList.toggle('layer-3')
})