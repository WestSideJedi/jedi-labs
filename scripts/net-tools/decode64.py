import base64
# ask user for input
encoded_data = input("Enter Base64 encoded text:")

while True:
    try:
        # decode the input
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        print("Decoded data: " + decoded_data)
        # ask if user wants to keep decoding 
        choice = input("Decode again? (y/n): ")
        if choice.lower() != 'y':
            break


         # Update the encoded data for the next iteration
        encoded_data = decoded_data
    except Exception as e:
        print("Decoding error: " + str(e))
        break