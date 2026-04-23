// use this on browser's console when on the challenges page
let s = document.createElement('script');
s.src = 'https://cdnjs.cloudflare.com/ajax/libs/html-to-image/1.11.11/html-to-image.min.js';
document.head.appendChild(s);
s.onload = () => htmlToImage.toPng(document.querySelector('.main-content')).then(d => {
    let a = document.createElement('a');
    a.download = 'screenshot.png';
    a.href = d;
    a.click();
});