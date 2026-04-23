from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

k = "e30a5b292fdc400a8e942c406a5eab91"
c = "66b6c18775c1db96d9ec22f32d422a876524f917774d17c2d639a59787e53fbd"

cipher = Cipher(algorithms.Camellia(bytes.fromhex(k)), modes.ECB())
decryptor = cipher.decryptor()

answer = decryptor.update(bytes.fromhex(c)) + decryptor.finalize()
print(answer.decode())