import os

def delete_file(mes, src):
    try:
        os.remove(src)
    except:
        pass

    try:
        os.remove(f'files/{mes}/photos/photos_1.jpg')
    except:
        pass
