def caesar_cipher_decoder(message, offset):
    """
    Decodes a message using the Caesar cipher.
    
    Args:
        message: Message to decode
        offset: Number of positions to shift
        
    Returns:
        Decoded message
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    punctuation = [" ", ",", ".", "!", "?"]
    decoded_message = ""
    for char in message:
        if char in punctuation:
            decoded_message += char
        else:
            decoded_message += alphabet[(alphabet.find(char) + offset) % len(alphabet)]
    return decoded_message

def caesar_cipher_encoder(message, offset):
    """
    Encodes a message using the Caesar cipher.
    
    Args:
        message: Message to encode
        offset: Number of positions to shift
        
    Returns:
        Encoded message
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    punctuation = [" ", ",", ".", "!", "?"]
    coded_message = ""
    for char in message:
        if char in punctuation:
            coded_message += char
        else:
            coded_message += alphabet[(alphabet.find(char) + offset) % len(alphabet)]
    return coded_message

def vigenere_cipher_decoder(message, key):
    """
    Decodes a message using the Vigenère cipher.
    
    Args:
        message: Message to decode
        key: Key to use for decoding
        
    Returns:
        Decoded message
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    punctuation = [" ", ",", "'", ".", "!", "?"]
    decoded_message = ""
    ki = 0
    for i in range(len(message)):
        if ki >= len(key):
            ki = 0
        if message[i] in punctuation:
            decoded_message += message[i]
        else:
            offset = alphabet.find(key[ki])
            location = (alphabet.find(message[i]) - offset) % 26
            decoded_message += alphabet[location]
            ki += 1
    return decoded_message

def vigenere_cipher_encoder(message, key):
    """
    Encodes a message using the Vigenère cipher.
    
    Args:
        message: Message to encode
        key: Key to use for encoding
        
    Returns:
        Encoded message
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    punctuation = [" ", ",", "'", ".", "!", "?"]
    encoded_message = ""
    ki = 0
    for i in range(len(message)):
        if ki >= len(key):
            ki = 0
        if message[i] in punctuation:
            encoded_message += message[i]
        else:
            offset = alphabet.find(key[ki])
            location = (alphabet.find(message[i]) + offset) % 26
            encoded_message += alphabet[location]
            ki += 1
    return encoded_message 