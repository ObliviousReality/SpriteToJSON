import argparse
from numpy import asarray, size
import os
from PIL import Image


def convertFile(file: str, sourcedir: str, outdir: str, one_file_mode: bool) -> None:
    spriteName, spriteType = file.split(".")

    if (spriteType != "png"):
        print(f"ERROR: Only supports .png files. File '{file}' is not a PNG.")
        return

    im = Image.open(sourcedir + "/" + file)
    arr = asarray(im)
    height = size(arr, 0)
    width = size(arr, 1)

    data = []
    for i in arr:
        buf = []
        for j in i:
            try:
                buf.append("0" if j[2] == 255 else "1")
            except Exception:
                print(
                    f"File: '{file}' has an incorrect bit-depth. Files must have a bit-depth of 32 bits.")
                break
        data.append(buf)
    im.close()

    if (not one_file_mode):
        outfile = open(outdir +"/" + spriteName + ".json", "w")
        outfile.write("{")
    else:
        outfile = open(outdir +"/output.json", "a")

    outfile.write('\n"' + spriteName + '": {\n')
    outfile.write('"width": ' + str(width) + ',\n')
    outfile.write('"height": ' + str(height) + ',\n')
    outfile.write('"data": [\n')
    count = 0
    for item in data:
        if (count == len(data) - 1):
            outfile.write('[' + ",".join(item) + ']\n')
        else:
            outfile.write('[' + ",".join(item) + '],\n')
            count += 1
    outfile.write(']\n}\n')
    if (not one_file_mode):
        outfile.write('}')
    outfile.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-sourcedir", default='./sprites')
    parser.add_argument('-outdir', default="./out")
    parser.add_argument('-one', action='store_true', default=False)
    args = parser.parse_args()

    if (not os.path.exists(args.outdir)):
        os.makedirs(args.outdir)
    
    if (args.one):
        f = open(args.outdir + "/output.json", "w")
        f.write("{")
        f.close()

    file_list = os.listdir(args.sourcedir)
    for file in file_list:
        convertFile(file, args.sourcedir, args.outdir, args.one)
        if (args.one and (file_list.index(file) != len(file_list) - 1)):
            f = open(args.outdir + "/output.json", "a")
            f.write(",")
            f.close()

    if (args.one):
        f = open(args.outdir + "/output.json", "a")
        f.write("}\n")
        f.close()

if __name__ == "__main__":
    main()
