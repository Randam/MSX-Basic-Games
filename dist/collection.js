const cards = [...document.querySelectorAll('.collection-card')];
const search = document.querySelector('#collection-search');
const brand = document.querySelector('#collection-brand');
const buttons = [...document.querySelectorAll('button[data-generation]')];
const count = document.querySelector('#collection-count');
let generation = '';
const searchable = new Map(cards.map(card => [card, card.textContent.toLocaleLowerCase('nl')]));
function filterCollection() {
  const terms = search.value.toLocaleLowerCase('nl').trim().split(/\s+/).filter(Boolean);
  let visible = 0;
  for (const card of cards) {
    const matches = (!brand.value || card.dataset.brand === brand.value)
      && (!generation || card.dataset.generation === generation)
      && terms.every(term => searchable.get(card).includes(term));
    card.hidden = !matches;
    if (matches) visible++;
  }
  count.textContent = `${visible} van ${cards.length} computers`;
  document.querySelector('#collection-empty').hidden = visible !== 0;
  for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.generation === generation));
}
search.addEventListener('input', filterCollection);
brand.addEventListener('change', filterCollection);
for (const button of buttons) button.addEventListener('click', () => {
  generation = button.dataset.generation;
  filterCollection();
});
document.querySelector('#reset-collection').addEventListener('click', () => {
  generation = ''; search.value = ''; brand.value = '';
  filterCollection();
});
document.querySelector('.collection-tools').hidden = false;
filterCollection();
