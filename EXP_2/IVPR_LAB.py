class Image():
    def __init__(self, filename):
        self.read_bmp_image(filename)

    def read_bmp_image(self, filename):
        with open(filename, "rb") as f:
            self.signature = f.read(2).decode("ascii")
            if self.signature != "BM":
                raise ValueError("Not a valid BMP file.")

            self.file_size = int.from_bytes(f.read(4), "little")
            self.reserved = int.from_bytes(f.read(4), "little")
            self.data_offset = int.from_bytes(f.read(4), "little")

            self.info_header_size = int.from_bytes(f.read(4), "little")
            self.width = int.from_bytes(f.read(4), "little")
            self.height = int.from_bytes(f.read(4), "little")
            self.planes = int.from_bytes(f.read(2), "little")
            self.bits_per_pixel = int.from_bytes(f.read(2), "little")
            self.compression = int.from_bytes(f.read(4), "little")
            self.image_size = int.from_bytes(f.read(4), "little")
            self.XpixelsperM = int.from_bytes(f.read(4), "little")
            self.YpixelsperM = int.from_bytes(f.read(4), "little")
            self.colors_used = int.from_bytes(f.read(4), "little")
            self.imp_colors = int.from_bytes(f.read(4), "little")

            if self.bits_per_pixel <= 8:
                if self.colors_used == 0:
                    self.colors_used = 2 ** self.bits_per_pixel
                self.color_table = [[], [], [], []]
                for _ in range(self.colors_used):
                    blue = int.from_bytes(f.read(1), "little")
                    green = int.from_bytes(f.read(1), "little")
                    red = int.from_bytes(f.read(1), "little")
                    reserved = int.from_bytes(f.read(1), "little")
                    self.color_table[0].append(blue)
                    self.color_table[1].append(green)
                    self.color_table[2].append(red)
                    self.color_table[3].append(reserved)

            self.image_array = []
            row_padding = (4 - (self.width * self.bits_per_pixel // 8) % 4) % 4

            for _ in range(self.height):
                row = []
                for _ in range(self.width):
                    if self.bits_per_pixel == 8:
                        row.append(int.from_bytes(f.read(1), "little"))
                    elif self.bits_per_pixel == 24:
                        blue = int.from_bytes(f.read(1), "little")
                        green = int.from_bytes(f.read(1), "little")
                        red = int.from_bytes(f.read(1), "little")
                        pixel = (red << 16) | (green << 8) | blue
                        row.append(pixel)
                f.read(row_padding)  
                self.image_array.append(row)

            print("-------------------------------------------------")
            print("File name :", filename)
            print("Height :", self.height)
            print("Width :", self.width)
            print("Bit Depth :", self.bits_per_pixel)
            print("File Size :", self.file_size)
            print("Image Data Size :", self.image_size)
            print("Data Offset :", self.data_offset)
            print("Colors Used:",  self.colors_used )
            print("-------------------------------------------------")

    def writeBMP(self, filename):
        with open(filename, "wb") as f:
            signature = 'BM'
            color_table_size = 4 * self.colors_used if self.bits_per_pixel <= 8 else 0
            row_padding = (4 - (self.width * self.bits_per_pixel // 8) % 4) % 4
            row_size = (self.width * self.bits_per_pixel // 8) + row_padding
            file_size = 14 + 40 + color_table_size + row_size * self.height
            data_offset = 14 + 40 + color_table_size

            f.write(signature.encode("ascii"))
            f.write(file_size.to_bytes(4, "little"))
            f.write((0).to_bytes(4, "little"))
            f.write(data_offset.to_bytes(4, "little"))

            f.write(self.info_header_size.to_bytes(4, "little"))
            f.write(self.width.to_bytes(4, "little"))
            f.write(self.height.to_bytes(4, "little"))
            f.write(self.planes.to_bytes(2, "little"))
            f.write(self.bits_per_pixel.to_bytes(2, "little"))
            f.write(self.compression.to_bytes(4, "little"))
            f.write(self.image_size.to_bytes(4, "little"))
            f.write(self.XpixelsperM.to_bytes(4, "little"))
            f.write(self.YpixelsperM.to_bytes(4, "little"))
            f.write(self.colors_used.to_bytes(4, "little"))
            f.write(self.imp_colors.to_bytes(4, "little"))

            if self.bits_per_pixel <= 8:
                for i in range(self.colors_used):
                    f.write(self.color_table[0][i].to_bytes(1, "little"))
                    f.write(self.color_table[1][i].to_bytes(1, "little"))
                    f.write(self.color_table[2][i].to_bytes(1, "little"))
                    f.write(self.color_table[3][i].to_bytes(1, "little"))

            for row in self.image_array:
                for pixel in row:
                    if self.bits_per_pixel == 8:
                        f.write(pixel.to_bytes(1, "little"))
                    elif self.bits_per_pixel == 24:
                        blue = pixel & 0xFF
                        green = (pixel >> 8) & 0xFF
                        red = (pixel >> 16) & 0xFF
                        f.write(blue.to_bytes(1, "little"))
                        f.write(green.to_bytes(1, "little"))
                        f.write(red.to_bytes(1, "little"))
                f.write(b'\x00' * row_padding)

    def has_color_table(self):
        return self.bits_per_pixel <= 8

    def remove_red(self, filename):
        if self.has_color_table():
            backup = self.color_table[2][:]
            self.color_table[2] = [0 for _ in self.color_table[2]]
            self.writeBMP(filename)
            self.color_table[2] = backup
        elif self.bits_per_pixel == 24:
            modified = []
            for row in self.image_array:
                new_row = []
                for pixel in row:
                    blue = pixel & 0xFF
                    green = (pixel >> 8) & 0xFF
                    new_pixel = (green << 8) | blue  
                    new_row.append(new_pixel)
                modified.append(new_row)
            backup = self.image_array
            self.image_array = modified
            self.writeBMP(filename)
            self.image_array = backup

    def remove_green(self, filename):
        if self.has_color_table():
            backup = self.color_table[1][:]
            self.color_table[1] = [0 for _ in self.color_table[1]]
            self.writeBMP(filename)
            self.color_table[1] = backup
        elif self.bits_per_pixel == 24:
            modified = []
            for row in self.image_array:
                new_row = []
                for pixel in row:
                    blue = pixel & 0xFF
                    red = (pixel >> 16) & 0xFF
                    new_pixel = (red << 16) | blue 
                    new_row.append(new_pixel)
                modified.append(new_row)
            backup = self.image_array
            self.image_array = modified
            self.writeBMP(filename)
            self.image_array = backup

    def remove_blue(self, filename):
        if self.has_color_table():
            backup = self.color_table[0][:]
            self.color_table[0] = [0 for _ in self.color_table[0]]
            self.writeBMP(filename)
            self.color_table[0] = backup
        elif self.bits_per_pixel == 24:
            modified = []
            for row in self.image_array:
                new_row = []
                for pixel in row:
                    green = (pixel >> 8) & 0xFF
                    red = (pixel >> 16) & 0xFF
                    new_pixel = (red << 16) | (green << 8)  
                    new_row.append(new_pixel)
                modified.append(new_row)
            backup = self.image_array
            self.image_array = modified
            self.writeBMP(filename)
            self.image_array = backup



if __name__ == "__main__":
    images = ["cameraman.bmp", "corn.bmp", "pepper.bmp"]
    
    for img_path in images:
        print(f"\nProcessing: {img_path}")
        img = Image(img_path)

        img.writeBMP(img_path.replace(".bmp", "_copy.bmp"))

        img.remove_red(img_path.replace(".bmp", "_no_red.bmp"))
        img.remove_green(img_path.replace(".bmp", "_no_green.bmp"))
        img.remove_blue(img_path.replace(".bmp", "_no_blue.bmp"))
