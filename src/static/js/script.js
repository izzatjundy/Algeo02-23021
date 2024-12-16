let index = 0;

function moveSlide(direction) {
    const gallery = document.querySelector('.display-foto-page');
    const totalImages = document.querySelectorAll('.display-foto-each').length;

    index += direction;
            
    if (index < 0) {
        index = totalImages - 1;
    } else if (index >= totalImages) {
        index = 0;
    }

    const offset = -(index * 290); // Each image width + margin
    gallery.style.transform = `translateX(${offset}px)`;
}