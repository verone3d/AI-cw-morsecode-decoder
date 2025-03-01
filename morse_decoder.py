class MorseCodeDecoder:
    MORSE_CODE_DICT = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        '0': '-----', ' ': ' '
    }

    def encode(self, message: str) -> str:
        """Convert text to Morse code."""
        morse = []
        for char in message.upper():
            if char in self.MORSE_CODE_DICT:
                morse.append(self.MORSE_CODE_DICT[char])
        return ' '.join(morse)

    def decode(self, morse_code: str) -> str:
        """Convert Morse code to text."""
        reverse_dict = {value: key for key, value in self.MORSE_CODE_DICT.items()}
        text = []
        for code in morse_code.split(' '):
            if code in reverse_dict:
                text.append(reverse_dict[code])
        return ''.join(text)


def main():
    decoder = MorseCodeDecoder()
    print("Morse Code Decoder")
    print("1. Text to Morse Code")
    print("2. Morse Code to Text")
    
    choice = input("Enter your choice (1/2): ")
    
    if choice == '1':
        text = input("Enter text to convert: ")
        morse = decoder.encode(text)
        print(f"Morse code: {morse}")
    elif choice == '2':
        morse = input("Enter Morse code (use spaces between letters): ")
        text = decoder.decode(morse)
        print(f"Decoded text: {text}")
    else:
        print("Invalid choice!")


if __name__ == '__main__':
    main()
