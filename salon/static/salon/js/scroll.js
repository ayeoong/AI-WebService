const slideDiv = document.querySelectorAll('.items');
let isDown;
let startX;
let scrollLeft;


slideDiv.forEach(slider =>
  slider.addEventListener('mousedown', (e) => {
    isDown = true;
    slider.classList.add('active');
    startX = e.pageX - slider.offsetLeft;
    scrollLeft = slider.scrollLeft;
  })
);
slideDiv.forEach(slider =>
  slider.addEventListener('mouseleave', () => {
    isDown = false;
    slider.classList.remove('active');
  })
);
slideDiv.forEach(slider =>
  slider.addEventListener('mouseup', () => {
    isDown = false;
    slider.classList.remove('active');
  })
);
slideDiv.forEach(slider =>
  slider.addEventListener('mousemove', (e) => {
    if(!isDown) return;
    e.preventDefault();
    const x = e.pageX - slider.offsetLeft;
    const walk = (x - startX) * 3; //scroll-fast
    slider.scrollLeft = scrollLeft - walk;
    // console.log(walk);
  })
);
