from binascii import crc32

from PIL.Image import NONE


class PNGChunkAnaliser:
    #PNG == Portable Network Graphics
    def __init__(self, FileName=None):
        self.width = 0
        self.height = 0
        self.bit_depth = 0
        self.color_type = 0
        self.chunks = []
        self.pallet = []
        self.functions = {}
        self.FileName = FileName

        # Gives the functions "names" that match their chunks
        self.functions[b'IHDR'] = self.IHDR_chunk
        self.functions[b'sRGB'] = self.sRGB_chunk
        self.functions[b'gAMA'] = self.gAMA_chunk
        self.functions[b'PLTE'] = self.PLTE_chunk
        self.functions[b'tEXt'] = self.tEXT_chunk

        if FileName != None:
            self.ReadPNG()


    #only prints the name, effectively a handler for unhandled chunks
    def DefaultChunkHandler(self, index, name, data):
        print(f'{name.decode("utf-8")} Chunk (Unhandled)')

    def ReadPNG(self, FileName):
        self.ReadChunks(FileName)
        for index, chunk in enumerate(self.chunks):
            self.functions.get(chunk[0],self.DefaultChunkHandler)(index,chunk[0],chunk[1]) 
            #chunk[0] is the name, chunk[1] is the data

    def ReadPNG(self):
        self.ReadChunks(self.FileName)
        for index, chunk in enumerate(self.chunks):
            self.functions.get(chunk[0],self.DefaultChunkHandler)(index,chunk[0],chunk[1]) 
            #chunk[0] is the name, chunk[1] is the data

    def ReadChunks(self, FileName):
        self.chunks.clear()
        with open(FileName, 'rb') as File:
            # Checking signature
            if File.read(8) != b'\x89PNG\r\n\x1a\n':
                raise Exception('Signature error')
            info = File.read(4)
            while info != b'':
                length = int.from_bytes(info, 'big')
                data = File.read(4 + length)
                if int.from_bytes(File.read(4), 'big') != crc32(data):
                    raise Exception('CRC Checkerror')
                #appends chunk name + its data
                self.chunks.append([data[:4], data[4:]])
                info = File.read(4)

    def IHDR_chunk(self, index, name, data):
        types = {0: 'Grayscale',
            2: 'Truecolor',
            3: 'Indexed-color',
            4: 'Greyscale with alpha',
            6: 'Truecolor with alpha'}

        if index != 0:
            raise Exception('first chunk')
        self.width = int.from_bytes(data[:4], 'big')
        self.height = int.from_bytes(data[4:8], 'big')
        self.bit_depth = int.from_bytes(data[8:9], 'big')
        self.color_type = int.from_bytes(data[9:10], 'big')
        print('IHDR Chunk')
        print(f'  width : {self.width}')
        print(f'  height: {self.height}')
        print(f'  bit depth: {self.bit_depth}')
        print(f'  color type: {types[self.color_type]}')
        print(f'  compression method: {int.from_bytes(data[10:11], "big")}')
        print(f'  filter method: {int.from_bytes(data[11:12], "big")}')
        print(f'  interlace method: {int.from_bytes(data[12:13], "big")}')

    def PLTE_chunk(self, index, name, data):
        print(f'{name.decode("utf-8")} Chunk')
        temp = divmod(len(data), 3)

        if temp[1] != 0:
            raise Exception('pallet')
        for pin in range(temp[0]):
            color = data[pin * 3], data[pin * 3 + 1], data[pin * 3 + 2]
            print(f'  #{color[0]:02X}{color[1]:02X}{color[2]:02X}')
            self.pallet.append(color)

    def gAMA_chunk(self, index, name, data):
        print(f'{name.decode("utf-8")} Chunk')
        print(f'  Image gamma: {int.from_bytes(data, "big")}')

    def tEXT_chunk(self, index, name, data):
        print(f'{name.decode("utf-8")} Chunk')
        txt = data.split(b'\x00')
        print(f'  {txt[0].decode("utf-8")}: {txt[1].decode("utf-8")}')

    def sRGB_chunk(self, index, name, data):
        print(f'{name.decode("utf-8")} Chunk')
        types = {
            0: 'Perceptual',
            1: 'Relatice colorimetric',
            2: 'Saturation',
            3: 'Absolute colorimetric'
            }
        index = int.from_bytes(data, 'big')
        print(f'  Rendering intent: {types[index]}')





#if __name__ == '__main__':
#    PPP = PNG('png_files\\type_3.png')