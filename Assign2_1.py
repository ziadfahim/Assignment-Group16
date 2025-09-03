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