from audio_processor import MorseAudioProcessor
import time
import os

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
    audio_processor = MorseAudioProcessor()
    
    while True:
        print("\nMorse Code Decoder")
        print("1. Text to Morse Code")
        print("2. Morse Code to Text")
        print("3. Audio File to Morse Code")
        print("4. Live Audio to Morse Code")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            text = input("Enter text to convert: ")
            morse = decoder.encode(text)
            print(f"Morse code: {morse}")

        elif choice == '2':
            morse = input("Enter Morse code (use spaces between letters): ")
            text = decoder.decode(morse)
            print(f"Decoded text: {text}")

        elif choice == '3':
            file_path = input("Enter the path to your audio file (MP3 or WAV): ")
            if os.path.exists(file_path):
                try:
                    print("Processing audio file...")
                    morse_code = audio_processor.process_audio_file(file_path)
                    print(f"Detected Morse code: {morse_code}")
                    if morse_code:
                        decoded_text = decoder.decode(morse_code)
                        print(f"Decoded text: {decoded_text}")
                    else:
                        print("No Morse code signals detected in the audio file.")
                except Exception as e:
                    print(f"Error processing audio file: {str(e)}")
            else:
                print("File not found!")

        elif choice == '4':
            print("Starting live audio recording...")
            print("Press Ctrl+C or wait 10 seconds to stop recording")
            
            try:
                stream = audio_processor.start_live_recording()
                time.sleep(10)  # Record for 10 seconds
                morse_code = audio_processor.stop_live_recording(stream)
                
                if morse_code:
                    print(f"\nDetected Morse code: {morse_code}")
                    decoded_text = decoder.decode(morse_code)
                    print(f"Decoded text: {decoded_text}")
                else:
                    print("\nNo Morse code signals detected.")
                    
            except KeyboardInterrupt:
                print("\nStopping recording...")
                morse_code = audio_processor.stop_live_recording(stream)
                if morse_code:
                    print(f"Detected Morse code: {morse_code}")
                    decoded_text = decoder.decode(morse_code)
                    print(f"Decoded text: {decoded_text}")
                else:
                    print("No Morse code signals detected.")
            except Exception as e:
                print(f"Error recording audio: {str(e)}")

        elif choice == '5':
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == '__main__':
    main()
