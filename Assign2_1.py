def shift_char(ch, shift, base):
    return chr((ord(ch) - base + shift) % 26 + base)

# Tags to remember rule applied
TAG_NON_ALPHA = 0
TAG_LOW_A_M   = 1
TAG_LOW_N_Z   = 2
TAG_UP_A_M    = 3
TAG_UP_N_Z    = 4

def classify_char(ch):
    if ch.islower():
        return TAG_LOW_A_M if 'a' <= ch <= 'm' else TAG_LOW_N_Z
    if ch.isupper():
        return TAG_UP_A_M if 'A' <= ch <= 'M' else TAG_UP_N_Z
    return TAG_NON_ALPHA

def transform_text(text, shift1, shift2, mode, tags=None):
    k_low_forward = shift1 * shift2
    k_low_backward = shift1 + shift2
    k_up_backward = shift1
    k_up_forward = shift2 ** 2

    out_chars = []
    out_tags = []

    if mode == "encrypt":
        for ch in text:
            tag = classify_char(ch)
            out_tags.append(str(tag))
            if tag == TAG_LOW_A_M:
                out_chars.append(shift_char(ch, +k_low_forward, ord('a')))
            elif tag == TAG_LOW_N_Z:
                out_chars.append(shift_char(ch, -k_low_backward, ord('a')))
            elif tag == TAG_UP_A_M:
                out_chars.append(shift_char(ch, -k_up_backward, ord('A')))
            elif tag == TAG_UP_N_Z:
                out_chars.append(shift_char(ch, +k_up_forward, ord('A')))
            else:
                out_chars.append(ch)
        # Save tags at the top of the encrypted text, separated by "|"
        return "|".join(out_tags) + "\n" + "".join(out_chars)

    else:  # decrypt
        tag_line, enc_body = text.split("\n", 1)
        tags = [int(x) for x in tag_line.split("|")]
        for ch, tag in zip(enc_body, tags):
            if tag == TAG_LOW_A_M:
                out_chars.append(shift_char(ch, -(shift1 * shift2), ord('a')))
            elif tag == TAG_LOW_N_Z:
                out_chars.append(shift_char(ch, +(shift1 + shift2), ord('a')))
            elif tag == TAG_UP_A_M:
                out_chars.append(shift_char(ch, +(shift1), ord('A')))
            elif tag == TAG_UP_N_Z:
                out_chars.append(shift_char(ch, -(shift2 ** 2), ord('A')))
            else:
                out_chars.append(ch)
        return "".join(out_chars)

def verify_files(file1, file2):
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
        return f1.read() == f2.read()

if __name__ == "__main__":
    shift1 = int(input("Enter shift1 value: "))
    shift2 = int(input("Enter shift2 value: "))

    raw_file = "raw_text.txt"
    encrypted_file = "encrypted_text.txt"
    decrypted_file = "decrypted_text.txt"

    # Encrypt
    with open(raw_file, "r", encoding="utf-8") as f:
        raw_text = f.read()
    encrypted_text = transform_text(raw_text, shift1, shift2, "encrypt")
    with open(encrypted_file, "w", encoding="utf-8") as f:
        f.write(encrypted_text)
    print("Encrypted file created")

    # Decrypt
    with open(encrypted_file, "r", encoding="utf-8") as f:
        encrypted_text = f.read()
    decrypted_text = transform_text(encrypted_text, shift1, shift2, "decrypt")
    with open(decrypted_file, "w", encoding="utf-8") as f:
        f.write(decrypted_text)
    print("Decrypted file created")

    # Verify
    if verify_files(raw_file, decrypted_file):
        print("Verification successful! Decryption matches original.")
    else:
        print("Verification failed.")