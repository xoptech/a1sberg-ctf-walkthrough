document.addEventListener("DOMContentLoaded", () => {
    const textElements = document.querySelectorAll('.typing');
    textElements.forEach(el => {
        const content = el.innerText; el.innerText = '';
        let i = 0; function typeWriter() {
            if (i < content.length) {
                el.innerHTML += content.charAt(i);
                i++;
                setTimeout(typeWriter, 40);
            }
        }
        typeWriter();
    });
});