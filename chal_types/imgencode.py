from PIL import Image
import math
import wave
import array
from pydub import AudioSegment


def start(inputfile, outputfile, duration, original_audio):
    im = Image.open(inputfile)
    width, height = im.size
    rgb_im = im.convert('RGB')

    durationSeconds = float(duration)
    tmpData = []
    maxFreq = 0
    data = array.array('h')
    sampleRate = 44100
    channels = 1
    dataSize = 2

    numSamples = int(sampleRate * durationSeconds)
    samplesPerPixel = math.floor(numSamples / width)

    C = 20000 / height

    for x in range(numSamples):
        rez = 0

        pixel_x = int(x / samplesPerPixel)
        if pixel_x >= width:
            pixel_x = width - 1

        for y in range(height):
            r, g, b = rgb_im.getpixel((pixel_x, y))
            s = r + g + b

            volume = s * 100 / 765

            if volume == 0:
                continue

            freq = int(C * (height - y + 1))

            rez += getData(volume, freq, sampleRate, x)

        tmpData.append(rez)
        if abs(rez) > maxFreq:
            maxFreq = abs(rez)

    for i in range(len(tmpData)):
        data.append(int(32767.0 * tmpData[i] / maxFreq))

    f = wave.open(outputfile, 'w')
    f.setparams((channels, dataSize, sampleRate,
                numSamples, "NONE", "Uncompressed"))
    f.writeframes(data.tobytes())
    f.close()
    if original_audio:
        combine(outputfile, original_audio)


def combine(outputfile, original_audio):
    audio1 = AudioSegment.from_file(original_audio, format="wav")
    audio2 = AudioSegment.from_file(outputfile, format="wav")
    audio1 = audio1.set_channels(1)
    combined = audio1 + audio2
    combined.export(outputfile, format="wav")


def getData(volume, freq, sampleRate, index):
    return int(volume * math.sin(freq * math.pi * 2 * index / sampleRate))
