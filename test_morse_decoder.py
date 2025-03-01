import pytest
from morse_decoder import MorseCodeDecoder

def test_encode():
    decoder = MorseCodeDecoder()
    assert decoder.encode("SOS") == "... --- ..."
    assert decoder.encode("HELLO") == ".... . .-.. .-.. ---"
    assert decoder.encode("12345") == ".---- ..--- ...-- ....- ....."

def test_decode():
    decoder = MorseCodeDecoder()
    assert decoder.decode("... --- ...") == "SOS"
    assert decoder.decode(".... . .-.. .-.. ---") == "HELLO"
    assert decoder.decode(".---- ..--- ...-- ....- .....") == "12345"
